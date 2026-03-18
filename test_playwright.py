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

        # 2. Go to Inventory
        await page.goto("http://localhost:8001/admin/mikes-groceries/inventory")
        await page.wait_for_selector('h1:has-text("Inventory Management")')

        # 3. Add Product
        await page.click('button:has-text("+ Add Product")')
        await page.wait_for_selector('#add-product-modal', state='visible')

        await page.fill('input[name="name"]', 'Giant Watermelon')
        await page.fill('input[name="price"]', '25')
        await page.fill('input[name="stock"]', '10')
        await page.select_option('select[name="category"]', 'Produce')
        await page.fill('input[name="image_url"]', 'https://img.icons8.com/color/96/watermelon.png')

        await page.click('#add-product-modal button[type="submit"]')

        # Wait for product to appear in the table
        await page.wait_for_selector('td:has-text("Giant Watermelon")')
        await page.screenshot(path="admin_inventory.png")
        print("Product added successfully in admin site.")

        # 4. Verify on Shopper Site
        await page.goto("http://localhost:8000/shop/mikes-groceries/index")
        await page.wait_for_selector('div.product-card h3:has-text("Giant Watermelon")')
        await page.screenshot(path="shopper_index.png")
        print("Product verified successfully in shopper site.")

        await browser.close()

asyncio.run(run())
