import tkinter as tk
import time
import random
import threading

class ReactionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🏁 F1 Reaction Time Test")
        self.root.geometry("500x300")
        self.root.configure(bg="black")

        self.label = tk.Label(root, text="Welcome to the F1 Reaction Time Test!\nPress 'Start' to begin.",
                              font=("Arial", 14), fg="white", bg="black")
        self.label.pack(pady=40)

        self.start_button = tk.Button(root, text="Start", font=("Arial", 14),
                                      command=self.start_game, bg="green", fg="white")
        self.start_button.pack()

        self.time_label = tk.Label(root, text="", font=("Arial", 20), fg="cyan", bg="black")
        self.time_label.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14), fg="yellow", bg="black")
        self.result_label.pack(pady=10)

        self.root.bind('<Return>', self.record_reaction)
        self.waiting = False
        self.start_time = None
        self.timer_running = False
        self.stop_event = threading.Event()

    def start_game(self):
        self.reset()
        self.label.config(text="🚦 Red Light... Get Ready!")
        self.root.update()

        delay = random.uniform(2, 5)
        self.root.after(int(delay * 1000), self.go_green)

    def go_green(self):
        self.label.config(text="🟢 GREEN LIGHT! Press ENTER!")
        self.start_time = time.time()
        self.waiting = True
        self.stop_event.clear()
        threading.Thread(target=self.show_timer, daemon=True).start()

    def show_timer(self):
        self.timer_running = True
        while not self.stop_event.is_set():
            elapsed = time.time() - self.start_time
            self.time_label.config(text=f"⏱️  {elapsed:.3f} sec")
            time.sleep(0.01)
        self.timer_running = False

    def record_reaction(self, event=None):
        if not self.waiting:
            return
        self.waiting = False
        reaction_time = time.time() - self.start_time
        self.stop_event.set()
        self.time_label.config(text=f"⏱️  {reaction_time:.3f} sec")
        self.give_feedback(reaction_time)

    def give_feedback(self, reaction_time):
        if reaction_time < 0.04:
            msg = "Fastest till date!! ⚡️"
        elif reaction_time < 0.2:
            msg = "Lightning fast! ⚡️"
        elif reaction_time < 0.35:
            msg = "Great reflexes! 🏎️"
        elif reaction_time < 0.5:
            msg = "Not bad! 🟡"
        else:
            msg = "You can do better! 🐢"

        record = "\nThe fastest reaction time till date:\nValtteri Bottas (2019 Suzuka GP)\n⏱️  0.04 sec"
        self.result_label.config(text=msg + record)

    def reset(self):
        self.result_label.config(text="")
        self.time_label.config(text="")
        self.waiting = False
        self.stop_event.set()

# Launch the game
if __name__ == "__main__":
    root = tk.Tk()
    app = ReactionGame(root)
    root.mainloop()
