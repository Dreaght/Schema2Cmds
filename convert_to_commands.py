import json

def convert_to_commands(groups_file):
    with open(groups_file, "r") as f:
        groups = json.load(f)

    commands = []
    for group in groups:
        start_x, start_y, start_z = group["start"]
        end_x, end_y, end_z = group["end"]
        material = group["material"]
        size = group["size"]

        if material not in ("minecraft:glass", "minecraft:air") or size < 0:
            continue

        material = str(material).replace("minecraft:glass", "glass").replace("minecraft:air", "0")

        commands.append(f"/tp {start_x} {start_y} {start_z}")
        commands.append("//pos1")
        commands.append(f"/tp {end_x} {end_y} {end_z}")
        commands.append("//pos2")
        commands.append(f"//set {material}")

    return commands


if __name__ == "__main__":
    import sys
    groups_file = sys.argv[1]  # Path to groups.json
    commands = convert_to_commands(groups_file)

    # Save commands to file
    with open("commands.txt", "w") as f:
        f.write("\n".join(commands))

    print("Commands conversion complete. Saved to 'commands.txt'.")
