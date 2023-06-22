import time
import numpy as np
import pyaudio
import config


def start_stream(callback, input_device_index=4):
    p = pyaudio.PyAudio()
    frames_per_buffer = int(config.MIC_RATE / config.FPS)
    
    # Check the available input devices
    device_info = p.get_host_api_info_by_index(0)  # Assuming the default host API
    device_count = device_info.get('deviceCount', 0)
    if input_device_index is not None and input_device_index >= device_count:
        raise ValueError("Invalid input_device_index. Please choose a valid device index.")
    
    # Open the audio stream with the specified input device index
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=config.MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=input_device_index)
    
    overflows = 0
    prev_ovf_time = time.time()
    running = True  # Added termination condition
    while running:
        try:
            y = np.fromstring(stream.read(frames_per_buffer), dtype=np.int16)
            y = y.astype(np.float32)
            callback(y)
        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))
                # Add termination condition based on your requirements
                if overflows >= 10:
                    running = False
    stream.stop_stream()
    stream.close()
    p.terminate()
