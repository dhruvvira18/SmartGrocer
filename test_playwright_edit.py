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
        await page.screenshot(path="dashboard_screenshot_3.png")

        # 2. Go to Inventory
        await page.goto("http://localhost:8001/admin/mikes-groceries/inventory")
        await page.wait_for_selector('h1:has-text("Inventory Management")')

        # Edit Product Modal
        await page.click('tr:has-text("Fresher Apple") >> button:has-text("Edit")')
        await page.wait_for_selector('#edit-product-modal', state='visible')

        # Wait for value to be populated
        await page.wait_for_function('document.getElementById("edit-name").value === "Fresher Apple"')

        await page.fill('#edit-name', 'Fresher Apple')
        await page.fill('#edit-price', '130')

        await page.screenshot(path="edit_product_modal_screenshot.png")

        await page.click('#edit-product-modal button[type="submit"]')

        # Wait for the page to reload
        await page.wait_for_selector('h1:has-text("Inventory Management")')
        await page.wait_for_selector('td:has-text("Fresher Apple")')
        await page.screenshot(path="inventory_screenshot_3.png")

        await browser.close()

asyncio.run(run())
