from pynput import mouse
from pynput import keyboard
from pathlib import Path
import time

# From https://github.com/moses-palmer/pynput/issues/383
import ctypes
PROCESS_PER_MONITOR_DPI_AWARE=2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)


SAVED_FILE_PATH = Path.home() / "pyinputrecorder_saved_macro"

class MouseFunctions:
    def __init__(self, mode:str) -> None:
        self.mode = mode
        assert self.mode in ["a", "r"]
        _controller = mouse.Controller()
        self.current_x, self.current_y = _controller.position

    def on_click(self, x, y, button, pressed):
        print('{0} at {1}   {2}'.format(
            'Pressed' if pressed else 'Released',
            (x, y),
            button.name))
        if self.mode == "r":
            old_x = x
            old_y = y
            x = x - self.current_x
            y = y - self.current_y
            self.current_x = old_x
            self.current_y = old_y

        with open(SAVED_FILE_PATH, "a") as f:
            f.write(f"m{self.mode},{time.time()},{button.name},{x},{y},{pressed}\n")
        
# Keyboard functions
class KeyboardFunctions:
    def __init__(self):
        self.listener = None

    def write_keyboard_data(self, key, pressed):
        if isinstance(key, keyboard.KeyCode):
            key = self.listener.canonical(key)
        rep = key.name if isinstance(key, keyboard.Key) else repr(key).strip("'")
        with open(SAVED_FILE_PATH, "a") as f:
            f.write(f"k,{time.time()},{rep},{pressed}\n")

    def on_press(self, key):
        print('{0} pressed'.format(key))
        # Stop all listeners if excape is pressed
        if key != keyboard.Key.esc:
            self.write_keyboard_data(key, True)

    def on_release(self, key):
        print('{0} released'.format(key))
        # Stop all listeners if excape is pressed
        if key == keyboard.Key.esc:
            # Stop listeners
            raise Exception()
        rep = key.name if isinstance(key, keyboard.Key) else key
        self.write_keyboard_data(key, False)


def setup_listeners(mode:str):
    with open(SAVED_FILE_PATH, "w") as f:
        f.write("")

    mouse_functions = MouseFunctions(mode)
    mouse_listener = mouse.Listener(
        # on_move=on_move,
        # on_scroll=on_scroll,
        on_click=mouse_functions.on_click)
    mouse_listener.start()

    keyboard_function = KeyboardFunctions()
    # Collect events until released
    with keyboard.Listener(
            on_press=keyboard_function.on_press,
            on_release=keyboard_function.on_release) as listener:
        keyboard_function.listener = listener
        try:
            listener.join()
        except:
            pass

    mouse_listener.stop()


def repeat_macro(speed: float):
    mouse_controller = mouse.Controller()
    keyboard_controller = keyboard.Controller()
    assert speed > 0, f"Speed was {speed}, should above 0."
    speed = speed / 100
    with open(SAVED_FILE_PATH, "r") as f:
        previous_ts = None
        base_ts = None
        ts = button_name = x = y = pressed = key = other = None
        for line in f:
            code = line.split(",")[0]
            is_mouse = False
            processed_line = line.strip().split(",")
            if code == "k":
                ts, key, pressed = processed_line[1:]
            else:
                is_mouse = True
                ts, button_name, x, y, pressed = processed_line[1:]
            ts = float(ts)
            if base_ts is None:
                base_ts = ts

            ts = (ts - base_ts) * speed

            if previous_ts is None:
                previous_ts = ts

            time.sleep(ts - previous_ts)
            # print(ts - previous_ts)
            if is_mouse:
                print("event: ", code, x, y, pressed)
                if code[1] == "a":
                    mouse_controller.position = (int(x), int(y))
                elif code[1] == "r":
                    mouse_controller.move(int(x), int(y))

                if pressed == "True":
                    mouse_controller.press(mouse.Button[button_name])
                else:
                    mouse_controller.release(mouse.Button[button_name])
            else:
                try:
                    k = keyboard.Key[key]
                except KeyError:
                    k = key
                if pressed == "True":
                    print(k, "press")
                    keyboard_controller.press(k)
                else:
                    print(k, "rel")
                    keyboard_controller.release(k)
            previous_ts = ts
