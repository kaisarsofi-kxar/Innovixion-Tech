import tkinter as tk
from datetime import datetime, timedelta
import time
import pygame

class AlarmClockApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Alarm Clock App")

        self.label = tk.Label(master, text="Enter alarm time (HH:MM):")
        self.label.pack(pady=10)

        self.entry = tk.Entry(master)
        self.entry.pack(pady=10)

        self.set_button = tk.Button(master, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=10)

        self.alarm_label = tk.Label(master, text="")
        self.alarm_label.pack(pady=10)

        self.countdown_label = tk.Label(master, text="")
        self.countdown_label.pack(pady=10)

        self.play_sound_button = tk.Button(master, text="Play Sound", command=self.play_sound)
        self.play_sound_button.pack(pady=10)

        # Initialize Pygame for sound
        pygame.init()
        pygame.mixer.init()

        self.update_countdown()  # Start updating the countdown

    def set_alarm(self):
        alarm_time_str = self.entry.get()

        try:
            alarm_time = datetime.strptime(alarm_time_str, "%H:%M")
            current_time = datetime.now()

            if alarm_time < current_time:
                # If the alarm time is earlier than the current time, set it for the next day
                alarm_time += timedelta(days=1)

            time_difference = (alarm_time - current_time).total_seconds()

            # Start a new thread to wait for the specified time before triggering the alarm
            self.master.after(int(time_difference * 1000), self.trigger_alarm)

            self.alarm_label.config(text=f"Alarm set for {alarm_time_str}")
        except ValueError:
            self.alarm_label.config(text="Invalid time format. Please use HH:MM")

    def trigger_alarm(self):
        self.alarm_label.config(text="ALARM! ALARM! ALARM!")
        self.play_sound()

    def play_sound(self):
        pygame.mixer.music.load("sound.mp3")  # Replace with the path to your alarm sound file
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

    def update_countdown(self):
        # Continuously update the countdown label
        alarm_time_str = self.entry.get()

        try:
            alarm_time = datetime.strptime(alarm_time_str, "%H:%M")
            current_time = datetime.now()

            if alarm_time < current_time:
                # If the alarm time is earlier than the current time, set it for the next day
                alarm_time += timedelta(days=1)

            time_difference = (alarm_time - current_time).total_seconds()

            hours, remainder = divmod(time_difference, 3600)
            minutes, seconds = divmod(remainder, 60)

            countdown_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
            self.countdown_label.config(text=f"Time remaining: {countdown_str}")

            # Update the countdown every second
            self.master.after(1000, self.update_countdown)
        except ValueError:
            pass  # Ignore invalid time format while updating countdown

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()
