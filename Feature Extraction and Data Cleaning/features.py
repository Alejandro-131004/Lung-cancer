import pylidc as pl
import SimpleITK as sitk
import pandas as pd
from radiomics import featureextractor
import numpy as np
import statistics
from concurrent.futures import ThreadPoolExecutor
from pylidc.utils import consensus
from scipy.fftpack import fftn  # Import FFT 3D function

# Initialize the feature extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

# Query the LIDC-IDRI dataset for scans with annotations
scans_with_annotations = pl.query(pl.Scan).filter(pl.Scan.annotations.any()).all()

# Lists to store the extracted features
features_list = []
nodule_id_counter = 1


# Function to calculate the mode
def calculate_mode(value):
    try:
        return statistics.mode(value)
    except statistics.StatisticsError:
        return np.nan  # Return NaN if no mode is found


# Function to calculate the mean
def calculate_mean(value):
    return np.mean(value)


# Function to calculate the median
def calculate_median(value):
    return np.median(value)


# Function to compute 3D Fourier Transform and return relevant metrics
def calculate_fourier_3d(nodule_image):
    # Apply 3D Fourier Transform (FFT)
    fourier_transformed = fftn(nodule_image)

    # Extract magnitude spectrum (absolute values)
    magnitude_spectrum = np.abs(fourier_transformed)

    # Compute histogram with 10 bins
    hist, _ = np.histogram(magnitude_spectrum, bins=10)

    # Normalize histogram
    hist_normalized = hist / np.sum(hist)

    # Return the normalized histogram as features
    return {f'fourier_hist_bin_{i}': hist_normalized[i] for i in range(10)}


