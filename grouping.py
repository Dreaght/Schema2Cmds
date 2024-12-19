import nbtlib
import sys
import json


def group_boxes(file_path):
    # Load the schematic file and detect its structure
    schem = nbtlib.load(file_path)

    if "size" in schem and "blocks" in schem and "palette" in schem:
        return handle_nbt_format(schem)
    else:
        raise ValueError("Unsupported schematic format or missing required keys.")


def handle_nbt_format(schem):
    """Process .nbt format files."""
    size = schem["size"]
    blocks = schem["blocks"]
    palette = schem["palette"]

    # Convert palette indices to block names
    block_map = {}
    for block in blocks:
        pos = block["pos"]
        state = block["state"]
        x, y, z = pos[0], pos[1], pos[2]
        material = palette[state]["Name"]
        block_map[(x, y, z)] = material

    return group_optimized_boxes(block_map, size)


def group_optimized_boxes(block_map, size):
    """Group boxes using an optimized strategy to minimize commands."""
    groups = []
    visited = set()
    width, height, depth = size

    for y in range(height):
        for z in range(depth):
            for x in range(width):
                if (x, y, z) in visited or (x, y, z) not in block_map:
                    continue

                material = block_map[(x, y, z)]
                if material == "minecraft:air":  # Skip air blocks
                    continue

                # Find and mark the largest box
                box = find_optimized_box(block_map, x, y, z, material, visited)
                if box:
                    groups.append(box)

    # Sort groups by volume (decreasing)
    groups.sort(key=lambda b: b["size"], reverse=True)

    # Return ordered groups with size (volume)
    return [
        {"start": b["start"], "end": b["end"], "material": b["material"], "size": b["size"]}
        for b in groups
    ]


def find_optimized_box(block_map, start_x, start_y, start_z, material, visited):
    """Find the largest box, expanding in all directions efficiently."""
    max_x, max_y, max_z = start_x, start_y, start_z

    # Expand as much as possible in all three dimensions
    expand_x = expand_y = expand_z = True
    while expand_x or expand_y or expand_z:
        if expand_x:
            for y in range(start_y, max_y + 1):
                for z in range(start_z, max_z + 1):
                    if (max_x + 1, y, z) not in block_map or block_map[(max_x + 1, y, z)] != material:
                        expand_x = False
                        break
                if not expand_x:
                    break
            if expand_x:
                max_x += 1

        if expand_y:
            for x in range(start_x, max_x + 1):
                for z in range(start_z, max_z + 1):
                    if (x, max_y + 1, z) not in block_map or block_map[(x, max_y + 1, z)] != material:
                        expand_y = False
                        break
                if not expand_y:
                    break
            if expand_y:
                max_y += 1

        if expand_z:
            for x in range(start_x, max_x + 1):
                for y in range(start_y, max_y + 1):
                    if (x, y, max_z + 1) not in block_map or block_map[(x, y, max_z + 1)] != material:
                        expand_z = False
                        break
                if not expand_z:
                    break
            if expand_z:
                max_z += 1

    # Mark all blocks in the box as visited
    for x in range(start_x, max_x + 1):
        for y in range(start_y, max_y + 1):
            for z in range(start_z, max_z + 1):
                visited.add((x, y, z))

    return {
        "start": (start_x, start_y, start_z),
        "end": (max_x, max_y, max_z),
        "material": material,
        "size": (max_x - start_x + 1) * (max_y - start_y + 1) * (max_z - start_z + 1),
    }


def adjust_coordinates_for_json(groups, start_pos):
    """Adjust the coordinates of the grouped boxes when saving to JSON."""
    adjusted_groups = []
    for group in groups:
        adjusted_start = (group["start"][0] + start_pos[0], group["start"][1] + start_pos[1], group["start"][2] + start_pos[2])
        adjusted_end = (group["end"][0] + start_pos[0], group["end"][1] + start_pos[1], group["end"][2] + start_pos[2])
        adjusted_groups.append({
            "start": adjusted_start,
            "end": adjusted_end,
            "material": group["material"],
            "size": group["size"]
        })
    return adjusted_groups


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python grouping.py <path_to_schematic> <start_x> <start_y> <start_z>")
        sys.exit(1)

    input_file = sys.argv[1]  # Path to schematic file
    start_pos = tuple(map(int, sys.argv[2:5]))  # Starting position (x, y, z)

    try:
        groups = group_boxes(input_file)
        adjusted_groups = adjust_coordinates_for_json(groups, start_pos)

        # Save adjusted output to 'groups.json'
        with open("groups.json", "w") as f:
            json.dump(adjusted_groups, f, indent=4)

        print("Grouping complete. Saved to 'groups.json'.")
    except Exception as e:
        print(f"Error: {e}")
