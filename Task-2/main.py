import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import time
import pygame
import threading

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")

        # Variables
        self.alarm_time_var = tk.StringVar()
        self.alarm_time_var.set("")

        # GUI Components
        background_image = tk.PhotoImage(file="download.png")
        background_label = tk.Label(root, image=background_image)
        background_label.place(relwidth=1, relheight=1)

        ttk.Label(root, text="Set Alarm Time:", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=10)

        self.time_entry = ttk.Entry(root, textvariable=self.alarm_time_var, font=("Helvetica", 14))
        self.time_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(root, text="AM/PM", font=("Helvetica", 12)).grid(row=0, column=2, padx=10, pady=10)

      
        self.set_alarm_button = tk.Button(root, text="Set Alarm", command=self.set_alarm, font=("Helvetica", 14))
        self.set_alarm_button.grid(row=1, column=0, columnspan=3, pady=10)

        # Initialize Pygame for sound
        pygame.init()

    def set_alarm(self):
        alarm_time_str = self.alarm_time_var.get()

        try:
            alarm_time = datetime.strptime(alarm_time_str, "%I:%M %p")
        except ValueError:
            print("Invalid time format. Use HH:MM AM/PM.")
            return

        current_time = datetime.now()
        alarm_datetime = datetime(current_time.year, current_time.month, current_time.day, alarm_time.hour, alarm_time.minute)

        if alarm_datetime < current_time:
            alarm_datetime += timedelta(days=1)  # Set alarm for the next day

        time_difference = (alarm_datetime - current_time).total_seconds()

        print(f"Alarm set for {alarm_datetime.strftime('%I:%M %p')}. Waiting...")

        threading.Thread(target=self.wait_and_play, args=(time_difference,)).start()

    def wait_and_play(self, time_difference):
        time.sleep(time_difference)
        self.play_alarm_sound()
        print("Alarm! Wake up!")

    def play_alarm_sound(self):
        pygame.mixer.music.load("tone.mp3")  
        pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
