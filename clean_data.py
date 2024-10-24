"""
This code cleans data!
"""

import pandas as pd
import numpy as np
import argparse
import tqdm
import datetime

def main():
    # Load data
    df = pd.read_csv('messy_population_data.csv')
    
    # Data summary
    print(df.info())
    print(df.describe())

    # Errors in data
    # years > 2024 
    print(f"There are {(df['year'] > 2024).sum()} values highere than 2024 in 'year' column.")
    # Impute errors in year (values > 2024) with median(of years <= 2024)
    np.random.seed(42)
    df.loc[df['year'] > 2024, 'year'] = np.random.choice(df.loc[df['year'] <= 2024, 'year'])

    # Impute errors in gender (values other than 1,2) with mode
    df.loc[~df['gender'].isin([1,2]), 'gender'] = df.loc[df['gender'].isin([1,2]), 'gender'].mode()[0]

    # Remove the '_typo' part from values in the 'income_groups' column
    df['income_groups'] = df['income_groups'].str.replace('_typo', '')

    # Number of duplicated rows
    print("Duplicates rows:", df.duplicated().sum())
    # Remove duplacates
    df = df.drop_duplicates()

    # Missing data counts per column
    print("Missing data per column")
    print(df.isnull().sum())

    # Handle missing values
    for col in df:
            if df[col].dtype == 'float':
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])

    # Outliers of a column (data points with z scores less than -3 or higher than 3)
    for col in df:
        if df[col].dtype == 'float':
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            outliers = len(df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)])
            print(f"{col} have {outliers} outliers.")

    # Remove outliers present in the population and year columns
    for col in df[['population', 'year']]:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        df = df[~((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr))]

    # Convert data types
    df = df.astype({'year': 'int', 'gender': 'int', 'population': 'int'})
    df = df.astype({'gender': 'category', 'income_groups': 'category'})

    # Document the results
    print("Data cleaning complete.")
    print(df.info())
    print(df.describe())

if __name__=="__main__":
    main()