from linebot import LineBotApi, WebhookHandler

def handle_message(event):
    pass

line_bot_api = LineBotApi("8tR6Z7GkmuSg0Xwj1DGPkeBiSWKiP+D29jNlTejUh9hKVRaeWySDkdTD7D7IlIyHS2KTpq9zj92/jPT73Yo5l+mXH50HhqKQ3uCbF2Q9f9D4JRV14HxjnUP9OzGlPQlvk0Cs06+Yk5sa/e6ygJ9NJQdB04t89/1O/w1cDnyilFU=")
webhook_handler = WebhookHandler("08c1695f0b7ecc5aba7ba36c10d0f281")

@webhook_handler.add(event='message')
def handle_message(event):
    print(event)

@webhook_handler.add(event='message')
def handle_message(event):
    if event.message.text == "/ผลบอลวันนี้":
        completed_matches = get_completed_matches()
        notification_message = ""
        for completed_match in completed_matches:
            home_team = completed_match["homeTeam"]["name"]
            away_team = completed_match["awayTeam"]["name"]
            score = completed_match["score"]["fullTime"]
            notification_message += f"[ผลบอลวันนี้] {home_team} {score['homeScore']}-{score['awayScore']} {away_team}\n"
        line_bot_api.push_message(event.source.user_id, notification_message)
        
webhook_handler.run()
