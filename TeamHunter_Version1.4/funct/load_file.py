"""

@author: Team Mizogg
"""
import os

BTC_TXT_FILE = "input/btc.txt"
def load_addresses():
    try:
        with open(BTC_TXT_FILE) as file:
            addfind = file.read().split()
    except FileNotFoundError:
        addfind = []

    return addfind

def count_addresses(btc_txt_file=None, last_updated=None):  
    if btc_txt_file is None:
        btc_txt_file = BTC_TXT_FILE
    addfind = load_addresses()  
    try:
        if last_updated is None:
            last_updated = os.path.getmtime(btc_txt_file)  

        last_updated_datetime = datetime.datetime.fromtimestamp(last_updated)
        now = datetime.datetime.now()
        delta = now - last_updated_datetime

        if delta < datetime.timedelta(days=1):
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60

            time_units = []

            if hours > 0:
                time_units.append(f"{hours} {'hour' if hours == 1 else 'hours'}")

            if minutes > 0:
                time_units.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")

            time_str = ', '.join(time_units)

            if time_units:
                message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{time_str}</b> old.'
            else:
                message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>less than a minute</b> old.'
        elif delta < datetime.timedelta(days=2):
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60

            time_str = f'1 day'

            if hours > 0:
                time_str += f', {hours} {"hour" if hours == 1 else "hours"}'

            if minutes > 0:
                time_str += f', {minutes} {"minute" if minutes == 1 else "minutes"}'

            message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{time_str}</b> old.'
        else:
            message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{delta.days} days</b> old.'
    except FileNotFoundError:
        message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses.'

    return message
