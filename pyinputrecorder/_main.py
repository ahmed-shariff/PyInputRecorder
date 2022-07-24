from pynput import mouse
from pynput import keyboard
from pathlib import Path
import time

SAVED_FILE_PATH = Path.home() / "pyinputrecorder_saved_macro"

def on_click(x, y, button, pressed):
    print('{0} at {1}   {2}'.format(
        'Pressed' if pressed else 'Released',
        (x, y),
        button.name))
    with open(SAVED_FILE_PATH, "a") as f:
        f.write(f"{time.time()},{button.name},{x},{y},{pressed}\n")

# Keyboard functions
def on_release(key):
    print('{0} released'.format(key))
    # Stop all listeners if excape is pressed
    if key == keyboard.Key.esc:
        # Stop listeners
        raise Exception()


def setup_listeners():
    with open(SAVED_FILE_PATH, "w") as f:
        f.write("")

    mouse_listener = mouse.Listener(
        # on_move=on_move,
        # on_scroll=on_scroll,
        on_click=on_click)
    mouse_listener.start()

    # Collect events until released
    with keyboard.Listener(
            # on_press=on_press,
            on_release=on_release) as listener:
        try:
            listener.join()
        except:
            pass

    mouse_listener.stop()


def repeat_macro():
    mouse_controller = mouse.Controller()
    with open(SAVED_FILE_PATH, "r") as f:
        previous_ts = None
        for line in f:
            ts, button_name, x, y, pressed = line.strip().split(",")
            ts = float(ts)
            if previous_ts is None:
                previous_ts = ts

            time.sleep(ts - previous_ts)
            print(ts - previous_ts)
            mouse_controller.position = (int(x), int(y))
            if pressed == "True":
                mouse_controller.press(mouse.Button[button_name])
            else:
                mouse_controller.release(mouse.Button[button_name])
            previous_ts = ts
