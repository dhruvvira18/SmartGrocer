import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 1. Login as Admin
        await page.goto("http://localhost:8001/login")
        await page.fill('input[name="email"]', 'mike@smartgrocer.com')
        await page.fill('input[name="password"]', 'MikesGroceries1')
        await page.click('button[type="submit"]')

        # Dashboard
        await page.wait_for_selector('h1:has-text("Inventory Control Center")')
        await page.screenshot(path="dashboard_screenshot_2.png")

        # 2. Go to Inventory
        await page.goto("http://localhost:8001/admin/mikes-groceries/inventory")
        await page.wait_for_selector('h1:has-text("Inventory Management")')

        # Get the stock before
        stock_element = await page.wait_for_selector('tr:has-text("Fresh Apple") >> span')
        stock_text_before = await stock_element.inner_text()
        print(f"Stock before: {stock_text_before}")

        # Add stock
        await page.fill('tr:has-text("Fresh Apple") >> input[name="amount"]', '5')
        await page.click('tr:has-text("Fresh Apple") >> button:has-text("+ Add Stock")')

        # Wait for the page to reload
        await page.wait_for_selector('h1:has-text("Inventory Management")')
        stock_element = await page.wait_for_selector('tr:has-text("Fresh Apple") >> span')
        stock_text_after = await stock_element.inner_text()
        print(f"Stock after: {stock_text_after}")

        await page.screenshot(path="inventory_screenshot_2.png")

        await browser.close()

asyncio.run(run())
