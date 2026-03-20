import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv("data/users.csv")

# Create target
def categorize(age):
    if age < 25:
        return "Young"
    elif age <= 40:
        return "Adult"
    else:
        return "Senior"

df["Category"] = df["Age"].apply(categorize)

# Encode Gender
le = LabelEncoder()
df["Gender"] = le.fit_transform(df["Gender"])

X = df[["Age", "Gender"]]
y = df["Category"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(le, open("encoder.pkl", "wb"))
