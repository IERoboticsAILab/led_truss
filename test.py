import asyncio
import argparse
from typing import Optional, Callable


async def poll_heart_rate(
    url: str = "https://app.hyperate.io/74524/",
    interval_sec: float = 1.0,
    duration_sec: Optional[float] = None,
    on_value: Optional[Callable[[int], None]] = None,
) -> None:
    """Continuously poll heart rate from a Hyperate share URL using a headless browser.

    Notes:
    - The Hyperate widget is a LiveView app; values update via WebSocket. A simple HTTP GET won't reflect live data.
    - This function uses Playwright to render the page and read the `.heartrate` element repeatedly.
    """
    try:
        from playwright.async_api import async_playwright
    except Exception as e:
        raise RuntimeError(
            "Playwright is required. Install with: pip install playwright and then run: python -m playwright install --with-deps"
        ) from e

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        # Wait for the heart rate element to appear
        await page.wait_for_selector(".heartrate", timeout=20000)

        loop = asyncio.get_running_loop()
        deadline = (loop.time() + duration_sec) if duration_sec is not None else float("inf")

        while loop.time() < deadline:
            try:
                text = await page.inner_text(".heartrate")
                digits = "".join(ch for ch in text if ch.isdigit())
                value = int(digits) if digits else 0
                if on_value is not None:
                    on_value(value)
                else:
                    print(value, flush=True)
            except Exception as read_err:
                print(f"read_error: {read_err}", flush=True)
            await asyncio.sleep(interval_sec)

        await browser.close()


def main() -> None:
    asyncio.run(poll_heart_rate())


if __name__ == "__main__":
    main()