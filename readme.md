# Blender Fluid Bakes Mover

This script helps in organizing Blender simulation bakes by splitting them into parts based on frame ranges and file sizes, making them suitable for rendering on platforms like SheepIt render farm. The script automatically detects domain folders, calculates file sizes, and creates parts with a maximum size specified by the user.

## Features

- Automatically detects domain folders.
- Splits files into parts based on specified frame ranges and maximum size.
- Maintains directory structure for domain and subfolders.
- Generates log files for each part, detailing the part size, start frame, and end frame.

## Requirements

- Python 3.x

## Usage

1. **Prepare the Script**:
    - Save the script as `move_frames.py`.

2. **Run the Script**:
    - Open a terminal or command prompt.
    - Navigate to the directory where `move_frames.py` is saved.
    - Run the script:
      ```bash
      python move_frames.py
      ```
    - Provide the required inputs when prompted:
      - The root directory of the Blender project.
      - The destination directory for the parts.
      - The maximum size for each part in GB (e.g., 1.9).

## Input Handling

- The script handles both Windows (`\`) and Linux (`/`) path separators.
- It ensures compatibility with various file systems and path structures.

## Log Files

- Each part folder will contain a `log.txt` file.
- The log file includes:
  - Part size (in GB)
  - Start frame
  - End frame

## Example

```bash
Enter the root directory of the Blender project: /path/to/blender/project
Enter the destination directory for the parts: /path/to/destination
Enter the maximum size for each part in GB (e.g., 1.9): 1.9
```

## Notes

- The script uses a brute force approach to sum up the size of each file for the current frame from all domains.
- It tracks the total size and creates a new part folder once the size exceeds the specified maximum.

## Limitations

- The script assumes a specific folder structure for domain and subfolders.
- It relies on file naming patterns (e.g., `_frameNumber.`) to identify and move files. Adjustments may be needed for different naming conventions or folder structures.

# If wrong files are moved

- an additional move.py file is provided
- place in the parts folder and then specify the path to the destination in the "part_name" variable
- give the frame range
- run the script