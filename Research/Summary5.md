**NOTAS ARTIGO 5-Highly accurate model for prediction of lung nodule malignancy with CT scans** 

- **CT examinations** -> used to predict lung nodule malignancy in patients.

- **Nodule X** -> Systematic approach to predict lung nodule malignancy from CT data, based on deep learning *convolutional neural networks (CNN)*.
    - For training and validation they analised over 1000 lung nodules in images. All of them were identified and classified by 4 experienced thoracic radiologists.
    - **Nodule X** achieves high accuracy with an AUC of approx 0.99.

- National Lung Screening Trial(NLST) has shown that low dose of *computed tomography screening* could reduce patient **mortality by 20%** comparing with *conventional chest radiographs*.

- **Challenges for computational approach:**
    - Need to provide sensitivy to nodule features as well as robustness to noise.
    - Datasets need to be large enough, consistent and maintain the accuracy of expert-defined ground truth for approach development, training, and testing.

- **General categories of computational strategies for lung nodule malignancy prediction from CT images:**

    - 1º- **Radiomics** approaches based on radiological quantitative image features (QIF);
    - 2º- **Deep learning** approaches such as those based on **convolutional neural networks (CNN)**

- **Radiomics approaches**:
    - They usually build the prediction model based on the extracted 2D or 3D radiological quantitative image features of lung nodules based on **prior knowledge of what features and characteristics are significant**.

- **Deep learning convolutional neural networks (CNN) approaches:**
    - They are very promising with the availability of CT scans from large cohorts (groups/collections/populations/sets/samples).


- **Differences between those 2 approaches:**
    - Both require different input information for nodule malignancy prediction. 
        - **Radiomics approaches** need proper segmentations of the nodules from radiologists or from segmentation algorithms, and then need quantitative image feature extraction.
        - **CNN approaches** do not necessarily require segmentation of the nodules and can perform prediction with one marked point per nodule after the prediction model is trained. Need for much larger training dataset.
    - Once trained, CNN models are more efficient for nodule malignancy prediction compared to radiomics-based models, as they predict directly from images without requiring prior quantitative feature extraction.

**Nodule X**
- Lesions are marked in **three categories**: “nodule > or = 3 mm,” “nodule < 3 mm,” and “non-nodule > or = 3 mm”.
- The lesions of nodules ≥ 3 mm have a **greater probability of malignancy** than lesions in the other two categories.
- **Malignancy scores from 1-5** (with score 1 meaning **highly unlikely to be malignant**, score 2 or 3 **indeterminate**, score 4 **moderately likely to be malignant**, and score 5 **highly likely to be malignant**).
- Sets S1, S2, S3, S4 and S5, respectively.
- They tested two designs: **S1 versus S45**, and **S12 versus S45**.
- For each design, the data were grouped into completely **independent training and validation sets**, with 80% for training and 20% for validation. Both the training and the validation sets was balanced to **contain an equal number of two classes of nodules as “likely malignant” and “likely benign” nodules**.
- S1 vs S45 had an AUC of 0.974 and S12 vs S45 0.971.

**Overview of Nodule X:**

- NoduleX takes a **marked point for a region of interest as input** to generate nodule classification predictions with high accuracy, matching experienced radiologists. Accuracy improves with segmentation by adding quantitative image features. 

    - (a) The deep learning model uses **CNN features** by processing 3D image volumes through 2D multi-channel convolutional and max-pooling layers, generating a feature vector for final classification via a **softmax function**.

    - (b) In the QIF model, around 50 quantitative features from 2D and 3D images are scored.

    - (c) The combined CNN + QIF classifier uses a feature vector from the CNN, combined with QIF features, as input to a trained **Random Forest classifier**.

**Radiomics approach for nodule malignancy classification of the LIDC/IDRI cohort**
- Classifications using a **Random Forest classifier**, based on radiomics features and radiologist segmentations, aligned closely with radiologists' assessments, even with minimal training data.
- Our testing revealed that radiomic quantitative image features **are able to describe the differences in nodules that are identified by experienced radiologists as belonging to different classes** (eg., “Highly unlikely for cancer” and “Highly suspicious for cancer”).
- To establish a baseline for the separation difficulty, a **logistic regression model (LM)** was trained only on a size metric (square root of largest cross-sectional area).

