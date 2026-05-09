import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# 1. إعداد جوجل شيت
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ['GOOGLE_CREDS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("me-live-sync").sheet1

# 2. سحب البيانات من الـ API
url = "https://eg.me.logisticsbackoffice.com/api/kiwi/v1/couriers/attendance/city/1?page=0&size=100&sort_by=break_time&sort_direction=desc"
headers = {"Authorization": f"Bearer {os.environ['API_TOKEN']}"}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if 'data' in data and 'items' in data['data']:
        riders = data['data']['items']
        rows_to_update = []
        
        for rider in riders:
            # سحب البيانات بناءً على الصورة الجديدة
            rider_id = rider.get('rider_id', '')
            name = rider.get('name', '')
            zone = rider.get('zone_name', '')
            phone = rider.get('phone', '')
            
            # حقول الوقت والشغل (بناءً على واجهة الـ Dashboard)
            time_worked = rider.get('worked_time', '00:00')  # الساعات اللي اشتغلها
            deliveries = rider.get('deliveries_count', 0)     # عدد التوصيلات
            total_break = rider.get('total_break_time', '00:00') # إجمالي البريك
            status = rider.get('status', 'Unknown')          # الحالة (Working/Break)

            # ترتيب الصف ليطابق أعمدة الشيت بتاعك
            # [ID, Name, Zone, Phone, الساعات, التوصيلات, الحالة]
            row = [rider_id, name, zone, phone, time_worked, deliveries, status]
            rows_to_update.append(row)
        
        # 3. تحديث الشيت
        # بنمسح القديم ونحط الجديد من الصف التاني
        sheet.delete_rows(2, 500)
        sheet.insert_rows(rows_to_update, 2)
        
        print(f"✅ تم تحديث {len(rows_to_update)} طيار بنجاح مع ساعات العمل!")
    else:
        print("⚠️ الـ API مبعتش بيانات الحقول المتوقعة.")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
