import os
import SimpleITK as sitk
import pandas as pd
from radiomics import featureextractor
import numpy as np
import statistics
import pylidc as pl
from concurrent.futures import ThreadPoolExecutor

# Initialize the feature extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

# Query the LIDC-IDRI dataset for scans with annotations
scans_with_annotations = pl.query(pl.Scan).filter(pl.Scan.annotations.any()).all()

# Lists to store the extracted features and patient IDs
features_list = []

# Variable to create unique IDs for the nodules
nodule_id_counter = 1

# Function to calculate the mode or mean, depending on the case
def calculate_value(value):
    try:
        return statistics.mode(value)
    except statistics.StatisticsError:
        return np.mean(value)

def calculate_mean(value):
    return np.mean(value)

def process_scan(scan):
    global nodule_id_counter
    patient_id = scan.patient_id
    print(f"Processing patient: {patient_id}")

    # Clusterize the annotations for the scan and retrieve all annotations
    nods = scan.cluster_annotations()

    # Use pylidc to stack DICOM slices into a 3D volume
    try:
        scan_array = scan.to_volume()
    except Exception as e:
        print(f"Error stacking DICOM for patient {patient_id}: {e}")
        return  # Skip this scan

    # Check if the scan array is empty
    if scan_array.size == 0:
        print(f"No volume data for patient {patient_id}")
        return

    # Get the spacing (PixelSpacing + SliceThickness) from the scan
    spacing = scan.pixel_spacing  # This gives (z_spacing, y_spacing, x_spacing)

    # Convert the NumPy array to a SimpleITK image for radiomics processing
    scan_image = sitk.GetImageFromArray(scan_array)
    scan_image.SetSpacing(spacing)

    # Iterate through all nodules of the patient
    for anns in nods:
        if anns:
            # Convert consensus annotations into a mask
            cmask, _, _ = pl.utils.consensus(anns, clevel=0.5)

            # Check if cmask is empty
            if cmask.size == 0:
                print(f"No consensus mask for patient {patient_id}")
                continue

            # Convert the mask to a SimpleITK image
            mask_image = sitk.GetImageFromArray(cmask.astype(float))

            # Extract radiomic features using PyRadiomics
            features = extractor.execute(scan_image, mask_image, label=1)

            # Add the patient ID and a unique ID for the nodule
            features['Patient_ID'] = patient_id
            features['Nodule_ID'] = f'Nodule_{nodule_id_counter}'
            nodule_id_counter += 1

            # Calculate additional annotation features for this nodule
            subtlety_value = calculate_value([ann.subtlety for ann in anns])
            internalStructure_value = calculate_value([ann.internalStructure for ann in anns])
            calcification_value = calculate_value([ann.calcification for ann in anns])
            sphericity_value = calculate_value([ann.sphericity for ann in anns])
            margin_value = calculate_value([ann.margin for ann in anns])
            lobulation_value = calculate_value([ann.lobulation for ann in anns])
            spiculation_value = calculate_value([ann.spiculation for ann in anns])
            texture_value = calculate_value([ann.texture for ann in anns])
            malignancy_value = calculate_mean([ann.malignancy for ann in anns])

            # Append these calculated values to the feature dictionary
            features.update({
                'subtlety': subtlety_value,
                'internalStructure': internalStructure_value,
                'calcification': calcification_value,
                'sphericity': sphericity_value,
                'margin': margin_value,
                'lobulation': lobulation_value,
                'spiculation': spiculation_value,
                'texture': texture_value,
                'malignancy': malignancy_value
            })

            # Add the features to the list
            features_list.append(features)
            print(f"Extracted features for patient {patient_id}, nodule {nodule_id_counter - 1}")

# Using multithreading to process scans concurrently
with ThreadPoolExecutor() as executor:
    executor.map(process_scan, scans_with_annotations)

# Create a DataFrame to store the features
features_df = pd.DataFrame(features_list)

# Check if the DataFrame is empty before saving
if features_df.empty:
    print("No features extracted. The CSV file will not be created.")
else:
    # Save the features to a CSV file
    features_df.to_csv('radiomic_features_pylidc.csv', index=False)
    print("Features saved to radiomic_features_pylidc.csv")