**There are in general three ways of using the data of the LIDC/IDRI cohort** for the study related to classifying nodule as two classes of “likely benign” and “likely malignant”:
- 1º- Using the set of nodules with the malignancy score/ratings (1, 2, 3, 4, and 5). They treated the malignancy of nodules as a **binary classification** problem for **“likely malignant”** versus **“likely benign”** by thresholding the radiologist-assigned malignancy values so that malignancy values **below 3** (i.e., 1 and 2) are categorized as **benign** and values **above 3** (i.e., 4 and 5) are categorized as **malignant**. 

    A multi-scale CNN approach produced a 50-size feature vector for a **Random Forest classifier**, achieving 86.84% accuracy. Another method using taxonomic indexes and phylogenetic trees with an **SVM** reached 88.44% accuracy, 84.22% sensitivity, 90.06% specificity, and an AUC of 0.8714.

- 2º- The study focused only on **nodules from patients with diagnosis data**, considering only those labeled as **benign** or **malignant**. It involved 52 subjects with malignant nodules and 21 with benign nodules, totaling 458 malignant and 107 benign nodules. The model achieved 82% accuracy for malignant and 93% for benign nodules on unseen test data. Another study, using pathologically-proven data as ground truth, reported an average accuracy of 77.52%, with 79.06% sensitivity and 76.11% specificity.

- 3º- Using both sets.

**Nodules vs Non-nodules**
- The study aimed to classify **nodules versus non-nodules** using the full LIDC/IDRI cohort, addressing challenges from the LUNA16 grand challenge. Common **pitfalls** in lung nodule malignancy classification include using **non-independent validation sets**, mixing nodules from the same patient, relying on size-related features, and not fully reporting AUC, accuracy, sensitivity, and specificity, which can **skew results**. 
- They used an **automated segmentation algorithm** as no segmentations were provided from LIDC/IDRI.
-  This technique tended to produce **segmentations that were larger and more “circular” than the visible region of interest in the image**.

**Nodule Section**
- The LIDC/IDRI dataset's XML nodule annotations were used to create a **consensus list of nodules** for each patient, ensuring no **overlap**. The assigned malignancy rating was the **average of the ratings** given by the radiologists who annotated the nodule.


**Description of the datasets** (Até poderiamos colocar isto no notebook)
- The LIDC/IDRI datasets contains the CT scans of 1018 patients/cases, and some patients may have more than one nodule. 
- These CT scans were reviewed by four experienced thoracic radiologists. 
- The radiologists annotated each scan by marking regions of interest in three classes: “nodule ≥ 3 mm,” “nodule < 3 mm,” and “non-nodule.” 
- Each nodule in the “nodule ≥ 3 mm” class was then given a malignancy 
score and a detailed segmentation. 
- “Non-nodule” and “nodule < 3 mm” regions were noted by position in the scan only. 
- The malignancy scores were defined as follows: 1 “Highly Unlikely for Cancer,” 2 “Moderately Unlikely for Cancer,” 3 “Indeterminate Likelihood,” 4 “Moderately Suspicious for Cancer,” 5 “Highly Suspicious for Cancer.”

**The process of Radiological quantitative image (QIF) features extraction**

- Segmentations for all “nodule ≥ 3 mm” regions were provided by the LIDC/IDRI study, they used a **consensus method** to combine the multiple segmentations and malignancy ratings provided for each nodule.
-  **Consensus segmentations** were obtained by plotting each of the radiologist provided segmentations (1 to 4 per nodule per slice), any voxel included in ≥50% of available segmentations was included in the consensus segmentation.
- The consensus malignancy rating was the **average of all malignancy ratings assigned to all slices** included in the final consensus segmentation.
- **“Non-nodule”** regions were segmented using an automated **Python software library**
-  The **segmented regions** were further processed by a Matlab/Octave library to produce the quantitative image feature measurements.
- The following 50 2D features were extracted:
    - **Size & Shape:**
        - Transverse plane with maximal area
        - Number of pixels inside nodule
        - Area
        - Span of nodule (x and y directions)
        - Perimeter
        - Circularity
        - Primary and secondary rotational moments
        - Ratio of largest to smallest rotational moment
    - **HU Statistics:**
        - Median, Mean, Standard Deviation, Variance
        - Skewness, Kurtosis, Entropy
    - **Difference Image HU Statistics:**
        - Mean, Standard Deviation, Variance
        - Skewness, Kurtosis, Entropy
    - **Texture Features:**
        - Lacunarity at 10 box sizes
        - Coarseness, Contrast, Busyness, Complexity, Texture Strength (at 1 and 2 pixel distances)
    - **Surface Features:**
        - Summed distance to surface, Mean distance to surface
        - Normalized summed distance, Normalized mean distance
    - **Fractal Dimensions:**
        - Fractal dimension of area, Fractal dimension of perimeter
    - **Gradient Margin**