# Function to process a single scan and extract features
def process_scan(scan):
    global nodule_id_counter  # Keep track of nodule IDs across threads
    feature_data = []

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
            if cmask.shape[0] <= scan_array.shape[0]:  # Check depth
                nodule_image[cmask > 0] = scan_array[
                    np.where(cmask > 0)[0],
                    np.where(cmask > 0)[1],
                    np.where(cmask > 0)[2]
                ]

            # Convert the new nodule image to a SimpleITK image
            nodule_image_sitk = sitk.GetImageFromArray(nodule_image)
            nodule_image_sitk.SetSpacing(spacing)

            # Convert the mask to a SimpleITK image
            mask_image = sitk.GetImageFromArray(cmask.astype(np.uint8))
            mask_image.SetSpacing(spacing)

            # Extract radiomic features using PyRadiomics
            features = extractor.execute(nodule_image_sitk, mask_image, label=1)

            # Add the patient ID and a unique ID for the nodule
            features['Patient_ID'] = patient_id
            features['Nodule_ID'] = f'Nodule_{nodule_id_counter}'
            nodule_id_counter += 1

            # Calculate the additional annotation features for this nodule
            subtlety_values = [ann.subtlety for ann in anns]
            subtlety_mode = calculate_mode(subtlety_values)
            subtlety_mean = calculate_mean(subtlety_values)
            subtlety_median = calculate_median(subtlety_values)

            internalStructure_values = [ann.internalStructure for ann in anns]
            internalStructure_mode = calculate_mode(internalStructure_values)
            internalStructure_mean = calculate_mean(internalStructure_values)
            internalStructure_median = calculate_median(internalStructure_values)

            calcification_values = [ann.calcification for ann in anns]
            calcification_mode = calculate_mode(calcification_values)
            calcification_mean = calculate_mean(calcification_values)
            calcification_median = calculate_median(calcification_values)

            sphericity_values = [ann.sphericity for ann in anns]
            sphericity_mode = calculate_mode(sphericity_values)
            sphericity_mean = calculate_mean(sphericity_values)
            sphericity_median = calculate_median(sphericity_values)

            margin_values = [ann.margin for ann in anns]
            margin_mode = calculate_mode(margin_values)
            margin_mean = calculate_mean(margin_values)
            margin_median = calculate_median(margin_values)

            lobulation_values = [ann.lobulation for ann in anns]
            lobulation_mode = calculate_mode(lobulation_values)
            lobulation_mean = calculate_mean(lobulation_values)
            lobulation_median = calculate_median(lobulation_values)

            spiculation_values = [ann.spiculation for ann in anns]
            spiculation_mode = calculate_mode(spiculation_values)
            spiculation_mean = calculate_mean(spiculation_values)
            spiculation_median = calculate_median(spiculation_values)

            texture_values = [ann.texture for ann in anns]
            texture_mode = calculate_mode(texture_values)
            texture_mean = calculate_mean(texture_values)
            texture_median = calculate_median(texture_values)

            diameter_values = [ann.diameter for ann in anns]
            diameter_mode = calculate_mode(diameter_values)
            diameter_mean = calculate_mean(diameter_values)
            diameter_median = calculate_median(diameter_values)

            surface_area_values = [ann.surface_area for ann in anns]
            surface_area_mode = calculate_mode(surface_area_values)
            surface_area_mean = calculate_mean(surface_area_values)
            surface_area_median = calculate_median(surface_area_values)

            volume_values = [ann.volume for ann in anns]
            volume_mode = calculate_mode(volume_values)
            volume_mean = calculate_mean(volume_values)
            volume_median = calculate_median(volume_values)

            malignancy_values = [ann.malignancy for ann in anns]
            malignancy_mode = calculate_mode(malignancy_values)
            malignancy_mean = calculate_mean(malignancy_values)
            malignancy_median = calculate_median(malignancy_values)

            # Append these calculated values to the feature dictionary
            features.update({
                'subtlety_mode': subtlety_mode,
                'subtlety_mean': subtlety_mean,
                'subtlety_median': subtlety_median,
                'internalStructure_mode': internalStructure_mode,
                'internalStructure_mean': internalStructure_mean,
                'internalStructure_median': internalStructure_median,
                'calcification_mode': calcification_mode,
                'calcification_mean': calcification_mean,
                'calcification_median': calcification_median,
                'sphericity_mode': sphericity_mode,
                'sphericity_mean': sphericity_mean,
                'sphericity_median': sphericity_median,
                'margin_mode': margin_mode,
                'margin_mean': margin_mean,
                'margin_median': margin_median,
                'lobulation_mode': lobulation_mode,
                'lobulation_mean': lobulation_mean,
                'lobulation_median': lobulation_median,
                'spiculation_mode': spiculation_mode,
                'spiculation_mean': spiculation_mean,
                'spiculation_median': spiculation_median,
                'texture_mode': texture_mode,
                'texture_mean': texture_mean,
                'texture_median': texture_median,
                'diameter_mode': diameter_mode,
                'diameter_mean': diameter_mean,
                'diameter_median': diameter_median,
                'surface_area_mode': surface_area_mode,
                'surface_area_mean': surface_area_mean,
                'surface_area_median': surface_area_median,
                'volume_mode': volume_mode,
                'volume_mean': volume_mean,
                'volume_median': volume_median
            })

            # Calculate Fourier Transform 3D features
            fourier_features = calculate_fourier_3d(nodule_image)
            features.update(fourier_features)

            # Add malignancy mode, mean, and median as the last columns
            features.update({
                'malignancy_mode': malignancy_mode,
                'malignancy_mean': malignancy_mean,
                'malignancy_median': malignancy_median
            })

            # Add the features to the feature data
            feature_data.append(features)

    return feature_data


# Multithreaded execution
with ThreadPoolExecutor(max_workers=8) as executor:
    results = executor.map(process_scan, scans_with_annotations)

# Collect results from all workers
for result in results:
    features_list.extend(result)

# Create a DataFrame to store the features
features_df = pd.DataFrame(features_list)

# Save the features to a CSV file, ensuring malignancy columns are last
columns = [col for col in features_df.columns if not col.startswith('malignancy')]  # All except malignancy columns
columns += ['malignancy_mode', 'malignancy_mean', 'malignancy_median']  # Add malignancy columns at the end
features_df = features_df[columns]

# Save the reordered DataFrame to CSV
features_df.to_csv('radiomic_features_pylidc_and_fourier.csv', index=False)