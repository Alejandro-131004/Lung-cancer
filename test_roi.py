import os
import xml.etree.ElementTree as ET
import pandas as pd
import SimpleITK as sitk
import numpy as np
from lxml import etree

# Function to load a NIfTI volume
def load_nifti_volume(volume_path):
    return sitk.ReadImage(volume_path)

# Function to extract Study Instance UID and Series Instance UID from the XML file
def extract_ids_from_xml(xml_file):
    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        # Extract StudyInstanceUID and SeriesInstanceUID
        study_uid_elements = root.xpath('//*[local-name()="StudyInstanceUID"]')
        series_uid_elements = root.xpath('//*[local-name()="SeriesInstanceUID"]')
        
        if study_uid_elements and series_uid_elements:
            return study_uid_elements[0].text, series_uid_elements[0].text
        else:
            print(f"StudyInstanceUID or SeriesInstanceUID missing in {xml_file}")
            return None, None
    except Exception as e:
        print(f"Error extracting IDs from {xml_file}: {e}")
        return None, None

# Function to extract nodule ID and edge map from the XML file
def extract_nodule_data_from_xml(xml_file):
    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()

        # Extract nodule data
        nodule_data = []
        for nodule in root.xpath('//*[local-name()="unblindedRead"]'):
            nodule_id_elements = nodule.xpath('./*[local-name()="noduleID"]')
            if nodule_id_elements:
                nodule_id = nodule_id_elements[0].text.strip()
                edge_map = []
                roi_elements = nodule.xpath('./*[local-name()="roi"]/*[local-name()="edgeMap"]')
                for edge in roi_elements:
                    x = int(edge.xpath('./*[local-name()="xCoord"]')[0].text)
                    y = int(edge.xpath('./*[local-name()="yCoord"]')[0].text)
                    edge_map.append((x, y))
                nodule_data.append((nodule_id, edge_map))
        return nodule_data
    except Exception as e:
        print(f"Error extracting nodule data from {xml_file}: {e}")
        return []

# Function to extract edge maps from XML
def extract_edge_map_from_annotation(nodule_data):
    edge_map = []
    for _, edges in nodule_data:
        edge_map.extend(edges)
    return edge_map

# Function to create a mask from XML annotations using 50% consensus
def create_consensus_mask(ct_volume, annotation_files):
    mask_shape = sitk.GetArrayFromImage(ct_volume).shape
    consensus_mask = np.zeros(mask_shape, dtype=np.float32)
    
    all_edge_maps = []
    
    for annotation_file in annotation_files:
        nodule_data = extract_nodule_data_from_xml(annotation_file)
        edge_map = extract_edge_map_from_annotation(nodule_data)
        if edge_map:
            all_edge_maps.append(edge_map)
    
    # Count votes for consensus
    for edge_map in all_edge_maps:
        for edge in edge_map:
            z, y, x = edge[1], edge[0], edge[2] if len(edge) == 3 else 0  # Adjust for 2D or 3D
            if z < mask_shape[0] and y < mask_shape[1] and x < mask_shape[2]:
                consensus_mask[z, y, x] += 1  # Increment the mask at the correct index
    
    # Apply 50% threshold
    consensus_mask = (consensus_mask >= (len(annotation_files) / 2)).astype(np.uint8)
    return sitk.GetImageFromArray(consensus_mask)

# Load the metadata CSV
metadata_path = r"C:\Users\joaop\OneDrive\Ambiente de Trabalho\Lung-cancer\LIDC-IDRI_MetaData.csv"
metadata_df = pd.read_csv(metadata_path)

# Load the nodule counts from the Excel file
nodule_counts_path = r"C:\Users\joaop\OneDrive\Ambiente de Trabalho\Lung-cancer\lidc-idri-nodule-counts-6-23-2015.xlsx"
nodule_counts_df = pd.read_excel(nodule_counts_path)

# Create a mapping from Patient ID to the number of nodules >=3mm
nodule_counts = pd.Series(nodule_counts_df["Number of Nodules >=3mm**"].values, index=nodule_counts_df["TCIA Patent ID"]).to_dict()

# Filter to only process patients 1-12
metadata_df = metadata_df[metadata_df['Subject ID'].between("LIDC-IDRI-0001", "LIDC-IDRI-0012")]

