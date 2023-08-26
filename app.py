import os
import requests
from linebot import (
    LineBotApi,
    WebhookHandler
)
from linebot.models import TextSendMessage, FlexSendMessage

# ข้อมูลการเข้าถึง API Line
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

# ข้อมูลการเข้าถึง API football-data.org
FOOTBALL_DATA_API_KEY = os.environ['FOOTBALL_DATA_API_KEY']

# ฟังก์ชันสำหรับรับข้อความจากผู้ใช้
def handle_message(event):
    # ตรวจสอบว่าผู้ใช้ส่งข้อความอะไรมา
    if event.type == 'message':
        # ตรวจสอบว่าผู้ใช้ส่งข้อความ /ตารางบอลวันนี้
        if event.message.text == '/ตารางบอลวันนี้':
            # ดึงข้อมูลตารางบอลวันนี้จาก API football-data.org
            url = 'https://api.football-data.org/v2/matches/?date=today&competitions=all&status=SCHEDULED'
            headers = {'X-Auth-Token': FOOTBALL_DATA_API_KEY}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # แปลงข้อมูล JSON เป็นรายการ
                matches = response.json()['matches']

                # สร้าง Flex Message สำหรับแสดงตารางบอล
                items = []
                for match in matches:
                    items.append({
                        'type': 'text',
                        'text': f'{match["utcDate"]} {match["homeTeamName"]} vs {match["awayTeamName"]}'
                    })
                flex_message = FlexSendMessage(
                    alt_text='ตารางบอลวันนี้',
                    template_type='carousel',
                    contents=[
                        {
                            'type': 'text',
                            'text': 'ตารางบอลวันนี้'
                        },
                        {
                            'type': 'carousel',
                            'contents': items
                        }
                    ]
                )

                # ส่งข้อความ Flex Message กลับไปยังผู้ใช้
                line_bot_api.reply_message(event.reply_token, flex_message)

# ฟังก์ชันหลักสำหรับรับข้อความจากผู้ใช้
def main():
    # เริ่มต้นใช้งาน LineBot
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

    # ฟังก์ชันสำหรับรับข้อความจากผู้ใช้
    line_bot_api.webhook(
        WebhookHandler(os.environ['LINE_CHANNEL_SECRET']),
        on_message=handle_message
    )

if __name__ == "__main__":
    main()
