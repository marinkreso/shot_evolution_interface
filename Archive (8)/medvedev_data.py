import zipfile
from pathlib import Path
import os
import shutil

def recursive_unzip(zip_path, extract_path, depth=0):
    """
    Recursively unzip files and their nested zip files.
    
    Args:
        zip_path (str): Path to the zip file
        extract_path (str): Path where files should be extracted
        depth (int): Current recursion depth for logging
    """
    try:
        # Create the extraction directory if it doesn't exist
        os.makedirs(extract_path, exist_ok=True)
        
        # Extract the current zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            #print(f"{'  ' * depth}Extracting: {Path(zip_path).name}")
            zip_ref.extractall(extract_path)
        
        # Look for zip files in the extracted contents
        for root, _, files in os.walk(extract_path):
            for file in files:
                if file.lower().endswith('.zip'):
                    nested_zip_path = os.path.join(root, file)
                    # Create a new directory for nested zip contents
                    nested_extract_path = os.path.join(
                        root, 
                        Path(file).stem  # Use the zip filename without extension as folder name
                    )
                    
                    # Recursively unzip nested file
                    recursive_unzip(nested_zip_path, nested_extract_path, depth + 1)
                    
                    # Optional: Remove the zip file after extraction
                    os.remove(nested_zip_path)
                    
    except zipfile.BadZipFile:
        ccc = None
        #print(f"Error: {Path(zip_path).name} is not a valid zip file")
    except Exception as e:
        ccc = None
        #print(f"Error processing {Path(zip_path).name}: {str(e)}")

def process_zip_folder(folder_path):
    """
    Process all zip files in a folder.
    
    Args:
        folder_path (str): Path to the folder containing zip files
    """
    # Create a directory for extracted contents
    extract_base_path = os.path.join(folder_path, "extracted")
    if os.path.exists(extract_base_path):
        shutil.rmtree(extract_base_path)  # Clean up any previous extraction
    os.makedirs(extract_base_path)
    
    # Process each zip file in the folder
    from glob import glob
    print(folder_path)
    for zip_file in glob(f'{folder_path}*.zip'):
        print(zip_file)
        # Create a separate directory for each root zip file
        zip_extract_path = os.path.join(extract_base_path, zip_file.stem)
        recursive_unzip(str(zip_file), zip_extract_path)

if __name__ == "__main__":
    # Replace with your folder path
    folder_path = "medvedev_2024_2023/"
    

    print("Starting extraction process...")
    process_zip_folder(folder_path)
    print("\nExtraction complete!")
