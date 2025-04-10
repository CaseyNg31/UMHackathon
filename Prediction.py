import joblib
import pandas as pd

# Load the trained model
def load_model(path='allocation_model.pkl'):
    try:
        model = joblib.load(path)
        print("Model loaded successfully")
        return model
    except FileNotFoundError:
        print("Error: allocation_model.pkl not found. Make sure the model is trained and saved.")
        exit()

# Define the target columns (same as during training)
target_columns = [
    'Advancing Health', 'Disease Support', 'Medical Research', 'Financial Aid',
    'Emergency Funds', 'Mitigation', 'Preparedness', 'Response', 'Recovery'
]

# Predict allocations for a given input
def predict_allocation(model, input_data):
    input_df = pd.DataFrame([input_data])
    raw_pred = model.predict(input_df)[0]
    
    prediction = dict(zip(target_columns, raw_pred))
    
    # Filter by category
    if input_data['category'] == 'medical':
        relevant_cols = ['Advancing Health', 'Disease Support', 'Medical Research', 'Financial Aid', 'Emergency Funds']
    else:
        relevant_cols = ['Mitigation', 'Preparedness', 'Response', 'Recovery', 'Emergency Funds']
    
    # Keep only relevant and non-negative values
    prediction = {k: max(0, prediction[k]) for k in relevant_cols}
    
    # Normalize to 100%
    total = sum(prediction.values())
    if total > 0:
        prediction = {k: round(v / total * 100, 1) for k, v in prediction.items()}
    else:
        prediction = {k: 0 for k in relevant_cols}
    
    return prediction

# Display predictions nicely
def display_prediction(title, input_data, prediction):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)
    print(f"Amount:  ${input_data['amount']:,.2f}")
    print(f"Urgency: {input_data['urgency']} / 10")
    print(f"Type:    {input_data['category'].capitalize()}")
    print("\nPredicted Allocation:")
    for k, v in prediction.items():
        print(f"  - {k:<20} {v:>5.1f}%")
    print(f"{'Total:':>24} {sum(prediction.values()):>5.1f}%")

# Main testing logic
def main():
    model = load_model()

    # You can add more test cases here
    test_cases = [
        {
            'name': 'High-urgency disaster',
            'amount': 40000,
            'urgency': 8,
            'category': 'disaster'
        },
        {
            'name': 'Low-urgency medical',
            'amount': 15000,
            'urgency': 4,
            'category': 'medical'
        },
        {
            'name': 'Moderate-urgency disaster',
            'amount': 20000,
            'urgency': 5,
            'category': 'disaster'
        },
        {
            'name': 'Minimal urgency medical',
            'amount': 10000,
            'urgency': 1,
            'category': 'medical'
        }
    ]

    for case in test_cases:
        prediction = predict_allocation(model, case)
        display_prediction(case['name'], case, prediction)

if __name__ == '__main__':
    main()
