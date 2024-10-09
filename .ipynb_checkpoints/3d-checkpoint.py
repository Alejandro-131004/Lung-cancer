# calculates the 3d image of all the slices for the radiomic feuture calculation


import os
import re
import SimpleITK as sitk
from concurrent.futures import ThreadPoolExecutor, as_completed

def find_dicom_files(directory):
    """
    Recursively search for DICOM files in the given directory and subdirectories.
    Returns a list of DICOM file paths.
    """
    dicom_files = []
    for root, _, files in os.walk(directory):  # os.walk will search recursively
        for file in files:
            if file.lower().endswith('.dcm'):  # Filter for DICOM files
                dicom_files.append(os.path.join(root, file))
    return dicom_files

def load_dicom_series_from_files(dicom_files):
    """
    Load a DICOM series from a list of DICOM files and return as a SimpleITK 3D image.
    """
    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(dicom_files)
    image = reader.Execute()
    return image

def save_3d_image(image, output_filename):
    """
    Save the SimpleITK image as a NIfTI file or other format.
    """
    sitk.WriteImage(image, output_filename)

def process_patient(patient_path, patient_dir):
    """
    Process a single patient directory: load the DICOM series, create a 3D volume, and save it.
    """
    try:
        print(f"Processing patient: {patient_dir}")
        
        # Recursively find DICOM files in the patient's subdirectories
        dicom_files = find_dicom_files(patient_path)
        
        if dicom_files:
            # Load DICOM files as a 3D volume
            ct_image = load_dicom_series_from_files(dicom_files)
            
            # Save the 3D volume (e.g., in NIfTI format)
            output_ct_path = os.path.join(patient_path, 'ct_volume.nii')
            save_3d_image(ct_image, output_ct_path)
            print(f"Saved 3D volume for {patient_dir} as {output_ct_path}")
        
        else:
            print(f"No DICOM files found for {patient_dir}")
    
    except Exception as e:
        print(f"Error processing {patient_dir}: {e}")

# Define the root directory where the LIDC-IDRI dataset is stored
root_dir = r'C:\Users\joaop\OneDrive\Documentos\manifest-1600709154662\LIDC-IDRI'

# Regex pattern to match directories with the format 'LIDC-IDRI-XXXX'
patient_dir_pattern = re.compile(r'LIDC-IDRI-\d{4}')

# Create a thread pool executor for parallel processing
with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust the number of workers as needed
    futures = []
    
    # Loop through the directories in the root folder and process only patient folders
    for patient_dir in os.listdir(root_dir):
        if patient_dir_pattern.match(patient_dir):  # Match only 'LIDC-IDRI-XXXX' format
            patient_path = os.path.join(root_dir, patient_dir)
            
            if os.path.isdir(patient_path):  # Only process directories
                # Submit a new task for each patient directory
                futures.append(executor.submit(process_patient, patient_path, patient_dir))
    
    # As tasks complete, we get their results
    for future in as_completed(futures):
        try:
            # Retrieve the result (if there’s any output from the task)
            future.result()  # This will also raise any exceptions if they occurred in the task
        except Exception as e:
            print(f"Task generated an exception: {e}")

