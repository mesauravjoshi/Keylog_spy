import time
import pyperclip

def monitor_clipboard(duration):
    
    # Get the initial clipboard content
    previous_text = pyperclip.paste()
    print(f"Previous text copied : {previous_text}")
    # Time when the program started
    start_time = time.time()
    
    # Open the file in append mode
    with open('clipboard_monitor.txt', 'a') as file:
        # Write the previous clipboard content at the beginning
        file.write("Previous text : " + previous_text + "\n")
        file.write("Current texts copied : \n-----------------------------------------\n")
        
    # Loop for the specified duration
    while (time.time() - start_time) < duration:
        # Check the current clipboard content
        current_text = pyperclip.paste()
        # Compare with previous content to find changes
        if current_text != previous_text:
            # Print new text
            
            with open('clipboard_monitor.txt', 'a') as file:
                file.write(current_text+"\n")
                file.write("-----------------------------------------\n")
            # Update previous_text to current_text
            previous_text = current_text
        
        # Wait for a short duration before checking again
        time.sleep(1)  # Adjust sleep duration as needed

    print("Duration ended. Stopping clipboard monitoring.")

