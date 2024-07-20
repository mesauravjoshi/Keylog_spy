import pyautogui
import time

def screenShot(duration,interval):
    # Initialize the start time
    start_time = time.time()
    while True:
        # Take a screenshot
        image = pyautogui.screenshot()
        image.save(f"screenshot_{int(time.time())}.png")

        # Check if the duration has been reached
        if time.time() - start_time >= duration:
            break

        # Wait for the interval
        time.sleep(interval)

# # Set the duration to 60 seconds
# duration = 60
# # Set the interval to 10 seconds
# interval = 10

# screenShot(duration,interval)
