import pyaudio

p = pyaudio.PyAudio()

device_info = p.get_host_api_info_by_index(0)
print(device_info)  # Assuming the default host API
device_count = device_info.get('deviceCount', 0)

print("Available input devices:")
for i in range(device_count):
    device_info = p.get_device_info_by_host_api_device_index(0, i)
    print(f"Index: {i}, Name: {device_info['name']}, Channels: {device_info['maxInputChannels']}")
