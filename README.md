# doctolib-checker
This little improvised python script is for anyone who books their doctor's appointment via [Doctolib](https://www.doctolib.de). Sometimes the next appointment available is several months away and you do not want to wait that long for your doctor's visit. But sometimes other patients cancel their appointments for various reasons and a free slot appears. This script automatically checks for these shortterm available appointments and notifies you on your pc/smartphone/tablet via [Pushover](https://pushover.net/) when a there is a free slot before a specified date available. 

# Setup
This script does not need any external python packages and has been tested with Python 3.11.9
However, you will need to do some changes in the `config.json` for this script to work:
- The variables `run_in_loop` and `interval_in_seconds` are used in case you want to run this script in a `while`-loop. In this case `run_in_loop` should be `true`. `interval_in_seconds` specifies the interval in second the script will be executed. Alternatively, you can run this script via crontab in this case you should put `"run_in_loop": false`
- `alive_check` and `hour_of_alive_check` are used to send a notification at one specific hour in the day in order to signal to you that the script is still running. So if you want this "alive check" to notify you everyday at 15 o'clock just put `"hour_of_alive_check": 15`

- `limit_date` is the latest date you want your appointment at, in the format of yyyy-mm-dd
- `start_date` is the date at which the script starts to look for appointments, also in the format of yyyy-mm-dd. If this date is in the past the current date will be chosen

- `limit` corresponds to the amount of days the script will check for appointments ahead of the `start_date`. Min. value is 2 and max. value is 15. 

- `url` is the Doctolib URL of your appointment overview. This one is a bit complicated but bear with me. There are better ways to this, I know, but this script is improvised :)
  - first of all you go to your preferred doctor and click through the menus to book an appointment until you can choose specific days and times for your appointment.
  - Then you go to the network monitor (Ctrl + Shift + E) and reload the page
  - Once you have done that you click on the last GET-Request and look to the right side of your window
  - Here you have to copy the URL of the GET-Request and paste it into the config file.
  - Then you prepare the link for formatting by replacing the part that looks like `start_date=2024-01-01&limit=15` with `start_date=%(start_date)s&limit=%(limit)s`.
- `pushover_credentials` are the credentials needed in order to send push notifications to your device in case a free appointment has been found. Take a look at the [Pushover API Documentation](https://pushover.net/api) to know what's what.

That was the setup. It is not as complicated as it looks ;) Have fun!