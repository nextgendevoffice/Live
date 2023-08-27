from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from db import get_user_leagues,update_user_leagues
from api import get_today_matches,get_league_table,get_leagues

# Initialize LINE SDK
line_bot_api = LineBotApi('8tR6Z7GkmuSg0Xwj1DGPkeBiSWKiP+D29jNlTejUh9hKVRaeWySDkdTD7D7IlIyHS2KTpq9zj92/jPT73Yo5l+mXH50HhqKQ3uCbF2Q9f9D4JRV14HxjnUP9OzGlPQlvk0Cs06+Yk5sa/e6ygJ9NJQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('91ab717cdd0910e3e593de39189c117b')

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text

    if message_text == "/สมัคร":
        leagues = get_leagues()
        league_list = "\n".join([f"{league['code']} - {league['name']}" for league in leagues['competitions']])
        reply_message = f"กรุณาเลือกลีคที่คุณต้องการติดตาม:\n{league_list}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

    # ... Handle other commands similarly
    elif message_text == "/ตารางแข่ง":
        user_leagues = get_user_leagues(user_id)
        if not user_leagues:
            reply_message = "You are not following any leagues yet."
        else:
            # Fetching today's matches for the leagues the user is following
            matches = []
            for league in user_leagues:
                league_matches = get_today_matches(league)
                for match in league_matches["matches"]:
                    match_info = f"{match['homeTeam']['name']} vs {match['awayTeam']['name']} at {match['utcDate']}"
                    matches.append(match_info)
            reply_message = "\n".join(matches) if matches else "No matches scheduled for today in the leagues you're following."
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

    elif message_text == "/ตารางคะแนน":
        user_leagues = get_user_leagues(user_id)
        if not user_leagues:
            reply_message = "You are not following any leagues yet."
        else:
            # Fetching the standings for the leagues the user is following
            standings = []
            for league in user_leagues:
                league_table = get_league_table(league)
                for team in league_table["standings"][0]["table"]:  # Assuming we're fetching the overall standings (type: TOTAL)
                    team_info = f"{team['position']}. {team['team']['name']} - {team['points']} pts"
                    standings.append(team_info)
            reply_message = "\n".join(standings)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        
    elif message_text.startswith("/ติดตาม "):  # For example, command to follow a league could be "/follow EPL"
        league_code = message_text.split(" ")[1]
        user_leagues = get_user_leagues(user_id)
        if league_code not in user_leagues:
            user_leagues.append(league_code)
            update_user_leagues(user_id, user_leagues)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"You are now following {league_code}.")
            )

# ... other command implementations ...

if __name__ == "__main__":
    app.run()
