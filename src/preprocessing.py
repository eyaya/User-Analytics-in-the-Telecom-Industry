import sys

import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join('./')))
from logger import Logger


class PreProcess:
    def __init__(self):
        """Initialize the PreProcess class.

        Args:
            df (pd.DataFrame): dataframe to be preprocessed
        """
        try:
            self.logger = Logger("preprocessing.log").get_app_logger()
            self.logger.info('Successfully Instantiated PreProcess Class Object')
        except Exception:
            self.logger.exception('Failed to Instantiate Preprocessing Class Object')
            sys.exit(1)

    def convert_to_datetime(self, df:pd.DataFrame, column: str) ->pd.DataFrame:
        """Convert a column to a datetime data type.

        Args:
            df (pd.DataFrame): dataframe to be preprocessed
            column (str): dataframe column to be converted to datetime
        """
        try:
            df[column] = pd.to_datetime(df[column], errors='coerce')
            self.logger.info('Converted datetime columns to datetime.')
        except Exception:
            self.logger.info('Unable to convert the column to datime.')
            sys.exit(1)
        return df

    def convert_to_float(self, df:pd.DataFrame, column: str) ->pd.DataFrame:
        """Convert column to float datatype.

        Args:
            df (pd.DataFrame): dataframe to be preprocessed
            column (str): Column to be converted to float datatype
        """
        try:
            df[column] = df[column].astype(float)
            self.logger.info('Successfully converted to float columns')
        except:
            self.logger.info('Coud not convert the column to float data type')
            sys.exit(1)
            
        return df
    
    def convert_to_str(self, df:pd.DataFrame, column: str) ->pd.DataFrame:
        """Convert column to float datatype.

        Args:
            df (pd.DataFrame): dataframe to be preprocessed
            column (str): Column to be converted to float datatype
        """
        try:
            df[column] = df[column].astype(str)
            self.logger.info('Successfully converted to float columns')
        except:
            self.logger.info('Coud not convert the column to float data type')
            sys.exit(1)
            
        return df


    def drop_columns(self, df:pd.DataFrame, percentage: float) ->pd.DataFrame:
        """Drop variables based on a percentage.

        Args:
            df (pd.DataFrame): dataframe to be preprocessed
            percentage(int): Percentage of variables to be dropped
        """
        df_before_filling = df.copy()
        df = df[df.columns[df.isnull().mean() < 0.3]]
        columns_to_drop = df.columns[df.isnull().mean() > 0]
        print(columns_to_drop)
        """
        try:
            old_df = df.copy()
            # Calculate the percentage of null values in each column
            null_percentages = (df.isnull().sum() / len(df)) * 100
            
            # Filter columns where null percentage is greater than or equal to percentage
            columns_to_drop = null_percentages[null_percentages >= percentage].index
            # Drop columns
            df.drop(columns=columns_to_drop, inplace=True)
            self.logger.info(f"Columns with {percentage}% null values dropped")
        except Exception:
            self.logger(f"Unable to drop columns with {percentage}% null values")
            sys.exit(1)
        """
        return df, df_before_filling, columns_to_drop

    def clean_feature_name(self, df):
        """Clean labels of the dataframe.

        Args:
            df (pd.DataFrame): dataframe to be preprocessed
        """
        try:
            df.columns = [column.replace(' ', '_').lower() for column in df.columns]
            self.logger.info('Cleaned feature names')
        except Exception:
            self.logger.info("Unable to clean feature names")
            sys.exit(1)
        return df

    def rename_columns(self, df: pd.DataFrame, column: str, new_column: str):
        """Rename a column.

        Args:
            df (pd.DataFrame): dataframe to be preprocessed
            column (str): column to be renamed
            new_column (str): New column name
        """
        df[column] = df[column].rename(new_column)
        dfRenamed = df.rename({column: new_column}, axis=1)
        return dfRenamed
    def missing_values_percentage(self,df):
        total_missing = df.isnull().sum().sort_values(ascending=False)
        percentage_missing = (total_missing / len(df)) * 100
        
        missing_value_df = pd.DataFrame({
            'Total Missing Values': total_missing,
            'Percentage Missing': percentage_missing
        })
        
        return missing_value_df

    def fill_nulls_with_method(self, df, method):
        """Fill numerical variables.

        Args:
            df (pd.DataFrame): dataframe to be preprocessed
        """
        try:
            if method == 'mean' or method == 'median':
                if method == "mean":
                    num_cols = df.select_dtypes(include=np.number).columns
                    df.loc[:, num_cols] = df.loc[:, num_cols].fillna(
                        df.loc[:, num_cols].mean())
                else:
                    num_cols = df.select_dtypes(include=np.number).columns
                    df.loc[:, num_cols] = df.loc[:, num_cols].fillna(
                        df.loc[:, num_cols].median())
                    
            elif method == 'mode':
                cat_cols = df.select_dtypes(exclude=np.number).columns
                df.loc[:, cat_cols] = df.loc[:, cat_cols].fillna(
                        df.loc[:, cat_cols].mode().iloc[0])
                    
            else:
                df.fillna(method=method, inplace=True)
                
            self.logger.info(f'The DataFrame was imputated successfully with method {method}.')
        except Exception:
            self.logger.info(f"Unable to imputet the DataFrame with {method}.")
            sys.exit(1)
            
        return df
    
    def num_outliers(self,col):
        thres = 3
        mean = np.mean(col)
        std = np.std(col)
        # print(mean, std)
        n = 0
        for i in col:
            z_score = (i-mean)/std
            if (np.abs(z_score) > thres):
                n +=1
        return n
    
    def fix_outlier(self, df:pd.DataFrame, column:float):
        df[column] = np.where(df[column] > df[column].quantile(0.95), df[column].median(),df[column])

        return df[column]
    
    def logscale(self, df: pd.DataFrame, cols):
        for col in cols:
            df[col] = np.log(df[col])
        return df
    
