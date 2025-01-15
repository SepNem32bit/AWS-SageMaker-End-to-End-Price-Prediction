# Mobile Price Prediction with AWS SageMaker

This project demonstrates an end-to-end machine learning workflow for predicting mobile prices using AWS SageMaker. It includes data preprocessing, model training, deployment, and testing.

## Workflow

### Data Preparation
- Load and preprocess the dataset (`mobile_prices.csv`).
- Split the data into training and testing sets.
- Upload the datasets to an S3 bucket.

### Model Training
- Train a Random Forest model using SageMaker's SKLearn Estimator.
- Save the trained model to S3.

### Model Deployment
- Deploy the model to a SageMaker endpoint for inference.

### Testing
- Use the deployed endpoint to make predictions on the test data.
- Clean up resources by deleting the endpoint.