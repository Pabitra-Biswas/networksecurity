# from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
# from networksecurity.entity.config_entity import DataValidationConfig
# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging
# from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
# from scipy.stats import ks_2samp
# import pandas as pd
# import numpy as np
# import os,sys
# from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file


# class DataValidation:
#     def __init__(self,data_ingestion_artifact:DataValidationArtifact,
#                  data_validation_config:DataValidationConfig):
        
#         try:
#             self.data_ingestion_artifact=data_ingestion_artifact
#             self.data_validation_config= data_validation_config
#             self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
    
#     @staticmethod
#     def read_data(file_path)-> pd.DataFrame:
#         try:
#             return pd.read_csv(file_path)
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def validate_number_of_column(self,dataframe:pd.DataFrame)->bool:
#         try:
#             number_of_columns = len(self._schema_config)
#             logging.info(f'required num ber of columns : {number_of_columns}')
#             logging.info(f'Dataframe has columns : {len(dataframe)}')
#             if len(dataframe)==number_of_columns:
#                 return True
#             return False
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def defect_dataset_drift(self,base_df,current_df,threshold=0.05)-> bool:
#         try:
#             status = True
#             report = {}
#             for column in base_df.columns:
#                 d1=base_df[column]
#                 d2 = current_df[column]
                
#                 is_same_dist = ks_2samp(d1,d2)
#                 if threshold<=is_same_dist.pvalue:
#                     is_found=False
#                 else:
#                     is_found=True
#                     status=False
#                 report.update({column:{
#                     "p_value":float(is_same_dist.pvalue),
#                     "drift_status": is_found
#                 }
                    
#                 }
                    
#                 )
#             drift_report_file_path = self.data_validation_config.drift_report_file_path
            
#             ## Create directory
#             dir_path = os.path.dirname(drift_report_file_path)
#             os.makedirs(dir_path,exist_ok=True)
#             write_yaml_file(file_path=drift_report_file_path,content=report)
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
            
    
#     def initiate_data_validation(self) -> DataValidationArtifact:
        
        
        
#         try:
            
            
#             train_file_path = self.data_ingestion_artifact.trained_file_path
#             test_file_path = self.data_ingestion_artifact.test_file_path

#             ## Read the data from train and test
#             train_dataframe = DataValidation.read_data(train_file_path)
#             test_dataframe = DataValidation.read_data(test_file_path)

#             ## Validate number of columns
#             status = self.validate_number_of_column(dataframe=train_dataframe)
#             if not status:
                
                
#                 raise ValueError("Trained dataframe does not contain all required columns.")

#             status = self.validate_number_of_column(dataframe=test_dataframe)
#             if not status:
                
                
#                 raise ValueError("Test dataframe does not contain all required columns.")

#             ## Check data drift
#             status = self.defect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

#             ## Create directory
#             dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
#             os.makedirs(dir_path, exist_ok=True)

#             ## Save validated data
#             train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
#             test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

#             ## Return DataValidationArtifact
#             data_validation_artifact = DataValidationArtifact(
                
                
#                 validation_status=status,
#                 valid_train_file_path=self.data_validation_config.valid_train_file_path,
#                 valid_test_file_path=self.data_validation_config.valid_test_file_path,
#                 invalid_train_file_path=None,
#                 invalid_test_file_path=None,
#                 drift_report_file_path=self.data_validation_config.drift_report_file_path
#         )

#         return data_validation_artifact

#         except Exception as e:
            
            
#             raise NetworkSecurityException(e, sys)


from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os
import sys
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """Reads CSV file and returns a DataFrame."""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """Validates if the DataFrame has the required number of columns."""
        try:
            required_columns = len(self._schema_config["columns"])
            actual_columns = len(dataframe.columns)

            logging.info(f"Required number of columns: {required_columns}")
            logging.info(f"DataFrame has columns: {actual_columns}")

            return actual_columns == required_columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """Detects dataset drift using the Kolmogorov-Smirnov test."""
        try:
            drift_status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                ks_test = ks_2samp(d1, d2)
                drift_found = ks_test.pvalue < threshold

                if drift_found:
                    drift_status = False  # If any drift is found, set status to False

                report[column] = {
                    "p_value": float(ks_test.pvalue),
                    "drift_status": drift_found
                }

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return drift_status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        """Initiates the data validation process."""
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read the data
            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            # Validate number of columns
            if not self.validate_number_of_columns(train_dataframe):
                raise ValueError("Train dataset does not contain all required columns.")
            if not self.validate_number_of_columns(test_dataframe):
                raise ValueError("Test dataset does not contain all required columns.")

            # Check for dataset drift
            drift_status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            # Save validated data
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            # Return DataValidationArtifact
            return DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            

        except Exception as e:
            raise NetworkSecurityException(e, sys)
