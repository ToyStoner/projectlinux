
import asyncio
from bleak import BleakClient
import mysql.connector

# Replace with your device's MAC address
DEVICE_ADDRESS = "53:03:E9:25:A5:C3"
HUMIDITY_CHARACTERISTIC_UUID = "00002a6f-0000-1000-8000-00805f9b34fb"
TEMPERATURE_CHARACTERISTIC_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"

def store_sensor_data(humidity, temperature):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="meejas",
            password="jasper",
            database="environment"
        )
        cursor = connection.cursor()
        query = "INSERT INTO measurements (humidity, temperature) VALUES (%s, %s)"
        cursor.execute(query, (humidity, temperature))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

async def read_sensor_data():
    async with BleakClient(DEVICE_ADDRESS) as client:
        humidity = await client.read_gatt_char(HUMIDITY_CHARACTERISTIC_UUID)
        temperature = await client.read_gatt_char(TEMPERATURE_CHARACTERISTIC_UUID)
        
        humidity_value = int.from_bytes(humidity, byteorder='little') / 100.0
        temperature_value = int.from_bytes(temperature, byteorder='little') / 100.0
        
        print(f"Humidity: {humidity_value}%")
        print(f"Temperature: {temperature_value}°C")

async def main():
    while True:
        await read_sensor_data()
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())