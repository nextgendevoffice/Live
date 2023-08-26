import requests
import json
from linebot import LineBotApi, WebhookHandler

def get_live_scores():
    url = "https://api.football-data.org/v2/matches/live"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        raise Exception("Error getting live scores")

def send_line_notification(data):
    channel_access_token = "YOUR_CHANNEL_ACCESS_TOKEN"
    line_bot_api = LineBotApi(channel_access_token)

    for live_score in data:
        home_team = live_score["homeTeam"]["name"]
        away_team = live_score["awayTeam"]["name"]
        score = live_score["score"]["fullTime"]
        time = live_score["matchStats"]["elapsed"]
        goals = live_score["goals"]
        shots = live_score["shots"]
        corners = live_score["corners"]

        if score["homeScore"] != score["awayScore"]:
            notification_message = f"[แจ้งเตือนผลบอลสด] {home_team} {score['homeScore']}-{score['awayScore']} {away_team} [นาทีที่ {time}]\n\n"
            notification_message += f"ประตู\n"
            for goal in goals:
                if goal["team"] == "home":
                    goal_team = home_team
                elif goal["team"] == "away":
                    goal_team = away_team
                else:
                    goal_team = "UNKNOWN"
                notification_message += f"* {goal_time}: {goal_team} {goal['scorer']}\n"
            notification_message += f"ยิงประตู\n"
            for shot in shots:
                if shot["team"] == "home":
                    shot_team = home_team
                elif shot["team"] == "away":
                    shot_team = away_team
                else:
                    shot_team = "UNKNOWN"
                notification_message += f"* {shot_time}: {shot_team} {shot['location']}\n"
            notification_message += f"ลูกเตะมุม\n"
            for corner in corners:
                if corner["team"] == "home":
                    corner_team = home_team
                elif corner["team"] == "away":
                    corner_team = away_team
                else:
                    corner_team = "UNKNOWN"
                notification_message += f"* {corner_time}: {corner_team}\n"
            line_bot_api.push_message(live_score["id"], notification_message)

def get_completed_matches():
    url = "https://api.football-data.org/v2/matches/completed"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        raise Exception("Error getting completed matches")

if __name__ == "__main__":
    live_scores = get_live_scores()
    send_line_notification(live_scores)
