
import os
from playwright.sync_api import sync_playwright, expect

def verify_showcase(page):
    # Get absolute path to index.html
    cwd = os.getcwd()
    file_path = f"file://{cwd}/index.html"

    print(f"Navigating to: {file_path}")
    page.goto(file_path)

    # Verify Title
    expect(page).to_have_title("Frontend Mentor Showcase | meg1502")

    # Verify Header
    expect(page.get_by_role("heading", name="Frontend Mentor Showcase")).to_be_visible()

    # Verify Grid exists
    grid = page.locator("#project-grid")
    expect(grid).to_be_visible()

    # Verify Cards - check for at least one known project
    meet_landing_page = page.get_by_role("link", name="Meet Landing Page").first
    expect(meet_landing_page).to_be_visible()

    # Wait for images to load (lazy loading might delay them, but file:// is fast)
    # We'll scroll to bottom to ensure lazy loaded images trigger
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000) # Short wait for scrolling

    # Take full page screenshot
    page.screenshot(path="verification/showcase.png", full_page=True)
    print("Screenshot saved to verification/showcase.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        try:
            verify_showcase(page)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()
