import pandas as pd
from joblib import dump, load
from sklearn import linear_model
import numpy as np
import os


def train():
    df = pd.read_csv("flight_prices_training.csv")
    
    #preprocessing
    df = df.drop(columns=['flight'])
    num_cols = ['days_left', 'duration']
    cat_cols = ['airline', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']
    train = pd.get_dummies(df, prefix = cat_cols, columns = cat_cols)
    y_train = train['price']
    X_train = train.drop(['price'], axis=1)

    lasso = linear_model.Lasso(alpha=.1, max_iter=5000)
    lasso = lasso.fit(X_train, y_train)
    dir = os.getcwd()
    output = os.path.join(dir,"model.joblib")
    dump(lasso,output)

def predict():
    dir = os.getcwd()
    output = os.path.join(dir,"prediction.csv")
    
    model = load("model.joblib")
    df = pd.read_csv("flight_prices_training.csv")

    predict = df.drop(columns=['flight'])
    cat_cols = ['airline', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']
    predict = pd.get_dummies(predict, prefix = cat_cols, columns = cat_cols)
    X = predict.drop(['price'], axis=1)
    result = model.predict(X)
    df['price'] = result.astype(int) 
    df.to_csv(output, index=False)


if __name__ == "__main__":
    train()
    predict()

