**NOTES LAB.IACD**

- **Metrics:**
	- Use different metrics like F1, recall, balanced accuracy
	- Forbidden to use accuracy
	- or confusion matrix

- **Normalize** the data so that the pyradiomics or the pylidc doesn't give more importance to other features

- Either we **increase the smaller class** or we **decrease the larger class**. For this we have smote, etc.

- We can also **adapt the model**, and for that we can use **weights** (they can be proportions of the dataset)