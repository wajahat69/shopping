import csv
import sys
import pandas as pd


from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.7


def main():

    df=pd.read_csv('shopping.csv')
    
    df['Weekend'] = df['Weekend'].astype(int)
    df['Revenue'] = df['Revenue'].astype(int)
   


    colums=['Month','VisitorType']

    le=LabelEncoder()
    for column in colums:
        df[column]=le.fit_transform(df[column])
    


    scaler = StandardScaler()
    evidence=scaler.fit_transform(df.drop(['Revenue'],axis=1))
    labels=df['Revenue']
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    model=KNeighborsClassifier(n_neighbors=1)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)


    
    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


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
