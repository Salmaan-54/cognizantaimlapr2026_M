#create polynomial regression model for the population dataset
import os
from pandas import pd
from sklearn.model_selection import train_test_split
from supervisedmlapp.configurations.conf import POPULATION_FILE_PATH
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
def polynomial_regression_model():
    # Load the dataset
    data = pd.read_csv(POPULATION_FILE_PATH)
    
    # Define features and target variable
    X = data[['Year']] # Features
    y = data['Population']  # Target variable

    #normalize the features
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = scaler.fit_transform(y.values.reshape(-1, 1))
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.3, random_state=42)
     
    # Create a polynomial regression model
    # we will use degree 2 for the polynomial regression
   
    polynomial_features = PolynomialFeatures(degree=2)
    X_train_poly = polynomial_features.fit_transform(X_train)
    X_test_poly = polynomial_features.transform(X_test)
    model = LinearRegression()
    # Fit the model to the training data
    # we will fit the model to the polynomial features
    # this will allow us to capture the non-linear relationship between the features and the target variable
    model.fit(X_train_poly, y_train)
    # Make predictions on the test set
    y_pred = model.predict(X_test_poly)
    # Evaluate the model
   
    mse = mean_squared_error(y_test, y_pred)**0.5
    r2 = r2_score(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    print(f'R^2 Score: {r2}')

