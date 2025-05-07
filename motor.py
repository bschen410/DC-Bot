import requests
from bs4 import BeautifulSoup
import datetime, asyncio


def get_tw_date():
    today = datetime.datetime.today()
    tw_year = today.year - 1911
    return f"{tw_year:03d}{today.month:02d}{today.day:02d}"


async def getData(opt1, opt2):
    payload = {
        "method": "query",
        "secDateStr": "",
        "secId": "",
        "divId": "",
        "licenseTypeCode": "3",
        "expectExamDateStr": get_tw_date(),
        "_onlyWeekend": "on",
        "dmvNoLv1": opt1,
        "dmvNo": opt2,
    }
    content = requests.post(
        "https://www.mvdis.gov.tw/m3-emv-trn/exm/locations", data=payload
    )
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(content.text)
    with open("test.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "lxml")
    rows = soup.select("tbody tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3 and "上午場次" in cols[1].text.strip():  # 確保有足夠的列
            date = cols[0].text.strip()
            state = cols[2].text.strip()
            data.append({"date": date, "state": state})
    # print(data)
    result = []
    for lst in data:
        if lst["state"] != "額滿":
            result.append(lst["date"] + " | 名額：" + lst["state"])
    # print(result)
    if result:
        loc = soup.select_one(f'option[value="{opt2}"]').text.strip()
        print(f'FROM motor.py --> result: {result} at {loc}')
        return result, loc
    else:
        print(f'FROM motor.py --> result not found')
        return result, ""

result, loc = asyncio.run(getData(20, 26))
print(result)
