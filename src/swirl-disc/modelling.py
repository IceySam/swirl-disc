import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

class Modelling:
    """
    A class for data cleaning and machine learning model building.
    """

    def __init__(self):
        """
        Initializes the Modelling class.
        """
        pass
    
    def clean(self, df, columns_to_drop=[], invalid_values=['', 'nan', '!@9#%8', '#F%$D@*&8'], column_types={}):
        """
        Cleans the input DataFrame by handling invalid values, dropping columns, and converting column types.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame to clean.
        columns_to_drop : list, optional
            Columns to drop from the DataFrame. Defaults to an empty list.
        invalid_values : list, optional
            List of invalid values to replace with NaN. Defaults to common placeholders.
        column_types : dict, optional
            Dictionary mapping column names to target data types. Defaults to an empty dictionary.

        Returns:
        --------
        pandas.DataFrame
            The cleaned DataFrame.
        """
        # Replace invalid string values with NaN
        df = df.map(
            lambda x: x if x is np.NaN or not isinstance(x, str) else str(x).strip('_')
        ).replace(invalid_values, np.NaN)

        # Drop specified columns
        if len(columns_to_drop) != 0:
            df.drop(columns=columns_to_drop, inplace=True, axis=1)

        # Convert columns to specified data types
        for column, dtype in column_types.items():
            if column in df.columns:
                df[column] = df[column].astype(dtype)

        return df
    
    def build_model(self, df, target_col):
        """
        Builds a machine learning model using a pipeline and evaluates its performance.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing features and target label (`is_credit_worthy`).

        Prints:
        -------
        - Training and test accuracy scores.
        - Classification report for the test set.
        - Cross-validation scores.
        """
        # Separate features and target variable
        x = df.drop([target_col], axis=1).values
        y = df[target_col].values

        # Split data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=50)
        
        self.test = x_test

        # Define a pipeline with preprocessing and model
        self.pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),  # Handle missing values
            ('scaler', StandardScaler()),  # Scale features
            ('random_forest', RandomForestClassifier(n_estimators=100, random_state=50, class_weight='balanced'))  # Random Forest with balanced class weight
        ])

        # Fit the pipeline on training data
        self.pipeline.fit(x_train, y_train)

        # Evaluate the model
        train_score = self.pipeline.score(x_train, y_train)  
        test_score = self.pipeline.score(x_test, y_test) 
        
        # Make predictions on the test set
        y_pred = self.pipeline.predict(x_test)
        
        # Print results
        dd = pd.DataFrame({"Y_test": y_test, "y_pred": y_pred})
        print(dd.head())  # Example of predictions vs true values
        
        print(f"Training Score: {train_score:.2f}")
        print(f"Test Score: {test_score:.2f}")

        print("Classification Report:\n", classification_report(y_test, y_pred))

        # Perform cross-validation
        cross_val_scores = cross_val_score(self.pipeline, x, y, cv=5)
        print(f"Cross-validation scores: {cross_val_scores}")
        print(f"Average Cross-validation score: {cross_val_scores.mean():.2f}")

