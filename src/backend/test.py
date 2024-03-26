from polar_bluetooth_interface import DataStreamer
import time

streamer = DataStreamer("C44F5830-8359-25F6-C6C8-D392D1E6B89A")




while True:
    if streamer.hr_queue:
        hr = streamer.hr_queue[-1]  # Access the most recent heart rate
        print("Heart Rate:", hr)
    time.sleep(1)  # Check every second (adjust as needed)

    print("IBI Queue Values:", streamer.ibi_queue_values)
    print("IBI Queue Times:", streamer.ibi_queue_times)