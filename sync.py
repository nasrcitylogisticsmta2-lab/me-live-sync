import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from datetime import datetime

# 1. إعداد جوجل شيت
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ['GOOGLE_CREDS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("me-live-sync").sheet1

# 2. سحب البيانات من الـ API (الرابط اللي في صورتك)
url = "https://eg.me.logisticsbackoffice.com/api/kiwi/v1/couriers/attendance/city/1?page=0&size=100&sort_by=break_time&sort_direction=desc"
headers = {"Authorization": f"Bearer {os.environ['API_TOKEN']}"}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if 'data' in data and 'items' in data['data']:
        riders = data['data']['items']
        rows_to_update = []
        
        for rider in riders:
            # استخراج البيانات - ركز في الأسماء دي لازم تطابق اللي في الـ Network عندك
            rider_id = rider.get('rider_id', '')
            name = rider.get('name', '')
            zone = rider.get('zone_name', '')
            phone = rider.get('phone', '')
            
            # استخراج الساعات (لو الحقل اسمه مختلف في الـ Response قولي)
            # بنفترض إن الساعات موجودة في حقل اسمه 'total_hours'
            hours = rider.get('total_hours', '0') 
            status = rider.get('status', 'مش مختار')

            # ترتيب الصف: ID, Name, Zone, Phone, Hours, Status
            row = [rider_id, name, zone, phone, hours, status]
            rows_to_update.append(row)
        
        # 3. مسح البيانات القديمة وتحديث الشيت
        # بيمسح من الصف الثاني (عشان يسيب العناوين)
        sheet.delete_rows(2, 500)
        sheet.insert_rows(rows_to_update, 2)
        
        print(f"تم تحديث بيانات {len(rows_to_update)} طيار بالساعات!")
    else:
        print("الـ API مبعتش داتا، تأكد من الـ Token")

except Exception as e:
    print(f"Error: {e}")
