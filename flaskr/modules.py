import io
import calendar
import win32com.client
import pythoncom
from datetime import datetime
from PIL import Image

# 160*160
def image_resize(img):
    img = Image.open(io.BytesIO(img))
    img.thumbnail((160, 160), Image.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='JPEG')
    return output.getvalue()

def make_id_to_obj_dict(objects):
    new_dict = {}
    for obj in objects:
        new_dict[obj.id] = obj
    return new_dict

def reformat_number(num):
    if len(str(num)) > 1:
        num = str(num)
    else:
        num = '0' + str(num)
    return num

def make_date_label(year, month, day):
    week_day = ['月', '火', '水', '木', '金', '土', '日']
    target_date = datetime(year, month, day)
    date_label = target_date.strftime('%Y年%m月%d日') + f'({week_day[target_date.weekday()]})'
    return date_label
    
def make_now_time_lable():
    now =datetime.now()
    hour = reformat_number(now.hour)
    minute = reformat_number(now.minute)
    now_time = f'{hour}:{minute}'
    return now_time

def make_monthly_calender(year, month):
    week_day = ['月', '火', '水', '木', '金', '土', '日']
    cal = calendar.monthcalendar(year, month)
    target_month = {'year': year, 'month': month, 'day': {}}
    for week in cal:
        week_day_count = 0
        for day in week:
            if not day is 0:
                target_month['day'][day] = week_day[week_day_count]
            week_day_count += 1
    return target_month