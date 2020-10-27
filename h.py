import requests
import re
import gspread
import pytz
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep


def get_spread_sheet():
    cred = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": "holodule-db",
        "private_key_id": "f513ed1bfffaedd588e99edcfc713565b91c8ffc",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDCpkqc4evZEoke"
                       "\n86a3mk361HonNTM8S4w64vW8d0rGSpRf1hKoY1TUNGwNyY+zbDZ8+gPHU7a28ppA\nLFtJ1iu"
                       "+rvr3LUC6CrCCSkdejz5fi/B9/FUT35eAhwb45541z3vXPBh+le7ybJzx\nm24oDxze4wx0M5C9kJxS"
                       "/xCeRepkckU4FrGh3OrKxmffuZyiVrIKgVxms7iRU8kI\nFstXef0c1p"
                       "+WbqKvQdMdZAUrBucgdH3mwU3opA3YPNk027v8IoYWPt6SuPoQXHrR\n94w3td0dlPEUrJ5QAMZTJdHaqYU3c1coXrtJo"
                       "/pVio3G139tYI++i9yOY3UVoQEu\nY058VayPAgMBAAECggEAG+uPa0ZqtpXWjlaDtPVQtyhwJxyV71Gk2TOB7RktZBkB"
                       "\nhGeoAHhTDCdC0o11a9abUDzqetZysHZHEupp48LxPmZKAFeA3861t9KgvxsL5tej\nVObzayjYyepUYTKT"
                       "+oL68AoiN1IZVrOmpW9Wky9rxDrMKATXf6F1EuCcSR+dOe/8\nFlgIbVDmJBoUTEIsAb3ZZxbaLpFihLMfzBzLsn"
                       "/j038DOYWzAxEHiEHMZ9OsV9Dl\nsTJwU3M0oftoWqeL/89gmC2wTE7/W98+suOZWx2UKoRpXbdrY5SG5Xj57j7k4JpA"
                       "\n9kzIZ0zWmRcB00QAJMwbr+TLbJE/ECxLJwigoD1F4QKBgQDlhcKAOAEhT8mWg6Ky\nHb/ajl8KOON5rP058N"
                       "/se1BBs9EqdXQHV03uRrju6n9phQJrX9iaMnue9bduuWJA\nHcnE8jXZog4I0KhcOrrnxI1"
                       "/CZfkASRKN11tpkZjrg3xwWub9QVQs+air/XWYbIy\nTufQIGvHvXGApMxAKwLe6"
                       "/tPIQKBgQDZGqrTfg5mZQS7Ssi14TKUvU7vKdXvV95X\nOu1m9eG/WTQdVHpTpYKQEb2L00wT"
                       "/99zrTw8wzqN3tR9gKpA1QlYyLB8nSMn9nHx\nPq6XKwiwNX7+nL/yvV7NdlfNEuQsvWO"
                       "/mOEcXuL3i4C635oQPv6Adxn8ddxwAsZB"
                       "\n4e1tntD1rwKBgQDia2irahQbU4VvGN6HzXc02JwDDonAv5ly7h9IP4G1vvjJZOKY"
                       "\nV1TGiTfoYKZeZtszJ3Ma8lAnSQiyjujQjVI9Gh9rWUV1Brn/eeRlvO1E9CbFwyaU\nnDdrcssfjFWvNvq7"
                       "+CNNMJuFxAXFfcz3egWOuFz6xvTQTkI7zvJfDPZ2YQKBgQCd\nt6vF/NuFM3nefhOVXcYbG"
                       "/PN9vx95b2WbS6uD44yLiGX9Rjwz1osQ1cJzzSDiuzP\n4lfSZJmTGwAPNHt6ockqgJEF1joF/BkGgtze4Nps+FALs+AV"
                       "/dBzPrfGOSUeA3AF\nbpCKxbvozaV1HJ+Vkc3dkaiFKTI9BSb2EaUkb62p7QKBgQCW4mzJBWU73Ab3FyS6"
                       "\nmAYEEv74sBwNRPu3u5W/gS2SjEI0d4JbUWM9Rx860ReHc2AD1P/nAfMhuWYvf4bA\ntYqj9UaMh/a6VjMD"
                       "+NogJqtSkhtSvzemXavEDKhoDFK4t78mxMT+bYg55oFr0YL4\nmPMlSlOApt7ebfApToxM5o/T9w==\n-----END "
                       "PRIVATE KEY-----\n",
        "client_email": "holodule-db-editor@holodule-db.iam.gserviceaccount.com",
        "client_id": "102798647501414411164",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/holodule-db-editor%40holodule-db"
                                ".iam.gserviceaccount.com "
    }, scopes=gspread.auth.DEFAULT_SCOPES)
    client = gspread.authorize(cred)
    return client.open("holodule_data").sheet1


g_sheet = get_spread_sheet()
g_records = g_sheet.get_all_records()


def req_get(url: str, **kwargs):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"}
    return requests.get(url, headers=headers, **kwargs)


def get_raw_data():
    cookies = {"timezone": "Asia/Jakarta"}
    return req_get("https://schedule.hololive.tv/", cookies=cookies)


