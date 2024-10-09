
# Environment Setup Guide for Lung Cancer Classification using CT Data

## Introduction

During the development of our project, we encountered compatibility issues between different libraries and Python versions. To ensure that everyone can work with the same dependencies and avoid potential conflicts, we have prepared this guide. Below are detailed steps for setting up a controlled virtual environment using `conda`, along with the installation of necessary packages and versions.

---

## Step 1: Install Anaconda or Miniconda

Ensure you have `conda` installed on your system. You can choose between:
- **Anaconda**: Provides a full package manager and data science suite.
  Download from [Anaconda](https://www.anaconda.com/products/distribution).
  
- **Miniconda**: A lightweight version of Anaconda.
  Download from [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

---

## Step 2: Create a Project Directory

Choose or create a directory on your computer where you will store your project files.

### On Windows:
1. Open Command Prompt or PowerShell.
2. Navigate to your desired location:
   ```
   cd path\to\your\desired\location
   ```
3. Create and navigate to a folder:
   ```
   mkdir lung_cancer_project
   cd lung_cancer_project
   ```

### On macOS/Linux:
1. Open Terminal.
2. Navigate to your desired location:
   ```
   cd /path/to/your/desired/location
   ```
3. Create and navigate to a folder:
   ```
   mkdir lung_cancer_project
   cd lung_cancer_project
   ```

---

## Step 3: Create a Conda Virtual Environment

Create a virtual environment named `lung_cancer_env` with Python 3.7:

```
conda create --name lung_cancer_env python=3.7
```

This will ensure that the environment has a compatible Python version for all libraries.

---

## Step 4: Activate the Environment

To start using the newly created environment, activate it.

### On Windows:
```
conda activate lung_cancer_env
```

### On macOS/Linux:
```
conda activate lung_cancer_env
```

You will see `(lung_cancer_env)` at the start of your terminal line, indicating the environment is active.

---

## Step 5: Install Required Packages

With the environment activated, install the necessary libraries.

### Libraries using `conda`:
```
conda install numpy=1.19.5
conda install matplotlib=3.4.3
conda install pandas=1.3.5
conda install -c conda-forge pydicom=2.0.0
```

### Libraries using `pip`:
```
pip install pylidc==0.2.3
pip install pyradiomics==2.2.0
pip install xlrd
pip install openpyxl
```

**Note:** If you encounter an error during the installation of `pyradiomics` related to `SimpleITK`, use the following command first:
```
conda install -c simpleitk simpleitk
```
Then run once again:
```
pip install pyradiomics==2.2.0
```

### Additional installation for Jupyter Notebook:
```
conda install jupyter
pip install ipykernel
```

---


## Step 6: Launch Jupyter Notebook

To use Jupyter Notebook within the `lung_cancer_env` environment:

1. Make sure the environment is activated.
2. Run:
   ```
   jupyter notebook
   ```

This will launch a Jupyter Notebook interface in your web browser with all the necessary libraries installed in the `lung_cancer_env` environment.

---

By following this guide, you will have a stable environment with compatible library versions to develop and test the Lung Cancer Classification using CT Data Project.
