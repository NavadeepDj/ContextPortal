"""Run the installer outside the Windows launcher that it needs to replace."""

import base64
import json
import os
import subprocess
import sys
from pathlib import Path

_UPGRADE_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Wait-ForLauncherExit($process) {
    if ($process -and -not $process.WaitForExit(30000)) {
        throw 'A ContextPortal process did not exit in time.'
    }
}

try {
    $upgrade = $env:CONTEXTPORTAL_WINDOWS_UPGRADE | ConvertFrom-Json
    $env:CONTEXTPORTAL_WINDOWS_UPGRADE = $null

    $updaterProcess = Get-Process -Id $upgrade.updater_pid -ErrorAction SilentlyContinue
    $launcherProcess = Get-Process -Id $upgrade.parent_pid -ErrorAction SilentlyContinue |
        Where-Object { $upgrade.launcher -and $_.Path -eq $upgrade.launcher }
    Wait-ForLauncherExit $updaterProcess
    Wait-ForLauncherExit $launcherProcess

    if ($upgrade.launcher) {
        $session = (Get-Process -Id $PID).SessionId
        $mcpProcesses = Get-CimInstance Win32_Process -Filter "Name = 'contextportal.exe'" -ErrorAction SilentlyContinue |
            Where-Object {
                $_.SessionId -eq $session -and $_.ExecutablePath -eq $upgrade.launcher -and
                    $_.CommandLine -match '^\s*(?:"[^"]+"|\S+)\s+(?:mcp|"mcp")\s*$'
            }
        foreach ($instance in $mcpProcesses) {
            $process = Get-Process -Id $instance.ProcessId -ErrorAction SilentlyContinue
            if (-not $process -or $process.Path -ne $upgrade.launcher -or
                [Math]::Abs(($process.StartTime - $instance.CreationDate).TotalMilliseconds) -ge 1) {
                continue
            }

            # Hold the process handle while taskkill acts on the PID and its children.
            [void]$process.Handle
            if ($process.HasExited) { continue }
            [Console]::WriteLine('Stopping a ContextPortal MCP server from this installation.')
            & "$env:SystemRoot\System32\taskkill.exe" /PID $process.Id /T /F | Out-Null
            if ($LASTEXITCODE -ne 0 -and -not $process.HasExited) {
                throw 'Could not stop a ContextPortal MCP server.'
            }
            Wait-ForLauncherExit $process
        }
    }

    $installer = $upgrade.command[0]
    $installerArgs = @($upgrade.command | Select-Object -Skip 1)
    & $installer @installerArgs
    if ($LASTEXITCODE -ne 0) { throw "The installer exited with code $LASTEXITCODE." }

    [Console]::WriteLine('ContextPortal upgrade finished. Run contextportal --version to confirm the installed version.')
    [Console]::WriteLine('Reconnect ContextPortal in your MCP client to start a fresh server.')
} catch {
    [Console]::Error.WriteLine("ContextPortal upgrade failed: $($_.Exception.Message)")
    [Console]::Error.WriteLine('If the launcher is locked, disconnect ContextPortal from your MCP client and retry.')
    exit 1
}
"""


def start_windows_upgrade(command: list[str]) -> None:
    """Start an external helper so the current Python process and launcher can exit."""
    # The Windows console entry point uses the launcher as Python's script argument.
    # A direct `python -m app.cli` invocation has no launcher to match or stop.
    launcher = None
    if len(sys.orig_argv) > 1:
        script = Path(sys.orig_argv[1])
        if script.name.lower() == "contextportal.exe":
            launcher = str(script.resolve())

    payload = json.dumps(
        {
            "updater_pid": os.getpid(),
            "parent_pid": os.getppid(),
            "launcher": launcher,
            "command": command,
        }
    )
    encoded_script = base64.b64encode(_UPGRADE_SCRIPT.encode("utf-16-le")).decode(
        "ascii"
    )
    powershell = (
        Path(os.environ["SystemRoot"])
        / "System32/WindowsPowerShell/v1.0/powershell.exe"
    )
    subprocess.Popen(
        [
            str(powershell),
            "-NoProfile",
            "-NonInteractive",
            "-EncodedCommand",
            encoded_script,
        ],
        stdin=subprocess.DEVNULL,
        env={**os.environ, "CONTEXTPORTAL_WINDOWS_UPGRADE": payload},
    )
