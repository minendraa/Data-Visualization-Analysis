import time
import random
import threading
import sys
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Stopwatch threading to show live timer
def show_stopwatch(start_time, stop_event):
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        print(f"\r⏱️  {elapsed:.3f} seconds", end="")
        time.sleep(0.01)

def f1_reaction_game():
    clear_screen()
    print("🏁 Welcome to the F1 Reaction Time Test!")
    print("Wait for the red light to go out (🚦), then press ENTER as fast as you can!")
    print("Press ENTER when you're ready...")
    input()

    # Red light
    clear_screen()
    print("🚦 Red Light... Get ready...")
    time.sleep(random.uniform(2, 5))  # Random delay

    # Green light
    clear_screen()
    print("🟢 GREEN LIGHT! PRESS ENTER!")

    start_time = time.time()
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=show_stopwatch, args=(start_time, stop_event))
    timer_thread.start()

    input()  # Wait for user to react
    reaction_time = time.time() - start_time

    stop_event.set()
    timer_thread.join()

    print(f"\n\nYour reaction time: {reaction_time:.3f} seconds")

    if reaction_time < 0.04:
        print("Fastest till date!! ⚡️")
    elif reaction_time < 0.2:
        print("Lightning fast! ⚡️")
    elif reaction_time < 0.35:
        print("Great reflexes! 🏎️")
    elif reaction_time < 0.5:
        print("Not bad! 🟡")
    else:
        print("You can do better! 🐢")

    print("\nThe fastest reaction time till date is made by:\nValtteri Bottas during the 2019 Suzuka Grand Prix.\nTime=0.04 seconds.")

# Run the game
f1_reaction_game()
