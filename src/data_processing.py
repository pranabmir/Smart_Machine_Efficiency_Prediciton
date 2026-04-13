import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from  config.paths_config import *

logger  = get_logger(__name__)

class DataProcessing:
    def __init__(self,input_path,output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None
        self.features = None

        os.makedirs(os.path.join(self.output_path),exist_ok = True)
        logger.info("Data processing initialized")
    
    def load_data(self):
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info("Data Successfully read..")
        except:
            logger.error(f"Error while loading the data")
            raise CustomException("Failed to load data")
    def preprocess(self):
        try:
            self.df["Timestamp"] = pd.to_datetime(self.df["Timestamp"] , errors='coerce')
            categorical_cols = ['Operation_Mode','Efficiency_Status']
            for col in categorical_cols:
                self.df[col] = self.df[col].astype('category')

            self.df["Year"] = self.df["Timestamp"].dt.year
            self.df["Month"] = self.df["Timestamp"].dt.month
            self.df["Day"] = self.df["Timestamp"].dt.day

            self.df["Hour"] = self.df["Timestamp"].dt.hour

            self.df.drop(columns=["Timestamp","Machine_ID"] , inplace=True)

            columns_to_encode = ["Efficiency_Status","Operation_Mode"]
            for col in columns_to_encode:
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col])

            logger.info("All basic data preprocessing done..")
        
        except Exception as e:
            logger.error(f"Error while preprocessing data {e}")
            raise CustomException("Failed to preprocess data",e)
    def split_data(self):
        try:
            self.features = [
                'Operation_Mode', 'Temperature_C', 'Vibration_Hz',
                'Power_Consumption_kW', 'Network_Latency_ms', 'Packet_Loss_%',
                'Quality_Control_Defect_Rate_%', 'Production_Speed_units_per_hr',
                'Predictive_Maintenance_Score', 'Error_Rate_%','Year', 'Month', 'Day', 'Hour'
            ]

            X = self.df[self.features]
            y = self.df["Efficiency_Status"]
            X_train , X_test , y_train , y_test = train_test_split(X,y, test_size=0.2 , random_state=42 , stratify=y)
            logger.info("Data splitted successfully")
            return X_train , X_test , y_train , y_test
        except Exception as e:
            logger.error(f"Error while splitting the data {e}")
            raise CustomException("Failed to split then data",e)
    
    def scale_data(self,X_train , X_test , y_train , y_test):
        try:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            logger.info("Data scaled successfully")
            return X_train_scaled , X_test_scaled , y_train , y_test
        except Exception as e:
            logger.error(f"Error while scaling the data {e}")
            raise CustomException("Failed to scaling the data",e)
    
    def save_data(self,X_train , X_test , y_train , y_test):
        try:
            joblib.dump(X_train , os.path.join(self.output_path , "X_train.pkl"))
            joblib.dump(X_test , os.path.join(self.output_path , "X_test.pkl"))
            joblib.dump(y_train , os.path.join(self.output_path , "y_train.pkl"))
            joblib.dump(y_test , os.path.join(self.output_path , "y_test.pkl"))
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error while saving the data {e}")
            raise CustomException("Failed to saving the data",e)
    
    def run(self):
        self.load_data()
        self.preprocess()
        X_train , X_test , y_train , y_test = self.split_data()
        X_train , X_test , y_train , y_test = self.scale_data(X_train , X_test , y_train , y_test)
        self.save_data(X_train , X_test , y_train , y_test)
        logger.info("Preprocessing Completed")

if __name__ =="__main__":
    processor = DataProcessing(DATA_PATH,PROCESSED_DATA_PATH)
    processor.run()