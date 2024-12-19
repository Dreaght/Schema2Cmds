import keyboard
import time
import sys

# Global flags to handle interruptions
stop_execution = False


def execute_commands(commands, delay):
    """Execute commands one by one, with real-time interrupt handling."""
    global stop_execution
    for i, command in enumerate(commands):
        if stop_execution:
            print("Execution interrupted!")
            break

        # Simulate pressing the key sequence to paste the command
        keyboard.press_and_release("enter")
        keyboard.press_and_release("t")

        time.sleep(0.2)

        print(f"{i}/{len(commands)} | {command}")  # Debug: show commands being executed

        keyboard.write(command, 0.01)

        keyboard.press_and_release("enter")
        time.sleep(delay)
    print("Finished command execution.")


def start_execution(commands, delay):
    """Wrapper to start execution when the hotkey is pressed."""
    global stop_execution
    print("Starting command execution...")
    stop_execution = False
    # Release the hotkey keys explicitly
    execute_commands(commands, delay)


def stop_execution_handler():
    """Set the global stop_execution flag."""
    global stop_execution
    print("Stop command received.")
    stop_execution = True
    # Release the hotkey keys explicitly


def exit_program():
    """Exit the program gracefully."""
    print("Stopped listening.")
    sys.exit(0)


def main(commands, delay):
    """Setup hotkeys and start listening."""
    print("Listening for hotkeys...")

    # Hotkeys setup
    keyboard.add_hotkey("pageup", start_execution, args=(commands, delay))
    keyboard.add_hotkey("pagedown", stop_execution_handler)
    keyboard.add_hotkey("delete", exit_program)

    # Keep the program running to listen for hotkeys
    keyboard.wait()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <commands_file> <delay>")
        sys.exit(1)

    commands_file = sys.argv[1]  # Path to commands.txt
    delay = float(sys.argv[2])  # Delay between commands

    with open(commands_file, "r") as f:
        commands = f.read().splitlines()

    main(commands, delay)
