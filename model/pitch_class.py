import numpy as np
import pandas as pd

from joblib import load, dump

class Pitch():
    def __init__(self):
        self.encoder_oh = {}

    def pitch_data(self, data:pd.DataFrame, y_name:str=None, strat:bool=False, normed:str=None, seed:int=None, one_hot:str=None) -> pd.DataFrame:

        # Generate the RandomState for the sample
        rs = np.random.RandomState(seed=seed)
    
        # One-hot encoding
        if one_hot:
            for col in one_hot:
                self.encoder_oh[col] = data[col].unique()
                dummies = pd.get_dummies(data[col], prefix=col).astype(float)
                data = pd.concat([data, dummies], axis=1)
                data.drop(col, axis=1, inplace=True) # del to prevent from multi-colinearity
        
        if y_name:
            # Stratification of data
            if strat:      
                sorted_data = data.sort_values(by=y_name)
                class_counts = sorted_data[y_name].value_counts()
                train_counts = (class_counts * 0.8).astype(int)
                train_data = pd.DataFrame()

                for label, count in train_counts.items():
                    label_data = sorted_data[sorted_data[y_name] == label]
                    sample_data = label_data.sample(n=count, random_state=rs)
                    train_data = pd.concat([train_data, sample_data])

                test_data = data.drop(train_data.index)
            else :          # No stratified data
                # create a 80/20 ratio sample for random train and test data
                train_data = data.sample(frac=0.8, random_state=rs)
                test_data = data.drop(train_data.index)

            x_train = np.array(train_data.drop(y_name, axis=1))
            y_train = np.array(train_data[y_name])
            x_test = np.array(test_data.drop(y_name, axis=1))
            y_test = np.array(test_data[y_name])
            
        else:
            x_train = np.array(data)
            x_test = 0

        # Data normalization
        if normed:
            means = {}
            stds = {}
            for col in normed:
                means[col] = x_train[:, data.columns.get_loc(col)].mean()
                stds[col] = x_train[:, data.columns.get_loc(col)].std()
                
                if stds[col] < 1e-10:  # if std is too low
                    x_train[:, col_index] -= means[col]
                    x_test[:, col_index] -= means[col]

                    x_train[:, data.columns.get_loc(col)] = (x_train[:, data.columns.get_loc(col)] - means[col]) / stds[col]
                    x_test[:, data.columns.get_loc(col)] = (x_test[:, data.columns.get_loc(col)] - means[col]) / stds[col]

        if y_name :
            return x_train, y_train, x_test, y_test
        else:
            return x_train
        
        
    def save(self, filepath):
        dump(self.encoder_oh, filepath)
    
    def load(self, filepath):
        self.encoder_oh = load(filepath)
    
    def encode(self, data: pd.DataFrame) -> pd.DataFrame:
        for col, unique_values in self.encoder_oh.items():
            for unique_value in unique_values:
                data[f"{col}_{unique_value}"] = (data[col] == unique_value).astype(float)
            data.drop(col, axis=1, inplace=True)
        return data