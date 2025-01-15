

import argparse
import os
import json
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score
import joblib
import pathlib
from io import StringIO
import boto3
import pandas as pd
import numpy as np

def model_fn(model_dir):
    #loading the model
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf

if __name__ =='__main__':

    print("[INFO] Extracting arguments")
    parser = argparse.ArgumentParser()

    # hyperparameters sent by the client are passed as command-line arguments to the script.
    parser.add_argument('--n_estimators', type=int, default=100)
    parser.add_argument('--random_state', type=int, default=0)
    # parser.add_argument('--epochs', type=int, default=10)
    # parser.add_argument('--batch-size', type=int, default=100)
    # parser.add_argument('--learning-rate', type=float, default=0.1)

    # an alternative way to load hyperparameters via SM_HPS environment variable.
    # parser.add_argument('--sm-hps', type=json.loads, default=os.environ['SM_HPS'])

    # input data and model directories
    #we can retrieve the value of an environment variable using its key by os.environ
    #The variables SM_MODEL_DIR, SM_CHANNEL_TRAIN, and SM_CHANNEL_TEST are environment variables used in AWS SageMaker to streamline the machine learning training and deployment workflow
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    parser.add_argument('--test', type=str, default=os.environ['SM_CHANNEL_TEST'])
    parser.add_argument('--train_file', type=str, default='train_mp.csv')
    parser.add_argument('--test_file', type=str, default='test_mp.csv')

    args, _ = parser.parse_known_args()

    print("SKLearn Version: ", sklearn.__version__)
    print("Joblib Version: ", joblib.__version__)

    print("[INFO] Reading data")
    print()
    train_df = pd.read_csv(os.path.join(args.train, args.train_file))
    test_df = pd.read_csv(os.path.join(args.test, args.test_file))

    features = list(train_df.columns)
    label = features.pop(-1)
    
    print("Building training and testing datasets")
    print()
    X_train = train_df[features]
    X_test = test_df[features]
    y_train = train_df[label]
    y_test = test_df[label]

    print('Column order: ')
    print(features)
    print()
    
    print("Label column is: ",label)
    print()
    
    print("Data Shape: ")
    print()
    print("---- SHAPE OF TRAINING DATA (80%) ----")
    print(X_train.shape)
    print(y_train.shape)
    print()
    print("---- SHAPE OF TESTING DATA (20%) ----")
    print(X_test.shape)
    print(y_test.shape)
    print()
    
    print("Training RandomForest Model.....")
    print()
    model = RandomForestClassifier(n_estimators=args.n_estimators, random_state=args.random_state, verbose=3, n_jobs=None)
    model.fit(X_train, y_train)
    print()

    model_path = os.path.join(args.model_dir, "model.joblib")
    #saving the trained model
    joblib.dump(model, model_path)
    print("Model persisted at " + model_path)
    print()

    
    y_pred_test = model.predict(X_test)
    test_acc = accuracy_score(y_test,y_pred_test)
    test_rep = classification_report(y_test,y_pred_test)

    print()
    print("---- METRICS RESULTS FOR TESTING DATA ----")
    print()
    print("Total Rows are: ", X_test.shape[0])
    print('[TESTING] Model Accuracy is: ', test_acc)
    print('[TESTING] Testing Report: ')
    print(test_rep)
