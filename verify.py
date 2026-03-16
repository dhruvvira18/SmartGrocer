import asyncio
from playwright.async_api import async_playwright
import uvicorn
import multiprocessing
import time
from customer_site.main import app as customer_app
from admin_site.main import app as admin_app

def run_customer():
    uvicorn.run(customer_app, host="127.0.0.1", port=8000, log_level="warning")

def run_admin():
    uvicorn.run(admin_app, host="127.0.0.1", port=8001, log_level="warning")

async def main():
    p1 = multiprocessing.Process(target=run_customer)
    p2 = multiprocessing.Process(target=run_admin)
    p1.start()
    p2.start()

    time.sleep(3) # Wait for servers to start

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Check Customer Login
        await page.goto("http://127.0.0.1:8000/shop/mikes-groceries/login")
        await page.screenshot(path="customer_login_updated.png")

        # Check Admin Login
        await page.goto("http://127.0.0.1:8001/login")
        await page.screenshot(path="admin_login_updated.png")

        await browser.close()

    p1.terminate()
    p2.terminate()
    p1.join()
    p2.join()

if __name__ == "__main__":
    asyncio.run(main())
