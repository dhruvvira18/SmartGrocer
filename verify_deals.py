import asyncio
from playwright.async_api import async_playwright
import time
import os

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # 1. Open Customer Storefront (to check initial state)
        page_customer = await browser.new_page()
        print("Navigating to customer site...")
        await page_customer.goto("http://localhost:8000/shop/mikes-groceries/index")
        await page_customer.screenshot(path="screenshots/customer_initial.png", full_page=True)

        # 2. Open Admin Portal to set a Daily Deal
        page_admin = await browser.new_page()
        print("Logging in to admin site...")
        await page_admin.goto("http://localhost:8001/login")

        # We need to fill login form
        # Assuming seed_admin.py created admin@mikesgroceries.com / admin123
        await page_admin.fill('input[name="email"]', 'admin@mikesgroceries.com')
        await page_admin.fill('input[name="password"]', 'admin123')
        await page_admin.click('button[type="submit"]')

        print("Navigating to inventory...")
        await page_admin.goto("http://localhost:8001/admin/mikes-groceries/inventory")
        await page_admin.wait_for_load_state("networkidle")

        print("Setting up daily deal...")
        # Find the first 'Manage Deal' button
        deal_buttons = await page_admin.locator('.deal-btn').all()
        if deal_buttons:
            await deal_buttons[0].click()
            # Wait for modal to be visible
            await page_admin.wait_for_selector('#deal-product-modal', state="visible")

            # Check the checkbox
            await page_admin.check('#deal-is-active')

            # Set discount to 20
            await page_admin.fill('#deal-discount', '20')

            # Submit the form
            await page_admin.click('#deal-form button[type="submit"]')
            await page_admin.wait_for_load_state("networkidle")
            print("Daily deal configured in admin.")
        else:
            print("Warning: No deal buttons found in admin inventory.")

        await page_admin.screenshot(path="screenshots/admin_inventory_after_deal.png", full_page=True)

        # 3. Verify Customer Storefront Again
        print("Reloading customer site to view deals...")
        await page_customer.reload()
        await page_customer.wait_for_load_state("networkidle")

        # Scroll to daily deals
        await page_customer.evaluate("document.getElementById('daily-deals').scrollIntoView()")
        # Wait a bit for images to load or scroll animation
        await asyncio.sleep(1)

        await page_customer.screenshot(path="screenshots/customer_with_deals.png", full_page=True)
        print("Screenshots captured in 'screenshots' directory.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
