import pytest
from playwright.sync_api import sync_playwright, Page

BASE_URL="https://sauce-demo.myshopify.com/"

EMAIL="bibaxip442@art2mart.com"
PASSWORD="662nz68qM@Xpwgb"

@pytest.fixture(scope="session")
def page_context():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        context=browser.new_context()
        context.tracing.start(snapshots=True,screenshots=True,sources=True)
        page=context.new_page()
        yield page 
        context.tracing.stop(path="globalsqa.zip")

@pytest.fixture()
def test_logged(page_context: Page):
    page=page_context
    page.goto(BASE_URL)

    page.get_by_role("link", name="Log In").click()
    page.locator("input[id='customer_email']").fill(EMAIL)
    page.locator("input[id='customer_password']").fill(PASSWORD)
    page.locator("input[value='Sign In']").click()
    page.get_by_text("My Account").is_visible()
    return page

def test_navigation(page_context: Page):
    page=page_context
    page.goto(BASE_URL)

    link=["Home","Catalog","Blog","Wish list","Log In","Refer a friend","Sign up"]
    for l in link:
        page.get_by_role("link", name=l).click()
        page.wait_for_timeout(1000)

def test_login(page_context: Page):
    page=page_context
    page.goto(BASE_URL)
    page.get_by_role("link", name="Log In").click()
    page.locator("input[id='customer_email']").fill(EMAIL)
    page.locator("input[id='customer_password']").fill(PASSWORD)
    page.locator("input[value='Sign In']").click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name="My Account").click()

def test_search_product(test_logged: Page):
    page=test_logged
    page.go_back()
    page.get_by_placeholder("Search").fill("shirt")
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")

