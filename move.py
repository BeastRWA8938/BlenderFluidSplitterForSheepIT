import os
import shutil
import re

def move_frames(part_folder, domains, frame_range):
    """
    Move specific frame ranges from the root project directory to the part folder.

    Args:
    - part_folder (str): The name of the part folder where frames should be moved.
    - domains (list): List of domain folder names to move.
    - frame_range (tuple): The range of frames to move, inclusive.
    """
    
    # Create the part folder if it doesn't exist
    if not os.path.exists(part_folder):
        os.makedirs(part_folder)
    
    # Iterate through each domain folder
    for domain in domains:
        # Define paths
        root_domain_path = os.path.join(domain)
        part_domain_path = os.path.join(part_folder, domain)
        
        # Create the domain folder in the part folder
        if not os.path.exists(part_domain_path):
            os.makedirs(part_domain_path)
        
        # Iterate through each subfolder in the domain folder
        for subfolder in ['config', 'data', 'guiding', 'mesh', 'noise', 'particles']:
            root_subfolder_path = os.path.join(root_domain_path, subfolder)
            part_subfolder_path = os.path.join(part_domain_path, subfolder)
            
            # Create the subfolder in the part domain folder
            if not os.path.exists(part_subfolder_path):
                os.makedirs(part_subfolder_path)
            
            # Check if the subfolder exists in the root domain folder
            if os.path.exists(root_subfolder_path):
                # Move the files in the specified frame range
                for file in os.listdir(root_subfolder_path):
                    match = re.search(r'_(\d+)\.', file)
                    if match:
                        frame_number = int(match.group(1))
                        if frame_range[0] <= frame_number <= frame_range[1]:
                            src = os.path.join(root_subfolder_path, file)
                            dst = os.path.join(part_subfolder_path, file)
                            shutil.move(src, dst)

# Example usage
part_folder = r"C:\Users\.." # change this to destination
domains = ["FifthTank","SixthTank", "SeventhTank"] # enter domain names
frame_range = (15235, 17300)  # Move frames from 12900 to 12950

move_frames(part_folder, domains, frame_range)
