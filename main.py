import tkinter as tk
import time

class ExamTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Časomíra pro zkoušky")
        self.root.geometry("400x500")
        
        self.part_durations = [400, 400, 400]  
        self.part_labels = ["Část 1", "Část 2", "Část 3"]
        self.current_part = 0
        self.time_left = self.part_durations[self.current_part]
        self.running = False
        
        self.current_time = tk.StringVar()
        self.part_text = tk.StringVar(value="Část 1 ze 3")
        self.countdown_text = tk.StringVar(value="06:40")
        self.percentage = tk.StringVar(value="100%")
        
        tk.Label(root, textvariable=self.current_time, font=("Arial", 14)).pack()
        tk.Label(root, textvariable=self.part_text, font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, textvariable=self.countdown_text, font=("Arial", 30, "bold"), fg="red").pack()
        
        self.canvas = tk.Canvas(root, width=200, height=200, bg="white", highlightthickness=0)
        self.canvas.pack()
        
        self.btn_pause = tk.Button(root, text="Spustit", command=self.toggle_timer, font=("Arial", 12))
        self.btn_pause.pack(pady=5)
        
        self.btn_restart = tk.Button(root, text="Restart", command=self.restart_timer, font=("Arial", 12), bg="red", fg="white")
        self.btn_restart.pack()
        
        tk.Label(root, text="Části zkoušky", font=("Arial", 12, "bold")).pack(pady=5)
        self.part_labels_labels = []
        for i, label in enumerate(self.part_labels):
            lbl = tk.Label(root, text=f"{label}: {i*6+40*i//60:02}:{i*40%60:02} - {(i+1)*6+40*(i+1)//60:02}:{(i+1)*40%60:02}", font=("Arial", 10))
            lbl.pack()
            self.part_labels_labels.append(lbl)
        
        self.update_time()
        self.highlight_current_part()
    
    def update_time(self):
        self.current_time.set(time.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def update_countdown(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
        elif self.running and self.time_left == 0:
            if self.current_part < 2:
                self.current_part += 1
                self.time_left = self.part_durations[self.current_part]
            else:
                return
        
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.countdown_text.set(f"{minutes:02}:{seconds:02}")
        self.part_text.set(f"Část {self.current_part + 1} ze 3")
        self.percentage.set(f"{(100 * self.time_left // self.part_durations[self.current_part]):d}%")
        
        self.draw_progress()
        self.highlight_current_part()
        
        if self.running:
            self.root.after(1000, self.update_countdown)
    
    def toggle_timer(self):
        self.running = not self.running
        self.btn_pause.config(text="Pauza" if self.running else "Spustit")
        if self.running:
            self.update_countdown()
    
    def restart_timer(self):
        self.running = False
        self.btn_pause.config(text="Spustit")
        self.current_part = 0
        self.time_left = self.part_durations[self.current_part]
        self.update_countdown()
    
    def draw_progress(self):
        self.canvas.delete("all")
        angle = 360 * (self.time_left / self.part_durations[self.current_part])
        self.canvas.create_oval(20, 20, 180, 180, outline="#ccc", width=15)
        self.canvas.create_arc(20, 20, 180, 180, start=90, extent=-angle, outline="blue", width=15, style=tk.ARC)
        self.canvas.create_text(100, 100, text=self.percentage.get(), font=("Arial", 20, "bold"), fill="black")
    
    def highlight_current_part(self):
        for i, label in enumerate(self.part_labels_labels):
            if i == self.current_part:
                label.config(font=("Arial", 10, "bold"), fg="blue")
            else:
                label.config(font=("Arial", 10), fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExamTimerApp(root)
    root.mainloop()
