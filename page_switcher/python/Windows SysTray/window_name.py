import win32gui, win32process, psutil
import time

def active_window_process_name() -> str:
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return(psutil.Process(pid[-1]).name().replace(".exe", ""))
    except:
        return None

last = ""

while True:
    if active_window_process_name() != last:
        last = active_window_process_name()
        print(last)
    time.sleep(0.5)