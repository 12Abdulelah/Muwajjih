# Engineering Decisions

## 1-TF-IDF
Converts complaint text into numbers the model can understand
## 2-Logistic Regression
Predicts the correct department
## 3-Emergency Rule
fire and gas leak are always urgent.
## 4-Protocol
Keeps the service separate from scikit-learn and makes testing easier
## 5-Startup Load
The model loads once when FastAPI starts, not on every request