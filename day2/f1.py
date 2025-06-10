import tkinter as tk
import time
import random
import threading

class ReactionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🏁 F1 Reaction Time Test")
        self.root.geometry("700x450")
        self.root.configure(bg="black")

        self.label = tk.Label(root, text="Welcome to the F1 Reaction Time Test!\nClick 'Start' to begin.",
                              font=("Arial", 18), fg="white", bg="black", justify="center")
        self.label.pack(pady=20)

        self.canvas = tk.Canvas(root, width=300, height=80, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.start_button = tk.Button(root, text="Start", font=("Arial", 16, "bold"),
                                      command=self.start_game, bg="green", fg="white", width=12, height=2)
        self.start_button.pack(pady=15)

        self.time_label = tk.Label(root, text="", font=("Arial", 26), fg="cyan", bg="black")
        self.time_label.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14), fg="yellow", bg="black", justify="center")
        self.result_label.pack(pady=10)

        self.root.bind('<Return>', self.record_reaction)
        self.lights = []
        self.waiting = False
        self.start_time = None
        self.stop_event = threading.Event()

        self.create_lights()

    def create_lights(self):
        self.lights.clear()
        self.canvas.delete("all")
        spacing = 10
        radius = 25
        for i in range(5):
            x = spacing + i * (2 * radius + spacing)
            light = self.canvas.create_oval(x, 10, x + 2 * radius, 10 + 2 * radius, fill="gray")
            self.lights.append(light)

    def start_game(self):
        self.reset()
        self.label.config(text="Get Ready...")
        self.create_lights()
        self.root.after(500, self.show_lights_sequence)

    def show_lights_sequence(self):
        delay = 700  # ms between lights
        for i in range(5):
            self.root.after(delay * (i + 1), lambda i=i: self.canvas.itemconfig(self.lights[i], fill="red"))

        # Random delay before lights out
        total_delay = delay * 5 + int(random.uniform(1000, 3000))
        self.root.after(total_delay, self.go_green)

    def go_green(self):
        for light in self.lights:
            self.canvas.itemconfig(light, fill="black")
        self.label.config(text="🟢 GREEN LIGHT! Press ENTER!")
        self.start_time = time.time()
        self.waiting = True
        self.stop_event.clear()
        threading.Thread(target=self.show_timer, daemon=True).start()

    def show_timer(self):
        while not self.stop_event.is_set():
            elapsed = time.time() - self.start_time
            self.time_label.config(text=f"⏱️  {elapsed:.3f} sec")
            time.sleep(0.01)

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

        record = "\nFastest recorded reaction:\nValtteri Bottas (2019 Suzuka GP)\n⏱️  0.04 sec"
        self.result_label.config(text=msg + record)

    def reset(self):
        self.result_label.config(text="")
        self.time_label.config(text="")
        self.waiting = False
        self.stop_event.set()
        self.create_lights()
        self.label.config(text="Get Ready...")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = ReactionGame(root)
    root.mainloop()
