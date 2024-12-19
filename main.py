import subprocess

if __name__ == "__main__":
    schema_path = input("Enter the path to the schematic file: ")
    delay = float(input("Enter delay between commands (seconds): "))
    start_x = int(input("Enter starting X coordinate: "))
    start_y = int(input("Enter starting Y coordinate: "))
    start_z = int(input("Enter starting Z coordinate: "))

    # Step 1: Grouping
    print("Step 1: Grouping...")
    subprocess.run(["python", "grouping.py", schema_path])

    # Step 2: Convert to commands
    print("Step 2: Converting to commands...")
    subprocess.run(["python", "convert_to_commands.py", "groups.json"])

    # Step 3: Listening and executing commands
    print("Step 3: Listening and executing commands...")
    subprocess.run([
        "python", "listener.py",
        "commands.txt",
        str(delay),
        str(start_x),
        str(start_y),
        str(start_z)
    ])
