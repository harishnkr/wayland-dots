#!/usr/bin/env python3
import time
import os
import subprocess

# ===== Pomodoro Settings =====
WORK_DURATION = 1      # minutes
SHORT_BREAK = 1         # minutes
LONG_BREAK = 1         # minutes
CYCLES_BEFORE_LONG = 4  # pomodoros before long break
STATUS_FILE = os.path.expanduser("~/.pomodoro_status")

# ===== Utility Functions =====
def update_status(text):
    """Write status for Waybar and flush immediately."""
    with open(STATUS_FILE, "w") as f:
        f.write(text + "\n")
        f.flush()
        os.fsync(f.fileno())

def notify(label):
    """Send desktop notification (Linux only)."""
    try:
        subprocess.run(["notify-send", "Pomodoro", f"{label} finished!"], check=True)
    except FileNotFoundError:
        pass  # notify-send not installed

def countdown(minutes, label):
    """Countdown timer showing mm:ss in terminal and Waybar."""
    seconds = minutes * 60
    while seconds > 0:
        mins = seconds // 60
        secs = seconds % 60
        time_str = f"{label} - {mins}:{secs:02d}"
        print(f"\r{time_str}", end="", flush=True)  # show in terminal
        update_status(time_str)
        time.sleep(1)
        seconds -= 1
    print()  # newline after countdown
    notify(label)

# ===== Main Loop =====
def main():
    cycle = 0
    while True:
        # Work session
        input(f"Press Enter to start WORK session ({WORK_DURATION} minutes)...")
        print("Work session started!")
        countdown(WORK_DURATION, "WORK")
        cycle += 1

        # Determine break type
        if cycle % CYCLES_BEFORE_LONG == 0:
            input(f"Press Enter to start LONG BREAK ({LONG_BREAK} minutes)...")
            print("Long break started!")
            countdown(LONG_BREAK, "LONG BREAK")
        else:
            input(f"Press Enter to start SHORT BREAK ({SHORT_BREAK} minutes)...")
            print("Short break started!")
            countdown(SHORT_BREAK, "SHORT BREAK")

        # Ask to continue
        answer = input("Do you want to start another Pomodoro? (y/n) ")
        if answer.lower() != "y":
            update_status("Pomodoro stopped")
            print("Pomodoro session ended. Good job!")
            break

if __name__ == "__main__":
    main()
