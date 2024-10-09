import os
import pydicom
import shutil

# Base directory for all patient data
base_directory = r"E:\manifest-1600709154662\LIDC-IDRI"

# Function to check if a DICOM file is RX (CR, DX)
def is_rx_dicom(dcm_file_path):
    try:
        # Read DICOM file metadata
        dcm_data = pydicom.dcmread(dcm_file_path, stop_before_pixels=True)
        # Check the Modality tag (0008, 0060)
        if dcm_data.Modality in ["CR", "DX"]:  # RX modalities
            return True
    except Exception as e:
        print(f"Error reading DICOM file {dcm_file_path}: {e}")
    return False

# Function to remove RX DICOM files and directories containing them
def remove_rx_dicom(base_directory):
    for patient_dir in os.listdir(base_directory):
        patient_path = os.path.join(base_directory, patient_dir)
        if os.path.isdir(patient_path):
            # Traverse directories to find DICOM files
            for root, dirs, files in os.walk(patient_path):
                for file in files:
                    if file.endswith(".dcm"):
                        dcm_file_path = os.path.join(root, file)
                        if is_rx_dicom(dcm_file_path):
                            print(f"Removing RX DICOM file: {dcm_file_path}")
                            os.remove(dcm_file_path)
                
                # Remove empty directories after RX files have been deleted
                if not os.listdir(root):
                    print(f"Removing empty directory: {root}")
                    shutil.rmtree(root)

# Run the function to remove RX DICOM files
remove_rx_dicom(base_directory)
