import requests
import psycopg2
from time import sleep
from datetime import datetime, timezone
from psycopg2 import OperationalError
import threading

# Database connection parameters
DB_HOST = "postgres"
DB_NAME = "gbfs_db"
DB_USER = "gbfs_user"
DB_PASSWORD = "gbfs_password"

# List of GBFS providers with their base URLs
providers = [
    {"name": "Careem BIKE", "url": "https://dubai.publicbikesystem.net/customer/gbfs/v2/gbfs.json"},
    {"name": "Bike Nordelta", "url": "https://nordelta.publicbikesystem.net/ube/gbfs/v1/"},
    {"name": "Ecobici", "url": "https://buenosaires.publicbikesystem.net/ube/gbfs/v1/"}
]

def create_table():
    """Attempt to connect to PostgreSQL and create the bike_stats table."""
    attempts = 5  # Number of connection retries
    conn = None

    # Retry loop for database connection
    for attempt in range(1, attempts + 1):
        try:
            print(f"Connecting to PostgreSQL (Attempt {attempt})...")
            conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            print("Connected to PostgreSQL successfully.")
            break  # Exit the loop if the connection is successful
        except OperationalError as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < attempts:
                sleep(5)  # Wait 5 seconds before retrying
            else:
                raise Exception("Could not connect to the database after several attempts.")

    # Create the bike_stats table if the connection was successful
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS bike_stats (
                    id SERIAL PRIMARY KEY,
                    provider VARCHAR(50),
                    station_id VARCHAR(50),
                    bike_count INT,
                    timestamp TIMESTAMP
                );
                """
            )
            conn.commit()
            print("Table 'bike_stats' created successfully or already exists.")
        finally:
            # Close the cursor and connection properly
            cur.close()
            conn.close()
            print("Database connection closed.")

def get_station_status_url(gbfs_url):
    """Fetch the station_status URL from gbfs.json."""
    response = requests.get(gbfs_url).json()
    feeds = response["data"]["en"]["feeds"]
    for feed in feeds:
        if feed["name"] == "station_status":
            return feed["url"]
    raise Exception(f"station_status feed not found in {gbfs_url}")

def save_data(provider_name, station_id, bike_count, timestamp):
    """Save bike availability stats to PostgreSQL."""
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO bike_stats (provider, station_id, bike_count, timestamp) 
        VALUES (%s, %s, %s, %s)
        """,
        (provider_name, station_id, bike_count, timestamp),
    )
    conn.commit()
    cur.close()
    conn.close()

def get_available_bikes(station_info_url):
    """Fetch available bikes from the station information URL."""
    stations_response = requests.get(station_info_url)
    stations_data = stations_response.json()
    
    # Summing available bikes across all stations
    total_available_bikes = sum(station['num_bikes_available'] for station in stations_data['data']['stations'])
    return total_available_bikes

def monitor_provider(provider):
    """Monitor changes in station_status for a specific provider."""
    status_url = get_station_status_url(provider["url"])
    print(f"Monitoring {provider['name']} at {status_url}")

    while True:
        try:
            response = requests.get(status_url).json()
            last_updated = response["last_updated"]
            stations = response["data"]["stations"]

            # Loop through each station and save bike counts
            for station in stations:
                station_id = station["station_id"]
                num_bikes = station["num_bikes_available"]

                # Create a timezone-aware datetime object
                timestamp = datetime.fromtimestamp(last_updated, tz=timezone.utc)
                save_data(provider["name"], station_id, num_bikes, timestamp)

            # Get the total available bikes and save to the database
            total_available_bikes = get_available_bikes(status_url)
            save_data(provider["name"], "total", total_available_bikes, timestamp)

            # Wait for 5 minutes before the next data fetch
            sleep(600)  # Sleep for 5 minutes (300 seconds)

        except Exception as e:
            print(f"Error monitoring {provider['name']}: {e}")
            sleep(30)  # Wait before retrying

def main():
    """Main function to start monitoring all providers."""
    create_table()  # Create the bike_stats table

    threads = []
    for provider in providers:
        thread = threading.Thread(target=monitor_provider, args=(provider,))
        threads.append(thread)
        thread.start()

    # Optionally, join threads if you want to wait for them to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()