def get_youtube_title(youtube_url: str):
    yt = req_get(f"https://www.youtube.com/oembed?url={youtube_url}&format=json").json()
    return yt["title"]


def add_to_database(row: list):
    g_sheet.append_row(row)


def parse_holodule():
    bs = BeautifulSoup(get_raw_data().text, "html.parser")
    schedules = bs.find_all("div", class_="col-6 col-sm-4 col-md-3")
    ret = list()

    for schedule in schedules:
        live_date = re.sub(r'\s+', ' ', schedule.find_previous("div", class_="holodule navbar-text").text.strip())
        live_time = schedule.find("div", class_="col-5 col-sm-5 col-md-5 text-left datetime").text.strip()

        jkt_current_time = datetime.now(tz=pytz.timezone("Asia/Jakarta"))
        live_at = datetime.strptime(f"{live_date.split()[0]}/{jkt_current_time.year} {live_time}",
                                    "%m/%d/%Y %H:%M").astimezone(tz=pytz.timezone("Asia/Jakarta"))
        if jkt_current_time > live_at:
            continue

        tomorrow = jkt_current_time + timedelta(days=1)

        if live_at >= datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0, 0).astimezone(
                tz=pytz.timezone("Asia/Jakarta")):
            continue

        member_name = schedule.find("div", class_="col text-right name").text.strip()
        youtube_link = schedule.find("a", class_="thumbnail")["href"]
        youtube_title = get_youtube_title(youtube_link)

        should_add_new_db_entry = True
        should_edit_existing_telegram_message = False
        for row, record in enumerate(g_records):
            if record["Youtube Link"] == youtube_link:
                should_add_new_db_entry = False
                old_live_date = record["Live Date"]
                old_live_time = record["Live Time"]
                old_yt_title = record["Youtube Title"]
                data_changed = False

                if old_live_date != live_date:
                    g_sheet.update_cell(row + 2, 1, live_date)
                    live_date = f"<s>{old_live_date}</s> -> {live_date}"
                    data_changed = True

                if old_live_time != live_time:
                    g_sheet.update_cell(row + 2, 2, f"'{live_time}")
                    live_time = f"<s>{old_live_time}</s> -> {live_time}"
                    data_changed = True

                if old_yt_title != youtube_title:
                    g_sheet.update_cell(row + 2, 5, youtube_title)
                    data_changed = True

                if data_changed:
                    member_name = f"[UPDATE]\n\n{member_name}"

                should_edit_existing_telegram_message = data_changed

                break

            else:
                should_add_new_db_entry = True

        ret.append({
            "Live Date": live_date,
            "Live Time": live_time,
            "Member Name": member_name,
            "Youtube Link": youtube_link,
            "Youtube Title": youtube_title,
            "Should Edit Existing Telegram Message": should_edit_existing_telegram_message
        })

        if should_add_new_db_entry:
            last = ret[-1]
            add_to_database([last['Live Date'], last['Live Time'], last['Member Name'],
                             last['Youtube Link'], last['Youtube Title']])

    return ret


def send_info(message: str, mode: str = 'w', message_id: int = -1):
    TOKEN = "1243277966:AAHBh9eRkNEcK4CuODijw5XWmzY8CMuKK-Q"
    mode = mode.lower()

    if mode == 'w':  # write new message
        payload = {
            "parse_mode": "html",
            "chat_id": "@holodule",
            "text": message,
        }
        api_method = "sendMessage"

    elif mode == 'e':  # edit existing message
        if message_id == -1:
            raise Exception("Message ID is needed for editing message!")

        payload = {
            "parse_mode": "html",
            "chat_id": "@holodule",
            "text": message,
            "message_id": message_id
        }
        api_method = "editMessageText"

    else:
        raise Exception("Invalid send info mode!")

    return requests.post(f"https://api.telegram.org/bot{TOKEN}/{api_method}", data=payload)


def main():
    global g_records

    holodules = parse_holodule()
    g_records = g_sheet.get_all_records()

    sent_message_counter = 0
    for i, holodule in enumerate(holodules):
        message_format = f"{holodule['Member Name']} @ {holodule['Live Date']} | {holodule['Live Time']} " \
                         f"(GMT+07:00)\n\n<a href=\"{holodule['Youtube Link']}\">{holodule['Youtube Title']}</a>"

        for row, record in enumerate(g_records):
            if record["Youtube Link"] == holodule["Youtube Link"]:
                telegram_message_id = record["Telegram Chat ID"]

                if telegram_message_id == '':
                    if (sent_message_counter + 1) % 20 == 0:
                        sleep(60.1)
                        
                    telegram_message_id = send_info(message_format).json()["result"]["message_id"]
                    sent_message_counter += 1
                    g_sheet.update_cell(row + 2, 6, telegram_message_id)
                    sleep(1.1)
                    break
                else:
                    if holodule["Should Edit Existing Telegram Message"]:
                        send_info(message_format, 'e', telegram_message_id)
                    break


if __name__ == '__main__':
    main()
