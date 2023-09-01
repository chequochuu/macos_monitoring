import subprocess
import time
import pygetwindow as gw
import datetime
from collections import defaultdict


def convert_seconds(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    remaining_seconds = remaining_seconds % 60
    return f"{hours} hour(s), {minutes} minute(s), {remaining_seconds} second(s)"

def beautify(target):
    if target.startswith('Iterm'):
        return 'Iterm'
    if target.startswith('Intellij'):
        return 'Intellij'
    if target.startswith('System Settings'):
        return 'System Settings'
    if target.startswith('Google Chrome'):
        if 'starcraft' in target.lower():
            return 'Google Chrome - StarCraft'
        if 'https://chat.openai.com' in target:
            return 'Google Chrome - chatgpt'
        if '//www.facebook.com/' in target:
            return 'Google Chrome - facebook'
        if ('https://github.com/' in target) or ('https://gitlab.com/' in target):
            return 'Google Chrome - git'

    print(target)

    return target

def get_statistic():
    stats = defaultdict(int)
    res = ''

    with open("activity_log.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            try:
                date_time_str, target = line.strip().split(" # ")
                target = beautify(target)
                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                stats[target] += 5
            except Exception as e:
                print(line)
                print(e)
                raise e

    for target, sec in stats.items():
        if sec < 30: 
            continue
        res += f"{target}: {convert_seconds(sec)}\n"
    return res


def get_chrome_url():
    try:
        script = '''
        tell application "Google Chrome"
            get URL of active tab of front window
        end tell
        '''
        url = subprocess.check_output(["osascript", "-e", script]).decode("utf-8").strip()
        return url
    except:
        return "No URL Found"

def show_popup(title, message):
    script = f'display dialog "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])


def monitor_activity():
    last_popup = 0
    with open("activity_log.txt", "a") as log_file:
        while True:
            active_window = gw.getActiveWindow()
            if active_window:
                active_title = active_window.title()
                target = active_title
                if "Google Chrome" in active_title:
                    url = get_chrome_url()
                    target += f' - {url}'
                    if ('https://www.facebook.com' in url or 'https://www.youtube.com' in url) and time.time() - last_popup > 60:
                        last_popup = time.time()
                        show_popup("Stop!", f"Stop scrolling \n {get_statistic()}")

                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} # {target} \n")
                log_file.flush()
        
            time.sleep(5)

if __name__ == "__main__":
    monitor_activity()

