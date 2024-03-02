from playwright.sync_api import Playwright, sync_playwright, expect
import requests
import time

def run(playwright: Playwright, _headless = False) -> None:
    waitms = 0 if _headless else 1500
    _host = "https://www.irs.gov/"
    browser = playwright.chromium.launch(headless=_headless)
    context = browser.new_context()
    page = context.new_page()
    page.goto(_host)
    page.get_by_role("textbox", name="Search").click()
    page.get_by_role("textbox", name="Search").fill("form 1065 (schedule k-1)")
    page.wait_for_timeout(waitms)
    page.get_by_role("textbox", name="Search").press("Enter")
    
    # get href of Form 1065 (Schedule K-1)
    href = page.get_by_role("link", name="Form 1065 (Schedule K-1),").get_attribute("href")
    url = f"{_host}{href}"
    
    page.wait_for_timeout(waitms)
    
    # visit the page
    page.get_by_role("link", name="Form 1065 (Schedule K-1),").click()

    # download pdf content using requests library
    response = requests.get(url)
    timestr = time.strftime("%Y-%m-%d-%H:%M:%S")
    with open(f"Schedule K-1 {timestr}.pdf", "wb") as f:
        f.write(response.content)

    page.wait_for_timeout(waitms)
    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright, True)
