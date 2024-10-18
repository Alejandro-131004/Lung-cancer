import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.animation as manim
from skimage.measure import find_contours
import pylidc as pyl
from pylidc.utils import consensus
import SimpleITK as sitk
from radiomics import featureextractor

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, roc_curve


from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

from sklearn.ensemble import StackingClassifier
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm



X_original = df.drop(['Target', 'Malignancy', 'Nodulo_id'], axis=1)
X = X_original.select_dtypes(include=['number', 'object'])
y = df['Target'] 

imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

column_names = X_original.select_dtypes(include=['number']).columns

X = pd.DataFrame(X)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# importancias das features
feature_importances = rf_model.feature_importances_

# dataset com as importancias e nomes das features
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})

# odena as features pela importancia
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# grafico de barras das importancias das features
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance')
plt.show()