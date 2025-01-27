import requests
from datetime import datetime, timedelta 

def get_schedule(start_date, end_date, group):
    start_date = start_date.strftime('%d.%m.%Y')
    end_date = end_date.strftime('%d.%m.%Y')
    schedule = requests.get(f"https://www.usue.ru/schedule/?t=0&action=show&startDate={start_date}&endDate={end_date}&group={group}")
    schedule = schedule.json()
    return schedule

def make_it_pretty(start_date, end_date, group):
    schedule = get_schedule(start_date, end_date, group)
    output = []
    for day in schedule:
        day_text = f"<b><u>{day['weekDay']} {day['date']}</u></b>"
        day["pairs"] = day["pairs"][:8]
        day_text += '<pre>'
        for pair in day["pairs"]:
            if pair["schedulePairs"]:
                if pair['schedulePairs'][0]['comm']:
                    day_text += f"\n{pair['schedulePairs'][0]['comm'][:-5]} {pair['N']} пара:\n"
                else:
                    day_text += f"\n{pair['time']} {pair['N']} пара:\n"
            else:
                day_text += f"\n{pair['time']} {pair['N']} пара:\n"
            for sched in pair["schedulePairs"]:
                day_text += f"{sched['subject']} {sched['aud']} {sched['group'][9:]}\n"
        day_text += '</pre>\n'
        output.append(day_text)
    text_out = "\n".join(output)
    return text_out
