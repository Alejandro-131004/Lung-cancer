import pylidc as pl
import SimpleITK as sitk
import pandas as pd
from radiomics import featureextractor
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from scipy.fftpack import fftn  # Import FFT 3D function
import threading  # For thread-safe operations

# Initialize the feature extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

# Query the LIDC-IDRI dataset for scans with annotations
scans_with_annotations = pl.query(pl.Scan).filter(pl.Scan.annotations.any()).all()

# Lists to store the extracted features
features_list = []
nodule_id_counter = 1
nodule_id_lock = threading.Lock()  # Lock for thread-safe incrementing

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

    # Load the full scan volume
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

    # Iterating through all annotations of the patient
    for ann in scan.annotations:
        # Get the bounding box for the annotation to reduce processing area
        bbox = ann.bbox()

        # Extract the nodule region from the scan array
        nodule_array = scan_array[bbox]

        # Get the mask for the annotation
        mask = ann.boolean_mask(pad=[(0, 0), (0, 0), (0, 0)])

        # Ensure the mask and nodule_array have the same shape
        if nodule_array.shape != mask.shape:
            # Resize mask to match nodule_array shape if necessary
            mask = mask[:nodule_array.shape[0], :nodule_array.shape[1], :nodule_array.shape[2]]

        # Convert the nodule array and mask to SimpleITK images
        nodule_image_sitk = sitk.GetImageFromArray(nodule_array)
        nodule_image_sitk.SetSpacing(spacing)

        mask_image = sitk.GetImageFromArray(mask.astype(np.uint8))
        mask_image.SetSpacing(spacing)

        # Extract radiomic features using PyRadiomics
        features = extractor.execute(nodule_image_sitk, mask_image, label=1)

        # Add the patient ID and a unique ID for the nodule
        features['Patient_ID'] = patient_id

        # Thread-safe increment of nodule_id_counter
        with nodule_id_lock:
            features['Nodule_ID'] = f'Nodule_{nodule_id_counter}'
            nodule_id_counter += 1

        # Include the annotation's semantic features directly
        features.update({
            'subtlety': ann.subtlety,
            'internalStructure': ann.internalStructure,
            'calcification': ann.calcification,
            'sphericity': ann.sphericity,
            'margin': ann.margin,
            'lobulation': ann.lobulation,
            'spiculation': ann.spiculation,
            'texture': ann.texture,
            'malignancy': ann.malignancy,
            'diameter': ann.diameter,
            'surface_area': ann.surface_area,
            'volume': ann.volume
        })

        # Calculate Fourier Transform 3D features
        fourier_features = calculate_fourier_3d(nodule_array)
        features.update(fourier_features)

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

# Save the features to a CSV file
features_df.to_csv('radiomic_features_pylidc_and_fourier_per_annotation.csv', index=False)
