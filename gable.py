import requests
payload = {
    'method': 'query',
    'secDateStr': '',
    'secId': '',
    'divId': '',
    'licenseTypeCode': '3',
    'expectExamDateStr': '1140310',
    '_onlyWeekend': 'on',
    'dmvNoLv1': '20',
    'dmvNo': '21'
}
html = requests.post('https://www.mvdis.gov.tw/m3-emv-trn/exm/locations', data=payload)
print(html.text)