def calculate_e_value(x_start, y_start, z_start, x_end, y_end, z_end, e_value_provided):
    """
    This function calculates the E value based on the starting and ending points (X, Y, Z).
    Handles 2D (X, Y) movement if Z is not provided.
    :param x_start: Starting X coordinate
    :param y_start: Starting Y coordinate
    :param z_start: Starting Z coordinate
    :param x_end: Ending X coordinate
    :param y_end: Ending Y coordinate
    :param z_end: Ending Z coordinate (optional, can be None)
    :param e_value_provided: Known E value for a specific distance
    :return: G-code command and calculated E value
    """
    # Calculate the distance between the starting and ending points (X, Y, Z if provided)
    if z_start is not None and z_end is not None:
        distance = np.sqrt((x_end - x_start)**2 + (y_end - y_start)**2 + (z_end - z_start)**2)
    else:
        distance = np.sqrt((x_end - x_start)**2 + (y_end - y_start)**2)

    # Assuming a linear relationship, calculate the E per distance
    # e_value_provided corresponds to the extrusion value for a known distance
    known_distance = np.sqrt((149.087 - 138.874)**2 + (109.557 - 99.344)**2 + (11.44 - 9.913)**2)  # Known distance from G-code
    e_per_distance = e_value_provided / known_distance

    # Calculate the E value for the new distance
    new_e_value = distance * e_per_distance

    # Create the G-code command with the calculated E value, formatting based on Z availability
    if z_end is not None:
        gcode_command = f"G1 X{x_end} Y{y_end} Z{z_end} E{new_e_value:.5f}"
    else:
        gcode_command = f"G1 X{x_end} Y{y_end} E{new_e_value:.5f}"

    return gcode_command, new_e_value

def process_gcode_batch(gcode_lines, e_value_provided):
    """
    This function processes a batch of G-code lines to calculate the E values for each movement in 3D (X, Y, and Z).
    :param gcode_lines: List of G-code lines to process
    :param e_value_provided: Known E value for a specific movement
    :return: List of G-code lines with calculated E values
    """
    updated_gcode_lines = []
    prev_x, prev_y, prev_z = None, None, None

    for line in gcode_lines:
        # Extract X, Y, and Z coordinates from the line
        if line.startswith("G1"):
            parts = line.split()
            x = prev_x  # Default to the previous X value if none found in current line
            y = prev_y  # Default to the previous Y value if none found in current line
            z = prev_z  # Default to the previous Z value if none found in current line

            for part in parts:
                if part.startswith("X"):
                    x = float(part[1:])  # Update X if present in the current line
                elif part.startswith("Y"):
                    y = float(part[1:])  # Update Y if present in the current line
                elif part.startswith("Z"):
                    z = float(part[1:])  # Update Z if present in the current line

            # If all X, Y, and Z coordinates are available (including previous values for any missing ones)
            if x is not None and y is not None:
                # If there is a previous point, calculate E value for the current line
                if prev_x is not None and prev_y is not None:
                    gcode, new_e_value = calculate_e_value(prev_x, prev_y, prev_z, x, y, z, e_value_provided)
                    updated_gcode_lines.append(gcode)
                else:
                    updated_gcode_lines.append(line)  # First move, no previous point to calculate E value from
            else:
                updated_gcode_lines.append(line)

            # Update previous X, Y, and Z coordinates for the next line
            prev_x, prev_y, prev_z = x, y, z
        else:
            updated_gcode_lines.append(line)

    return updated_gcode_lines

# Example G-code lines (replace these with your actual G-code)
gcode_lines = [

"G1 X152.363 Y155.013",
"G1 Z8.519",
"G1 X151.23 Y155.132 Z7.395",
"G1 X151.712 Y155.08 Z7.396",
"G1 X151.962 Y155.036 Z7.4",
"G1 X152.935 Y154.859 Z7.39",
"G1 X153.457 Y154.764 Z7.4",
"G1 X154.533 Y154.419 Z7.397",
"G1 X154.879 Y154.305 Z7.386",
"G1 X155.16 Y154.212 Z7.392",
"G1 X155.597 Y154.024 Z7.396",


]

# Known E value for reference (from the G-code example)
e_value_provided = 0.5

# Process the batch of G-code lines
updated_gcode_lines = process_gcode_batch(gcode_lines, e_value_provided)

# Output the updated G-code lines
for line in updated_gcode_lines:
    print(line)
