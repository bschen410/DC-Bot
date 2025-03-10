from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import datetime, asyncio


async def getData():
    url = "https://www.mvdis.gov.tw/m3-emv-trn/exm/locations"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.locator("#licenseTypeCode").select_option("普通重型機車")
        await page.locator("#expectExamDateStr").fill("114" + datetime.date.today().strftime("%m%d"))
        await page.locator("#dmvNoLv1").select_option(value="40")
        # await page.locator("#dmvNoLv1").select_option(value="20")
        await page.locator("#dmvNo").select_option(value="46")
        # await page.locator("#dmvNo").select_option(value="25")
        await page.locator(".std_btn[onclick='query();']").click()
        await page.get_by_role("link", name="選擇場次繼續報名").click()

        content = await page.locator("#trnTable").inner_html()
        with open("test.html", "w", encoding="utf-8") as f:
            f.write(content)

        with open("test.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "lxml")
        data = []
        rows = soup.find_all("tr")
        for row in rows[1:]:
            cols = row.find_all("td")
            info = cols[1].text.strip()
            if "上午場次" in info:
                date = cols[0].text.strip()
                number = cols[2].text.strip()
                function = cols[3].text.strip()
                data.append({"date": date, "state": number, "function": function})

        # print(data)
        # print(rows[0].find_all("th"))
        result = []
        for lst in data:
            if lst["function"]:
                # print("\n==========有名額==========")
                # print(lst["date"], lst["state"], lst["function"], sep=" | ", end="\n")
                result.append(lst["date"] + " | 名額：" + lst["state"])
        print(result)
        await browser.close()
        return result
