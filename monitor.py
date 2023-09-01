import subprocess
import time
import pygetwindow as gw

def get_chrome_url():
    try:
        script = '''
        tell application "Google Chrome"
            get URL of active tab of front window
        end tell
        '''
#        url = 'aaa'
        url = subprocess.check_output(["osascript", "-e", script]).decode("utf-8").strip()
        return url
    except:
        return "No URL Found"

def monitor_activity():
    i = 0
    while True:
        active_window = gw.getActiveWindow()
        if active_window:
            active_title = active_window.title()
            print(active_title)
            if "Google Chrome" in active_title:
                url = get_chrome_url()
                print(f"Chrome active, current URL: {url}")
                with open("activity_log.txt", "a") as log_file:
                    log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Chrome - {url}\n")
        
        i += 1
        print(i)
        time.sleep(5)

if __name__ == "__main__":
    monitor_activity()

