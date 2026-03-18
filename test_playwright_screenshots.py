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
        await page.screenshot(path="dashboard_screenshot.png")

        # 2. Go to Inventory
        await page.goto("http://localhost:8001/admin/mikes-groceries/inventory")
        await page.wait_for_selector('h1:has-text("Inventory Management")')
        await page.screenshot(path="inventory_screenshot.png")

        # 3. Add Product Modal
        await page.click('button:has-text("+ Add Product")')
        await page.wait_for_selector('#add-product-modal', state='visible')
        await page.screenshot(path="add_product_modal_screenshot.png")

        await browser.close()

asyncio.run(run())
