import os
import xml.etree.ElementTree as ET
import pandas as pd
import SimpleITK as sitk
import numpy as np

# Function to load a NIfTI volume
def load_nifti_volume(volume_path):
    return sitk.ReadImage(volume_path)

# Function to create a mask from XML annotations using 50% consensus
def create_consensus_mask(ct_volume, annotation_files, nodule_id):
    # Initialize a binary mask with zeros
    mask_shape = sitk.GetArrayFromImage(ct_volume).shape
    consensus_mask = np.zeros(mask_shape, dtype=np.float32)
    total_annotations = len(annotation_files)
    
    # Collect all edge maps from annotations
    all_edge_maps = []
    
    for annotation_file in annotation_files:
        edge_map = extract_edge_map_from_xml(annotation_file)
        if edge_map is not None:
            all_edge_maps.append(edge_map)

    # Count votes for consensus
    for edge_map in all_edge_maps:
        for edge in edge_map:
            # Increment the consensus mask at the edge coordinates
            consensus_mask[edge[2], edge[1], edge[0]] += 1  # (z, y, x)

    # Apply 50% threshold
    consensus_mask = (consensus_mask >= (total_annotations / 2)).astype(np.uint8)

    # Convert back to SimpleITK image
    return sitk.GetImageFromArray(consensus_mask)

# Function to extract edge maps from an XML annotation file
def extract_edge_map_from_xml(annotation_file):
    tree = ET.parse(annotation_file)
    root = tree.getroot()
    
    ns = {'ns': 'http://www.nih.gov'}  # Adjust namespace as needed
    edge_map = []

    for roi in root.findall('.//roi', ns):
        # Get the nodule ID (if needed)
        nodule_id_elem = roi.find('noduleID', ns)
        if nodule_id_elem is not None and nodule_id_elem.text != nodule_id:
            continue  # Skip if this ROI does not match the desired nodule ID

        for edge in roi.findall('.//edgeMap', ns):
            x = int(edge.find('xCoord', ns).text)
            y = int(edge.find('yCoord', ns).text)
            z = int(roi.find('imageZposition', ns).text)  # Get the z position (depth)
            edge_map.append((x, y, z))  # Append coordinates (x, y, z)

    return edge_map

# Load the metadata CSV
metadata_path = "D:\\LIDC-IDRI_MetaData.csv"  # Adjust path as needed
metadata_df = pd.read_csv(metadata_path)

# Create a mapping from Study UID to Subject ID
uid_to_subject_id = pd.Series(metadata_df["Subject ID"].values, index=metadata_df["Study UID"]).to_dict()

# Directory where XML files are located
xml_base_directory = "D:\\LIDC-XML-only\\tcia-lidc-xml"  # Adjust path as needed
xml_files = []

# Collect all XML files in subdirectories
for subdir, _, files in os.walk(xml_base_directory):
    for file in files:
        if file.endswith('.xml'):
            xml_files.append(os.path.join(subdir, file))

# Dictionary to store masks for each patient
patient_masks = {}

# Iterate through XML files to create consensus masks for nodules
nodule_masks = {}
for xml_file in xml_files:
    # Extract StudyInstanceUID from the XML file
    study_uid = extract_study_uid_from_xml(xml_file)

    if study_uid is None:
        print(f"StudyInstanceUID not found in {xml_file}. Skipping this file.")
        continue  # Skip this file if no UID is found

    # Map StudyInstanceUID to Subject ID
    subject_id = uid_to_subject_id.get(study_uid)

    if subject_id is None:
        print(f"No matching Subject ID found for StudyInstanceUID {study_uid}. Skipping this file.")
        continue  # Skip if no corresponding Subject ID is found

    # Construct the patient directory path
    patient_directory = os.path.join("C:\\Users\\joaop\\OneDrive\\Documentos\\manifest-1600709154662\\LIDC-IDRI", subject_id)

    # Load the NIfTI volume for the patient
    volume_files = [f for f in os.listdir(patient_directory) if f.endswith('.nii')]

    if volume_files:
        volume_path = os.path.join(patient_directory, volume_files[0])  # Load the first NIfTI file found
        ct_volume = load_nifti_volume(volume_path)

        # Process each nodule
        nodule_id = "Nodule 004"  # Replace with your logic to extract the correct nodule ID
        if nodule_id not in nodule_masks:
            nodule_masks[nodule_id] = []
        nodule_masks[nodule_id].append(xml_file)  # Store XML file for this nodule

# Create consensus masks for each nodule
for nodule_id, annotations in nodule_masks.items():
    consensus_mask = create_consensus_mask(ct_volume, annotations, nodule_id)
    
    # Store the consensus mask in the patient_masks dictionary
    if subject_id not in patient_masks:
        patient_masks[subject_id] = []
    patient_masks[subject_id].append(consensus_mask)
