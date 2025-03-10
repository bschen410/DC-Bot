import datetime

today = datetime.date.today()
print(today.strftime("%Y%m%d"))
print("114" + datetime.date.today().strftime("%m%d"))
