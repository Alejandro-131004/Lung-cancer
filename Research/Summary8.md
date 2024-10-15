**Methods** 
- Two statistical learning techniques:
    - logistic regression (linear) 
    - random forests (non-linear)
- They were used to predict nodule malignancy. The study used eight diagnostic features ** (e.g., spiculation, calcification, subtlety) and additionally derived diameter and volume features from radiologist annotations.

**Results**

- **Classification accuracy** was high: 85.74% (±1.14%) using **only the radiologist-quantified features**.

- **Accuracy** improved to 88.08% (±1.11%) when **diameter and volume were included**.

- The **best-performing features** for malignancy prediction were **spiculation**, **lobulation**, **subtlety**, and **calcification**.

- The **area-under-the-curve** (AUC) score also increased with more features, rising from 0.932 to 0.949 when diameter and volume were added.

**Features used:**

- **Subtlety** (ordinal scale from 1 to 5)

- **Internal Structure** (categorical)

- **Calcification** (categorical)

- **Sphericity** (ordinal)

- **Margin** (ordinal)

- **Lobulation** (ordinal)

- **Spiculation** (ordinal)

- **Texture** (ordinal)

**Feature Importance** 
- The most predictive features for classifying nodule malignancy were identified as:

    - Spiculation
    - Lobulation
    - Subtlety
    - Calcification 

- These features contributed the most to improving classification accuracy.