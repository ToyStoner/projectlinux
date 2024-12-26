import asyncio
import requests
from bleak import BleakClient
import mysql.connector
from mysql.connector import Error

# Replace with your device's MAC address
DEVICE_ADDRESS = "53:03:E9:25:A5:C3"
HUMIDITY_CHARACTERISTIC_UUID = "00002a6f-0000-1000-8000-00805f9b34fb"
TEMPERATURE_CHARACTERISTIC_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"

# ThingSpeak API configuration
THINGSPEAK_API_KEY = "GE08E5B650OT2X84"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

def store_sensor_data(humidity, temperature):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="meejas",
            password="jasper",
            database="environment"
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        cursor = connection.cursor()
        query = "INSERT INTO measurements (humidity, temperature) VALUES (%s, %s)"
        cursor.execute(query, (humidity, temperature))
        connection.commit()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def send_to_thingspeak(humidity, temperature):
    try:
        response = requests.get(THINGSPEAK_URL, params={
            'api_key': THINGSPEAK_API_KEY,
            'field1': temperature,
            'field2': humidity
        })
        if response.status_code == 200:
            print("Data successfully sent to ThingSpeak")
        else:
            print(f"Failed to send data to ThingSpeak: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while sending data to ThingSpeak: {e}")

async def read_sensor_data(client):
    try:
        humidity = await client.read_gatt_char(HUMIDITY_CHARACTERISTIC_UUID)
        temperature = await client.read_gatt_char(TEMPERATURE_CHARACTERISTIC_UUID)
        
        humidity_value = int.from_bytes(humidity, byteorder='little') / 100.0
        temperature_value = int.from_bytes(temperature, byteorder='little') / 100.0
        
        print(f"Humidity: {humidity_value}%")
        print(f"Temperature: {temperature_value}°C")
        store_sensor_data(humidity_value, temperature_value)
        send_to_thingspeak(humidity_value, temperature_value)
    except Exception as e:
        print(f"Failed to read sensor data: {e}")

async def main():
    while True:
        try:
            async with BleakClient(DEVICE_ADDRESS) as client:
                while True:
                    await read_sensor_data(client)
                    await asyncio.sleep(3)
        except Exception as e:
            print(f"BLE client disconnected or failed to connect: {e}")
            print("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
