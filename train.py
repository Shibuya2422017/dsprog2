import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

urls = {
    "平日": "https://transit.yahoo.co.jp/timetable/22691/7170?kind=1",
    "休日": "https://transit.yahoo.co.jp/timetable/22691/7170?kind=4"
}

schedule_data = {}

for day_type, url in urls.items():
    print(f"Fetching data for {day_type}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        times = []
        timetable = soup.find("ul", class_="timetable")
        if timetable:
            for li in timetable.find_all("li"):
                time_text = li.get_text(strip=True)
                match = re.match(r"\d{1,2}:\d{2}", time_text)
                if match:
                    times.append(match.group())

        schedule_data[day_type] = times
    else:
        print(f"Failed to fetch data for {day_type}. Status code: {response.status_code}")

df = pd.DataFrame.from_dict(schedule_data, orient="index").transpose()
df.to_csv("train_schedule_comparison.csv", index=False)
print("Comparison saved to 'train_schedule_comparison.csv'")
