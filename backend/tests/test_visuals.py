from unittest.mock import MagicMock, patch

import pytest

from app.core.visuals import (
    MAX_VISUAL_BYTES,
    VisualURLPolicyError,
    _BrowserURLPolicy,
    _collect_visuals,
    _original_image,
    _track_image,
)

PNG = b"\x89PNG\r\n\x1a\noriginal image"
IMAGE_URL = "https://cdn.example.com/image.png"


def mock_image():
    response = MagicMock()
    response.url = IMAGE_URL
    response.headers = {"content-type": "image/png"}
    response.server_addr.return_value = {"ipAddress": "93.184.216.34", "port": 443}
    response.request.sizes.return_value = {"responseBodySize": len(PNG)}
    response.body.return_value = PNG
    element = MagicMock()
    element.bounding_box.return_value = {"width": 210, "height": 120}
    element.evaluate.side_effect = [
        "img",
        {"url": IMAGE_URL, "alt": "A diagram", "pixels": 25200},
    ]
    return element, response


def test_visuals_use_original_image_and_only_capture_drawn_chart():
    page = MagicMock()
    image, response = mock_image()
    chart = MagicMock()
    chart.bounding_box.return_value = {"width": 300, "height": 200}
    chart.evaluate.return_value = "canvas"
    chart.screenshot.return_value = PNG + b" chart"
    page.locator.return_value.first.count.return_value = 1
    page.locator.return_value.first.locator.return_value.all.return_value = [
        image,
        chart,
    ]

    visuals = _collect_visuals(page, {IMAGE_URL: response}, MagicMock())

    assert [visual.data for visual in visuals] == [PNG, PNG + b" chart"]
    assert visuals[0].label == "A diagram"
    image.screenshot.assert_not_called()
    chart.screenshot.assert_called_once()


def test_original_image_with_private_peer_or_oversized_body_is_skipped():
    for peer, size in [
        ("127.0.0.1", len(PNG)),
        ("93.184.216.34", MAX_VISUAL_BYTES + 1),
    ]:
        element, response = mock_image()
        element.evaluate.side_effect = None
        element.evaluate.return_value = {"url": IMAGE_URL, "alt": "", "pixels": 25200}
        response.server_addr.return_value = {"ipAddress": peer, "port": 443}
        response.request.sizes.return_value = {"responseBodySize": size}

        assert (
            _original_image(
                element, {IMAGE_URL: response}, MagicMock(), MAX_VISUAL_BYTES
            )
            is None
        )
        response.body.assert_not_called()


def test_image_redirect_is_matched_to_embedded_url():
    page = MagicMock()
    _, response = mock_image()
    response.ok = True
    response.frame = page.main_frame
    response.request.resource_type = "image"
    response.request.url = IMAGE_URL
    response.request.redirected_from.url = "https://example.com/diagram"
    response.request.redirected_from.redirected_from = None
    images = {}

    _track_image(page, response, images)

    assert images["https://example.com/diagram"] is response
    assert images[IMAGE_URL] is response


@pytest.mark.parametrize(
    "address",
    ["127.0.0.1", "10.0.0.1", "::1", "169.254.169.254", "224.0.0.1", "0.0.0.0"],
)
def test_visual_policy_rejects_hosts_resolving_to_non_public_addresses(address):
    with patch(
        "socket.getaddrinfo", return_value=[(None, None, None, None, (address, 0))]
    ):
        with pytest.raises(VisualURLPolicyError, match="non-public"):
            _BrowserURLPolicy().check("https://example.com")


def test_browser_blocks_private_redirect_before_continuing_request():
    page = MagicMock()
    session = page.context.new_cdp_session.return_value
    policy = _BrowserURLPolicy()
    policy.attach(page)
    handler = session.on.call_args.args[1]
    with patch(
        "socket.getaddrinfo",
        return_value=[(None, None, None, None, ("93.184.216.34", 0))],
    ):
        handler({"requestId": "first", "request": {"url": "https://example.com"}})
        handler(
            {
                "requestId": "second",
                "redirectedRequestId": "first",
                "request": {"url": "http://127.0.0.1/"},
            }
        )

    session.send.assert_any_call("Fetch.continueRequest", {"requestId": "first"})
    session.send.assert_called_with(
        "Fetch.failRequest", {"requestId": "second", "errorReason": "BlockedByClient"}
    )
