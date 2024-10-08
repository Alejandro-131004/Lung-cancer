import pylidc as pl
import SimpleITK as sitk
import pandas as pd
from radiomics import featureextractor
import numpy as np
import statistics
from pylidc.utils import consensus

# Initialize the feature extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

# Query the LIDC-IDRI dataset for scans with annotations
scans_with_annotations = pl.query(pl.Scan).filter(pl.Scan.annotations.any()).all()[:8]

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

# Iterating through all scans with annotations
for scan in scans_with_annotations:
    # Get the patient ID
    patient_id = scan.patient_id

    # Clusterize the annotations for the scan and retrieve all annotations
    nods = scan.cluster_annotations()

    # Use pylidc to stack DICOM slices into a 3D volume
    scan_array = scan.to_volume()

    # Handle pixel spacing depending on its type
    if isinstance(scan.pixel_spacing, (list, tuple)):
        spacing = (scan.pixel_spacing[0], scan.pixel_spacing[1], scan.slice_thickness)
    else:
        # Assuming the spacing is isotropic, if pixel_spacing is a single float
        spacing = (scan.pixel_spacing, scan.pixel_spacing, scan.slice_thickness)

    # Convert the NumPy array to a SimpleITK image for radiomics processing
    scan_image = sitk.GetImageFromArray(scan_array)
    scan_image.SetSpacing(spacing)

    # Iterating through all nodules of the patient
    for anns in nods:
        if anns:
            # Convert consensus annotations into a mask
            cmask, _, _ = pl.utils.consensus(anns, clevel=0.5, pad=[(20, 20), (20, 20), (0, 0)])

            # Check the dimensions of the scan_array and cmask
            print(f"Scan dimensions: {scan_array.shape}, Mask dimensions: {cmask.shape}")

            # Create a nodule image initialized to zeros with the same shape as the mask
            nodule_image = np.zeros_like(cmask, dtype=scan_array.dtype)

            # Fill the nodule_image based on the mask and corresponding region in scan_array
            # First, ensure the mask and scan_array can be correctly indexed
            if cmask.shape[0] <= scan_array.shape[0]:  # Check depth
                nodule_image[cmask > 0] = scan_array[
                    np.where(cmask > 0)[0],
                    np.where(cmask > 0)[1],
                    np.where(cmask > 0)[2]
                ]

            # Convert the new nodule image to a SimpleITK image
            nodule_image_sitk = sitk.GetImageFromArray(nodule_image)
            nodule_image_sitk.SetSpacing(spacing)  # Set spacing for the new image

            # Convert the mask to a SimpleITK image
            mask_image = sitk.GetImageFromArray(cmask.astype(np.uint8))
            mask_image.SetSpacing(spacing)  # Set spacing for the mask image

            # Extract radiomic features using PyRadiomics
            features = extractor.execute(nodule_image_sitk, mask_image, label=1)

            # Add the patient ID and a unique ID for the nodule
            features['Patient_ID'] = patient_id
            features['Nodule_ID'] = f'Nodule_{nodule_id_counter}'
            nodule_id_counter += 1

            # Calculate the additional annotation features for this nodule
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

# Create a DataFrame to store the features
features_df = pd.DataFrame(features_list)

# Save the features to a CSV file
features_df.to_csv('radiomic_features_pylidc.csv', index=False)
