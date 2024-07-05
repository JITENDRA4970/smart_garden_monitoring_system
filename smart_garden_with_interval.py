import streamlit as st
import statistics
import sqlite3
from datetime import datetime
import time


def get_sensor_readings(prefix=""):
    temp = st.number_input(f"{prefix}Enter temperature reading:", format="%f", key=f'{prefix}temp', value=0.0)
    humidity = st.number_input(f"{prefix}Enter humidity reading:", format="%f", key=f'{prefix}humidity', value=0.0)
    soil_moisture = st.number_input(f"{prefix}Enter soil moisture reading:", format="%f", key=f'{prefix}soil_moisture',
                                    value=0.0)
    return temp, humidity, soil_moisture


def analyze_readings(readings):
    temps, humidities, soil_moistures = zip(*readings)

    avg_temp = statistics.mean(temps)
    max_temp = max(temps)
    avg_humidity = statistics.mean(humidities)
    avg_soil_moisture = statistics.mean(soil_moistures)

    return avg_temp, max_temp, avg_humidity, avg_soil_moisture


def decide_watering(avg_temp, max_temp, avg_humidity, avg_soil_moisture):
    if avg_soil_moisture < 30 and avg_temp > 25 and avg_humidity < 60:
        return True
    if avg_soil_moisture < 50 and avg_temp > 35 and avg_humidity < 70:
        return True
    if avg_soil_moisture < 60 and avg_temp > 40 and avg_humidity < 80:
        return True
    return False


def store_data(conn, timestamp, avg_temp, max_temp, avg_humidity, avg_soil_moisture, watering_decision):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO garden_data 
        (timestamp, temperature, temperature_max, humidity, soil_moisture, watering_decision)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, avg_temp, max_temp, avg_humidity, avg_soil_moisture, watering_decision))
    conn.commit()


def setup_database():
    conn = sqlite3.connect('smart_garden.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS garden_data
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         timestamp TEXT,
         temperature REAL,
         temperature_max REAL,
         humidity REAL,
         soil_moisture REAL,
         watering_decision INTEGER)
    ''')
    conn.commit()
    return conn


# Streamlit application
def main():
    st.title("Smart Garden Monitoring System")

    conn = setup_database()

    if 'readings' not in st.session_state:
        st.session_state.readings = []
        st.session_state.step = 0

    if st.session_state.step == 0:
        st.write("Please enter the first set of sensor readings.")
        temp, humidity, soil_moisture = get_sensor_readings("First Reading: ")

        if st.button("Submit First Reading"):
            st.session_state.readings.append((temp, humidity, soil_moisture))
            st.session_state.step = 1
            st.experimental_rerun()

    elif st.session_state.step == 1:
        st.write("Waiting for 5 seconds before next reading...")
        time.sleep(5)
        st.write("Please enter the second set of sensor readings.")
        temp, humidity, soil_moisture = get_sensor_readings("Second Reading: ")

        if st.button("Submit Second Reading"):
            st.session_state.readings.append((temp, humidity, soil_moisture))
            st.session_state.step = 2
            st.experimental_rerun()

    elif st.session_state.step == 2:
        avg_temp, max_temp, avg_humidity, avg_soil_moisture = analyze_readings(st.session_state.readings)
        watering_needed = decide_watering(avg_temp, max_temp, avg_humidity, avg_soil_moisture)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.write(f"\nAnalysis Results at {current_time}:")
        st.write(f"Average Temperature: {avg_temp:.2f}°C")
        st.write(f"Maximum Temperature: {max_temp:.2f}°C")
        st.write(f"Average Humidity: {avg_humidity:.2f}%")
        st.write(f"Average Soil Moisture: {avg_soil_moisture:.2f}%")

        if watering_needed:
            st.write("Watering recommended!")
            st.image("watering_logo.png", caption="Watering Recommended")
        else:
            st.write("Watering not needed at this time.")
            st.image("not_watering_logo.png", caption="No Watering Needed")

        store_data(conn, current_time, avg_temp, max_temp, avg_humidity, avg_soil_moisture, int(watering_needed))

        st.session_state.readings = []
        st.session_state.step = 0  # Reset for next set of readings

    conn.close()


if __name__ == "__main__":
    main()
