import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

def createDecisionTree():
    # Load dataset
    data = pd.read_csv('dataset.csv')
    data.head()

    # Dropping unneccesary columns
    data = data.drop(['filename'], axis=1)

    # Scaling the Feature columns¶
    scaler = StandardScaler()
    X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype=float))
    y = data.iloc[:, -1]
    # Spliting data into test and training set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=29)

    # Create Decision Tree classifer object
    clf = DecisionTreeClassifier(criterion="entropy", max_depth=20)

    # Train Decision Tree Classifer
    clf = clf.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    """Saving the model"""

    joblib.dump(scaler, 'scalerDecisionTree.pkl')
    joblib.dump(clf, 'classifierDecisionTree')

if __name__ == '__main__':
    createDecisionTree()

