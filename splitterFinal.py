import os
import shutil
import re
from pathlib import Path

def get_size(start_path='.', patterns=None):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            if patterns is None or any(re.search(p, f) for p in patterns):
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    return total_size

def move_frames(root_dir, dest_dir, max_size_gb):
    """
    Move specific frame ranges from the root project directory to the part folder based on size.

    Args:
    - root_dir (str): The root directory of the Blender project.
    - dest_dir (str): The destination directory for the parts.
    - max_size_gb (float): The maximum size of each part in GB.
    """
    max_size_bytes = max_size_gb * 1024 ** 3
    part_count = 1
    part_size = 0
    part_start_frame = None
    part_end_frame = None

    # Detect domain folders
    domain_paths = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]

    # Get frame ranges
    frame_pattern = re.compile(r'_(\d+)\.')
    frames = set()
    for domain in domain_paths:
        for subfolder in ['config', 'data', 'guiding', 'mesh', 'noise', 'particles']:
            path = os.path.join(root_dir, domain, subfolder)
            if os.path.exists(path):
                for file in os.listdir(path):
                    match = frame_pattern.search(file)
                    if match:
                        frames.add(int(match.group(1)))
    frames = sorted(frames)

    # Move files based on frame ranges and size
    for frame in frames:
        current_frame_size = 0
        for domain in domain_paths:
            for subfolder in ['config', 'data', 'guiding', 'mesh', 'noise', 'particles']:
                path = os.path.join(root_dir, domain, subfolder)
                if os.path.exists(path):
                    for file in os.listdir(path):
                        if f"_{frame:04}" in file:
                            current_frame_size += os.path.getsize(os.path.join(path, file))

        if part_size + current_frame_size > max_size_bytes:
            # Finalize the current part and start a new one
            if part_start_frame is not None:
                log_path = os.path.join(dest_dir, f"Part{part_count}", "log.txt")
                with open(log_path, 'w') as log_file:
                    log_file.write(f"Part Size: {part_size / (1024 ** 3):.2f} GB\n")
                    log_file.write(f"Start Frame: {part_start_frame}\n")
                    log_file.write(f"End Frame: {part_end_frame}\n")

            part_count += 1
            part_size = 0
            part_start_frame = frame

        part_folder = os.path.join(dest_dir, f"Part{part_count}")
        if not os.path.exists(part_folder):
            os.makedirs(part_folder)

        for domain in domain_paths:
            domain_path = os.path.join(part_folder, domain)
            if not os.path.exists(domain_path):
                os.makedirs(domain_path)

            for subfolder in ['config', 'data', 'guiding', 'mesh', 'noise', 'particles']:
                root_subfolder_path = os.path.join(root_dir, domain, subfolder)
                part_subfolder_path = os.path.join(domain_path, subfolder)
                
                if not os.path.exists(part_subfolder_path):
                    os.makedirs(part_subfolder_path)
                
                if os.path.exists(root_subfolder_path):
                    for file in os.listdir(root_subfolder_path):
                        if f"_{frame:04}" in file:
                            src = os.path.join(root_subfolder_path, file)
                            dst = os.path.join(part_subfolder_path, file)
                            shutil.move(src, dst)

        part_size += current_frame_size
        if part_start_frame is None:
            part_start_frame = frame
        part_end_frame = frame

    # Finalize the last part
    if part_start_frame is not None:
        log_path = os.path.join(dest_dir, f"Part{part_count}", "log.txt")
        with open(log_path, 'w') as log_file:
            log_file.write(f"Part Size: {part_size / (1024 ** 3):.2f} GB\n")
            log_file.write(f"Start Frame: {part_start_frame}\n")
            log_file.write(f"End Frame: {part_end_frame}\n")

# Example usage
root_dir = input("Enter the complete root directory of the Blender project (e.g, C:\Users\....): ")
dest_dir = input("Enter the complete destination directory for the parts(e.g, C:\Users\....): ")
max_size_gb = float(input("Enter the maximum size for each part in GB (e.g., 1.9): "))

move_frames(root_dir, dest_dir, max_size_gb)
