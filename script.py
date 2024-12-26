import asyncio
from bleak import BleakClient

# Replace with your device's MAC address
DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"
HUMIDITY_CHARACTERISTIC_UUID = "00002a6f-0000-1000-8000-00805f9b34fb"
TEMPERATURE_CHARACTERISTIC_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"

async def read_sensor_data():
    async with BleakClient(DEVICE_ADDRESS) as client:
        humidity = await client.read_gatt_char(HUMIDITY_CHARACTERISTIC_UUID)
        temperature = await client.read_gatt_char(TEMPERATURE_CHARACTERISTIC_UUID)
        
        humidity_value = int.from_bytes(humidity, byteorder='little') / 100.0
        temperature_value = int.from_bytes(temperature, byteorder='little') / 100.0
        
        print(f"Humidity: {humidity_value}%")
        print(f"Temperature: {temperature_value}°C")

if __name__ == "__main__":
    asyncio.run(read_sensor_data())