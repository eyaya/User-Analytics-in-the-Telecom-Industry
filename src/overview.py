import sys

import numpy as np
import pandas as pd
from logger import Logger


class Overview:
    def __init__(self):
        """Initialize the Overview class.

        Args:
            df (pd.DataFrame): dataframe to be analyzed for users overview
        """
        try:
            self.logger = Logger("overview.log").get_app_logger()
            self.logger.info(
                'Successfully Instantiated Overview Class Object')
        except Exception:
            self.logger.exception(
                'Failed to Instantiate Overview Class Object')
            sys.exit(1)

    

    def percent_missing(self, df: pd.DataFrame)-> None:
        """Get the percentage of missing values in the dataset.

        Args:
            df (pd.DataFrame): a dataframe to be preprocessed

        Returns:
            pd.DataFrame: the dataframe
        """
        # get the size of the dataset
        data_size = df.size 

        # Count number of missing values per column
        missingCount = df.isnull().sum()

        # Calculate total number of missing values
        totalMissing = missingCount.sum()

        # Calculate percentage of missing values
        try:
            percentage = (totalMissing/data_size)*100
            self.logger.info("Calculated Percentage of missing values in the dataset")
        except Exception:
            self.logger.exception(
                'You provided empty dataframe')
            sys.exit(1)
        return round(percentage,2)

    def number_of_duplicates(self, df: pd.DataFrame) -> None:
        """Prints the number of duplicates in the dataset.

        Args:
            df (pd.DataFrame): Dataset to be analyzed
        """
        duplicated_entries = df[df.duplicated()]
        self.logger.info(
            'Number of duplicated fields calculated')
        print(duplicated_entries.shape)

    def get_skewness(self, df):
        """Return the skewness of the dataset.

        Args:
            df (pd.DataFrame): a dataframe to be analyzed
        """
        # calculate skewness
        skewness = df.skew(axis=0, skipna=True, numeric_only=True)
        self.logger.info('Skewness calculated')
        return skewness

    def get_decile(self, df: pd.DataFrame, column: str, decile: int, labels: list = []) -> pd.DataFrame:
        """Get the decile based on the column.

        Args:
            df (pd.DataFrame): Dataset to be used for Decile
            column (str): column to calculate the decile
            decile (int): number of decile
            labels (list, optional): Decile labels. Defaults to [].

        Returns:
            pd.DataFrame: Calculated decile
        """
        df['deciles'] = pd.qcut(df[column], decile, labels=labels)
        return df