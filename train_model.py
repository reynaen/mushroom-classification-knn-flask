import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load dataset
df = pd.read_csv('mushrooms.csv')
print(f"Dataset shape: {df.shape}")
print(f"Class distribution:\n{df['class'].value_counts()}")

# Encode all categorical columns
le_dict = {}
df_encoded = df.copy()

for col in df.columns:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    le_dict[col] = le

# Features and target
X = df_encoded.drop('class', axis=1)
y = df_encoded['class']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train KNN model (k=5)
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train)

# Evaluate
y_pred = knn.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {acc:.4f} ({acc*100:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['edible', 'poisonous']))

# Save model and encoders
model_data = {
    'model': knn,
    'encoders': le_dict,
    'feature_columns': list(X.columns),
    'accuracy': acc
}

with open('model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print("\nModel saved as model.pkl")
print(f"Feature columns: {list(X.columns)}")
