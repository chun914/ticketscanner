#!/usr/bin/env python3
"""
TicketScanner - HK Express 機票爬蟲
使用 Playwright 自動化搜尋

安裝方法:
1. pip install playwright
2. playwright install chromium
3. python3 hkexpress_scraper.py
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def search_hkexpress():
    """搜尋 HK Express 機票"""
    
    async with async_playwright() as p:
        # 啟動瀏覽器 (headless 模式)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        try:
            print("🚀 正在開啟 HK Express 網站...")
            await page.goto('https://www.hkexpress.com/en-hk/', wait_until='networkidle')
            
            # 等 cookie banner 出現並接受
            print("🍪 處理 Cookie...")
            try:
                await page.click('button:has-text("Accept All")', timeout=5000)
            except:
                pass
            
            # 填寫搜尋表單
            print("📝 填寫搜尋資料...")
            
            # 揀出發地 (香港)
            await page.click('button:has-text("Departure")')
            await asyncio.sleep(1)
            await page.click('button:has-text("Hong Kong")')
            await asyncio.sleep(1)
            
            # 揀目的地 (大阪)
            await page.click('button:has-text("Arrival")')
            await asyncio.sleep(1)
            await page.click('button:has-text("Japan")')
            await asyncio.sleep(1)
            # 揀大阪關西
            await page.click('text=Osaka (KIX)')
            
            # 填日期
            print("📅 填寫日期...")
            await page.fill('input[placeholder="Departure Date"]', '2026-07-18')
            await page.fill('input[placeholder="Return Date"]', '2026-07-26')
            
            # 撳搜尋掣
            print("🔍 搜尋航班中...")
            await page.click('button:has-text("Find flights")')
            
            # 等結果載入
            print("⏳ 等待結果...")
            await asyncio.sleep(10)
            
            # 擷取價格資料
            print("📊 擷取資料中...")
            
            # 擷取網頁內容
            content = await page.content()
            
            # 儲存截圖
            await page.screenshot(path='hkexpress_results.png', full_page=True)
            print("✅ 截圖已儲存: hkexpress_results.png")
            
            # 嘗試擷取價格 (根據實際網頁結構調整)
            prices = await page.query_selector_all('.price')
            if prices:
                print(f"\n💰 找到 {len(prices)} 個價格:")
                for i, price in enumerate(prices[:5], 1):
                    text = await price.text_content()
                    print(f"  {i}. {text}")
            else:
                print("\n⚠️ 未能自動擷取價格，請查看截圖")
            
            # 儲存 HTML
            with open('hkexpress_page.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("📄 網頁內容已儲存: hkexpress_page.html")
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            # 出錯時都儲存截圖
            try:
                await page.screenshot(path='hkexpress_error.png')
                print("📸 錯誤截圖已儲存")
            except:
                pass
            
        finally:
            await browser.close()
            print("\n🏁 完成")

if __name__ == "__main__":
    print("=" * 60)
    print("✈️  TicketScanner - HK Express 機票搜尋")
    print("=" * 60)
    print("\n搜尋: 香港 → 大阪關西")
    print("日期: 2026-07-18 至 2026-07-26")
    print("乘客: 1 位成人\n")
    
    asyncio.run(search_hkexpress())