# Create a mapping from Study UID to Subject ID
uid_to_subject_id = pd.Series(metadata_df["Subject ID"].values, index=metadata_df["Study UID"]).to_dict()

# Directory where XML files are located
xml_base_directory = "D:\\LIDC-XML-only\\tcia-lidc-xml"
xml_files = []
for subdir, _, files in os.walk(xml_base_directory):
    for file in files:
        if file.endswith('.xml'):
            xml_files.append(os.path.join(subdir, file))

# Filter XML files to only include those for patients 1-12
xml_files_filtered = []
for xml_file in xml_files:
    study_uid, series_uid = extract_ids_from_xml(xml_file)
    if study_uid in uid_to_subject_id:
        xml_files_filtered.append(xml_file)

xml_files = xml_files_filtered

# Dictionary to store masks for each patient
nodule_masks = {}

# Debugging print to check how many XML files are processed
print(f"Total XML files being processed: {len(xml_files)}")

# Iterate through XML files to create consensus masks for nodules
for xml_file in xml_files:
    study_uid, series_uid = extract_ids_from_xml(xml_file)
    if study_uid is None or series_uid is None:
        print(f"StudyInstanceUID or SeriesInstanceUID not found in {xml_file}. Skipping this file.")
        continue
    subject_id = uid_to_subject_id.get(study_uid)
    if subject_id is None:
        print(f"No matching Subject ID found for StudyInstanceUID {study_uid}. Skipping this file.")
        continue
    
    # Load the patient's CT volume
    patient_directory = os.path.join("C:\\Users\\joaop\\OneDrive\\Documentos\\manifest-1600709154662\\LIDC-IDRI", subject_id)
    volume_files = [f for f in os.listdir(patient_directory) if f.endswith('.nii')]
    
    if volume_files:
        volume_path = os.path.join(patient_directory, volume_files[0])
        
        nodule_data = extract_nodule_data_from_xml(xml_file)
        
        if not nodule_data:
            print(f"Nodule data not found in {xml_file}. Skipping this file.")
            continue
        
        # Create unique key based on StudyInstanceUID and NoduleID
        for nodule_id, _ in nodule_data:
            unique_key = f"{subject_id}_{study_uid}_{nodule_id.replace(' ', '_').replace('/', '_')}"
            
            # Store annotations in the nodule_masks dictionary
            if unique_key not in nodule_masks:
                nodule_masks[unique_key] = {'annotations': [], 'subject_id': subject_id, 'volume_path': volume_path}
            
            nodule_masks[unique_key]['annotations'].append(xml_file)

# Check how many unique nodules are found
print(f"Total unique nodules found: {len(nodule_masks)}")

# Ensure you set the correct output directory
output_directory = r"C:\Users\joaop\OneDrive\Ambiente de Trabalho\Lung-cancer\masks"  # Specify your output directory here
os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

# Create consensus masks for each nodule
for unique_key, nodule_data in nodule_masks.items():
    annotations = nodule_data['annotations']
    subject_id = nodule_data['subject_id']
    volume_path = nodule_data['volume_path']
    
    ct_volume = load_nifti_volume(volume_path)  # Reload volume for each patient
    consensus_mask = create_consensus_mask(ct_volume, annotations)  # Use all annotations

    # Simplified naming convention: Patient ID and Nodule ID
    nodule_id = unique_key.split('_')[2]  # Extracting the nodule ID from the unique key
    standardized_nodule_name = f"{subject_id}_Nodule_{nodule_id}_mask.nii"  # Simplified name

    output_path = os.path.join(output_directory, standardized_nodule_name)  # Use the specified output directory

    # Validate the consensus mask before saving
    if consensus_mask:
        sitk.WriteImage(consensus_mask, output_path)
        print(f"Saved consensus mask for {subject_id} Nodule {nodule_id} at {output_path}")
    else:
        print(f"Consensus mask is empty for {unique_key}, not saving.")


    

# Verify that the number of masks matches the expected nodule count
for patient_id, count in nodule_counts.items():
    # Count the number of masks for the current patient
    patient_masks = [key for key in nodule_masks.keys() if key.startswith(patient_id)]
    actual_mask_count = len(patient_masks)
    
    # Check if the actual count matches the expected count
    if actual_mask_count != count:
        print(f"Warning: Patient {patient_id} has {actual_mask_count} masks but expected {count} based on nodule counts.")
    

# Final message indicating the completion of processing
print("Mask creation process completed.")
