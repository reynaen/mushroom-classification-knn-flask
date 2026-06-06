from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load model
with open('model.pkl', 'rb') as f:
    model_data = pickle.load(f)

knn_model = model_data['model']
encoders = model_data['encoders']
feature_columns = model_data['feature_columns']
model_accuracy = model_data['accuracy']

# Feature options mapping
FEATURE_OPTIONS = {
    'cap-shape': {
        'b': 'Bell', 'c': 'Conical', 'f': 'Flat',
        'k': 'Knobbed', 's': 'Sunken', 'x': 'Convex'
    },
    'cap-surface': {
        'f': 'Fibrous', 'g': 'Grooves', 's': 'Smooth', 'y': 'Scaly'
    },
    'cap-color': {
        'b': 'Buff', 'c': 'Cinnamon', 'e': 'Red', 'g': 'Gray',
        'n': 'Brown', 'p': 'Pink', 'r': 'Green', 'u': 'Purple',
        'w': 'White', 'y': 'Yellow'
    },
    'bruises': {'f': 'No Bruises', 't': 'Bruises'},
    'odor': {
        'a': 'Almond', 'c': 'Creosote', 'f': 'Foul', 'l': 'Anise',
        'm': 'Musty', 'n': 'None', 'p': 'Pungent', 's': 'Spicy', 'y': 'Fishy'
    },
    'gill-attachment': {'a': 'Attached', 'f': 'Free'},
    'gill-spacing': {'c': 'Close', 'w': 'Crowded'},
    'gill-size': {'b': 'Broad', 'n': 'Narrow'},
    'gill-color': {
        'b': 'Buff', 'e': 'Red', 'g': 'Gray', 'h': 'Chocolate',
        'k': 'Black', 'n': 'Brown', 'o': 'Orange', 'p': 'Pink',
        'r': 'Green', 'u': 'Purple', 'w': 'White', 'y': 'Yellow'
    },
    'stalk-shape': {'e': 'Enlarging', 't': 'Tapering'},
    'stalk-root': {
        '?': 'Missing', 'b': 'Bulbous', 'c': 'Club',
        'e': 'Equal', 'r': 'Rooted'
    },
    'stalk-surface-above-ring': {
        'f': 'Fibrous', 'k': 'Silky', 's': 'Smooth', 'y': 'Scaly'
    },
    'stalk-surface-below-ring': {
        'f': 'Fibrous', 'k': 'Silky', 's': 'Smooth', 'y': 'Scaly'
    },
    'stalk-color-above-ring': {
        'b': 'Buff', 'c': 'Cinnamon', 'e': 'Red', 'g': 'Gray',
        'n': 'Brown', 'o': 'Orange', 'p': 'Pink', 'w': 'White', 'y': 'Yellow'
    },
    'stalk-color-below-ring': {
        'b': 'Buff', 'c': 'Cinnamon', 'e': 'Red', 'g': 'Gray',
        'n': 'Brown', 'o': 'Orange', 'p': 'Pink', 'w': 'White', 'y': 'Yellow'
    },
    'veil-type': {'p': 'Partial'},
    'veil-color': {'n': 'Brown', 'o': 'Orange', 'w': 'White', 'y': 'Yellow'},
    'ring-number': {'n': 'None', 'o': 'One', 't': 'Two'},
    'ring-type': {
        'e': 'Evanescent', 'f': 'Flaring', 'l': 'Large',
        'n': 'None', 'p': 'Pendant'
    },
    'spore-print-color': {
        'b': 'Buff', 'h': 'Chocolate', 'k': 'Black', 'n': 'Brown',
        'o': 'Orange', 'r': 'Green', 'u': 'Purple', 'w': 'White', 'y': 'Yellow'
    },
    'population': {
        'a': 'Abundant', 'c': 'Clustered', 'n': 'Numerous',
        's': 'Scattered', 'v': 'Several', 'y': 'Solitary'
    },
    'habitat': {
        'd': 'Woods', 'g': 'Grasses', 'l': 'Leaves', 'm': 'Meadows',
        'p': 'Paths', 'u': 'Urban', 'w': 'Waste'
    }
}


@app.route('/')
def index():
    return render_template('index.html',
                           features=FEATURE_OPTIONS,
                           feature_columns=feature_columns,
                           accuracy=round(model_accuracy * 100, 2))


@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = {}
        for col in feature_columns:
            val = request.form.get(col)
            if val is None:
                return jsonify({'error': f'Missing field: {col}'}), 400
            le = encoders[col]
            encoded_val = le.transform([val])[0]
            input_data[col] = encoded_val

        input_df = pd.DataFrame([input_data])
        prediction = knn_model.predict(input_df)[0]
        probabilities = knn_model.predict_proba(input_df)[0]

        label_encoder = encoders['class']
        predicted_class = label_encoder.inverse_transform([prediction])[0]
        is_poisonous = predicted_class == 'p'

        result = {
            'class': 'Poisonous' if is_poisonous else 'Edible',
            'class_raw': predicted_class,
            'is_poisonous': is_poisonous,
            'confidence': round(float(max(probabilities)) * 100, 2),
            'prob_edible': round(float(probabilities[0]) * 100, 2),
            'prob_poisonous': round(float(probabilities[1]) * 100, 2),
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/about')
def about():
    return render_template('about.html', accuracy=round(model_accuracy * 100, 2))


if __name__ == '__main__':
    app.run(debug=True)
