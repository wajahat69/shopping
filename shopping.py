import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

def main():
    df = pd.read_csv('shopping.csv')

    # Drop unnecessary columns
    df = df.drop(columns=[
        "Administrative", "Administrative_Duration", "Informational",
        "Informational_Duration", "OperatingSystems", "Browser",
        "Region", "TrafficType"
    ])

    # Convert boolean columns to int
    df['Weekend'] = df['Weekend'].astype(int)
    df['Revenue'] = df['Revenue'].astype(int)

    # Encode categorical columns
    label_cols = ['Month', 'VisitorType']
    le = LabelEncoder()
    for col in label_cols:
        df[col] = le.fit_transform(df[col])

    # Feature scaling
    scaler = StandardScaler()
    X = df.drop(['Revenue'], axis=1)
    y = df['Revenue']
    X_scaled = scaler.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=TEST_SIZE
    )

    # Train KNN model
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Evaluate
    sensitivity, specificity = evaluate(y_test, predictions)
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

    # Save model, scaler, and feature names
    joblib.dump(model, "shopping_model.pkl")
    joblib.dump(scaler, "shopping_scaler.pkl")
    joblib.dump(X.columns.tolist(), "shopping_features.pkl")  # <<< important fix


def evaluate(y_test, predictions):
    true_positive = ((y_test == 1) & (predictions == 1)).sum()
    true_negative = ((y_test == 0) & (predictions == 0)).sum()
    false_positive = ((y_test == 0) & (predictions == 1)).sum()
    false_negative = ((y_test == 1) & (predictions == 0)).sum()

    sensitivity = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    specificity = true_negative / (true_negative + false_positive) if (true_negative + false_positive) > 0 else 0

    return sensitivity, specificity


if __name__ == "__main__":
    main()
