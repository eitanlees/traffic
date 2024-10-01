import logging
import os
import time
from datetime import datetime

import googlemaps
import schedule
from fastlite import database

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Setup Google Maps client
gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])

# Setup addresses
home = os.environ["HOME_ADDRESS"]
work = os.environ["WORK_ADDRESS"]

# Setup database
db = database("data/traffic.db")


class Traffic:
    id: int
    origin: str
    destination: str
    timestamp: datetime
    travel_time: int


traffic_table = db.create(Traffic)


# Get travel time between two locations at a specific time
def travel_time(origin, destination, dt):
    trip = gmaps.distance_matrix(origin, destination, departure_time=dt)
    return trip["rows"][0]["elements"][0]["duration_in_traffic"]["value"]


# Calculate delay until the next 5-minute interval
def calculate_delay():
    current_time = datetime.now()
    minutes_remaining = 5 - (current_time.minute % 5)
    delay_seconds = (minutes_remaining * 60) - current_time.second
    return delay_seconds


# Log traffic data and store it in the database
def traffic():
    dt = datetime.now()
    current_hour = dt.hour
    if 6 <= current_hour < 20:
        # Home to work
        home_to_work = travel_time(home, work, dt)
        traffic_table.insert(
            Traffic(
                origin=home, destination=work, timestamp=dt, travel_time=home_to_work
            )
        )

        # Work to home
        work_to_home = travel_time(work, home, dt)
        traffic_table.insert(
            Traffic(
                origin=work, destination=home, timestamp=dt, travel_time=work_to_home
            )
        )

        logging.info(f"↗ {home_to_work//60} min / ↘ {work_to_home//60} min")
    else:
        logging.info("Outside of tracking hours (6:00 - 20:59)")


if __name__ == "__main__":
    logging.info("--------------------")
    logging.info("- Traffic Tracking -")
    logging.info("--------------------")

    # Calculate delay until the next 5-minute interval
    delay = calculate_delay()
    logging.info(
        f"Waiting {delay//60} minutes and {delay%60} seconds till next 5-min interval"
    )

    # Wait for the calculated delay before starting the first traffic check
    time.sleep(delay)
    traffic()

    # Schedule the traffic function to run every 5 minutes
    schedule.every(5).minutes.do(traffic)

    # Run the scheduled tasks indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)
