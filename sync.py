import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# 1. إعداد جوجل شيت
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# هنقرأ مفتاح جوجل من الـ Secrets عشان الأمان
creds_dict = json.loads(os.environ['GOOGLE_CREDS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("me-live-sync").sheet1

# 2. نداء الـ API الخاص بـ Logistics
url = "https://eg.me.logisticsbackoffice.com/api/kiwi/v1/couriers/attendance/city/1?page=0&size=100"
headers = {"Authorization": f"Bearer {os.environ['API_TOKEN']}"}
response = requests.get(url, headers=headers)
data = response.json()

# 3. تحديث الشيت (مثال: مسح البيانات القديمة وكتابة الجديدة)
# هنا بنكتب المنطق اللي بيوزع الساعات على الأعمدة اللي في صورتك
# كبداية، هنطبع الداتا للتأكد
print(data)
