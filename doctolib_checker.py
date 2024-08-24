import urllib
import json
import time
import datetime
import http.client
import urllib.request

# load config.json
config = json.load(open("config.json"))

# yyyy-mm-dd
limit_date = config["limit_date"]
start_date = config["start_date"]

# max number of days in advance
limit = config["limit"]

# the url to fetch the data from. The start_date and limit will be replaced by the actual values
url = config["url"] % {"start_date": start_date, "limit": limit}


def send_pushover_notification(message):
    """Send a pushover notification"""

    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(
            {
                "token": config["pushover_credentials"]["api_token"],
                "user": config["pushover_credentials"]["user_key"],
                "message": message,
            }
        ),
        {"Content-type": "application/x-www-form-urlencoded"},
    )
    conn.getresponse()


def get_closest_available_time_slot(json_data):
    """Get the closest available time slot"""

    availabilities = json_data["availabilities"]
    closest_slot = ""

    for slot in availabilities:
        if slot["slots"] == []:
            continue

        if datetime.datetime.strptime(
            slot["date"][:10], "%Y-%m-%d"
        ) <= datetime.datetime.strptime(limit_date, "%Y-%m-%d"):
            closest_slot = slot["slots"][0]
            break

    return closest_slot


def format_string_to_date(date):
    """Get a proper date string
    Input will be something like "2024-11-07T11:20:00.000+01:00"
    Output will be something like "2024-11-07 11:20:00"
    """
    return str(datetime.datetime.strptime(date[:-10], "%Y-%m-%dT%H:%M:%S"))


def main():
    print("Starting...")
    send_pushover_notification(
        f"Doctolib script started. \nLooking for appointments up to {limit_date}"
    )

    while config["run_in_loop"]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Magic Browser"})
            con = urllib.request.urlopen(req)
            json_data = json.loads(con.read())

            # there is a free slot in the next <limit> days
            if json_data["total"] > 0:
                closest_slot = get_closest_available_time_slot(json_data)
                if closest_slot != "":
                    send_pushover_notification(
                        f'New appointment available on Doctolib within the next {limit} days! \nNumber of available appointments: {json_data["total"]} \nEarliest appointment: {format_string_to_date(closest_slot)}'
                    )

            # if next available slot is before the limit date
            elif datetime.datetime.strptime(
                json_data["next_slot"][:10], "%Y-%m-%d"
            ) <= datetime.datetime.strptime(limit_date, "%Y-%m-%d"):
                send_pushover_notification(
                    f'New appointment available on Doctolib within your limit time! \nEarliest appointment: {format_string_to_date(json_data["next_slot"])}'
                )

            # send an alive message at <hour_of_alive_check> o'clock and minute 0 everyday if <alive_check> is True
            if (
                config["alive_check"]
                and datetime.datetime.now().hour == config["hour_of_alive_check"]
                and datetime.datetime.now().minute == 0
            ):
                send_pushover_notification(
                    f"Doctolib script is still running. \nLooking for appointments up to {limit_date}"
                )
            time.sleep(config["interval_in_seconds"])

        except Exception as e:
            send_pushover_notification(
                f"An error occured while running the Doctolib script: {e}"
            )


if __name__ == "__main__":
    main()
