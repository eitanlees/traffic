import os
import time
import schedule
import logging
from datetime import datetime
# from fastlite import database

import googlemaps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])
home = os.environ["HOME_ADDRESS"]
work = os.environ["WORK_ADDRESS"]

# TODO: Set up database
# class Traffic: 
# db = database('traffic.db')

def travel_time(origin, destination, dt):
    trip = gmaps.distance_matrix(origin, destination, departure_time=dt) 
    return trip["rows"][0]["elements"][0]["duration_in_traffic"]["value"]

def calculate_delay():
    current_time = datetime.now()
    minutes_remaining = 5 - (current_time.minute % 5)
    delay_seconds = (minutes_remaining * 60) - current_time.second
    return delay_seconds

def traffic():
    dt = datetime.now()
    current_hour = dt.hour
    if 6 <= current_hour <= 20:
        home_to_work = travel_time(home, work, dt)
        work_to_home = travel_time(work, home, dt)
        logging.info(f"↗ {home_to_work//60} min / ↘ {work_to_home//60} min")
    else:
        logging.info("Outside of tracking hours (6:00 - 20:59)")

if __name__ == "__main__":
    logging.info("-------------------")
    logging.info("- Traffic Tacking -")
    logging.info("-------------------")

    delay = calculate_delay()
    logging.info(f"Waiting {delay//60} minutes and {delay%60} seconds till next 5-min interval")

    time.sleep(delay)
    traffic()
    schedule.every(5).minutes.do(traffic)
    while True:
        schedule.run_pending()
        time.sleep(1)
