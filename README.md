# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview

-   **Name**: messy_population_data.csv
-   **Rows**: 125718
-   **Columns**: 5

### Column Details

| Column Name   | Data Type | Non-Null Count | #Unique Values | Mean      |
|---------------|-----------|----------------|----------------|-----------|
| income_groups | object    | 119412         | 9              | \-        |
| age           | float64   | 119495         | 102            | 50.00     |
| gender        | float64   | 119811         | 4              | 1.57      |
| year          | float64   | 119516         | 170            | 2025      |
| population    | float64   | 119378         | 114926         | 111298303 |

### Identified Issues

1.  **Errors (invalid values)**
    -   Description: Invalid data entries such as invalid years, or a third category for gender, or typos in income_groups column.
    -   Affected Column(s): 'income_groups', 'gender', 'year'
    -   Example: 'income_groups' = 'high_income_typo', 'gender' = 3, 'year' = 2025
    -   Potential Impact: Distorts the accuracy of the dataset and affects analysis results.
2.  **Duplicates**
    -   Description: Duplicated rows which means exact repeated rows.
    -   Affected Column(s): All, there are 5444 duplicated row.
    -   Example: -
    -   Potential Impact: Increases dataset size unnecessarily and leads to skewed analysis.
3.  **Missing values**
    -   Description: Missing values such as NaN.
    -   Affected Column(s): 'age', 'year', 'population'
    -   Example: 'year' = NaN
    -   Potential Impact: Reduces the completeness and reliability of the dataset.
4.  **Outliers**
    -   Description: Extreme values (i.e. data point with values \> Q3 + 1.5 IQR or \< Q1 - 1.5IQR).
    -   Affected Column(s): 'population', 'year'
    -   Example: 'population' = 32930428000
    -   Potential Impact: Distorts the central tendency and variability of the dataset.
5.  **Inappropriate Data Types**
    -   Description: Some variables should be categorical but are floats for example.
    -   Affected Column(s): 'income_groups', 'gender', 'year', 'population'
    -   Example: 'gender' type should be category instead of float64
    -   Potential Impact: Prevents proper analysis and categorization of data.

## 2. Data Cleaning Process

### Issue 1: Errors (invalid values)

-   **Cleaning Method**: Replacing the errors of a column with column mode or median (of corrected values) or corrected version of the error (e.g. fixing the typo) or random values from the existing values.

-   **Implementation**:

    ``` python
    # Impute errors in year (values > 2024) with a random value (of years <= 2024)
    np.random.seed(42)
    df.loc[df['year'] > 2024, 'year'] = np.random.choice(df.loc[df['year'] <= 2024, 'year'])

    # Impute errors in gender (values other than 1,2) with mode (of correct values)
    df.loc[~df['gender'].isin([1,2]), 'gender'] = df.loc[df['gender'].isin([1,2]), 'gender'].mode()[0]

    # Impute errors in incom_groups (e.g. typos) with corrected values.
    # Remove the '_typo' part from values in the 'income_groups' column
    df['income_groups'] = df['income_groups'].str.replace('_typo', '')
    ```

-   **Justification**:Correcting errors improves data accuracy and ensures valid entries for analysis.

-   **Impact**:

    -   Rows affected: 'year' : 60211 rows (greater than 2024),

        'gender': 6286 rows (equal to 3),

        'income_group': 5959 rows contain a typo).

    -   Data distribution change: Slight shifts in the distribution of gender, year, and income groups due to the corrections.

### Issue 2: Duplicates

-   **Cleaning Method**: Removing (dropping) duplicated (repeated) rows.

-   **Implementation**:

    ``` python
    # Number of duplicated rows
    print("Duplicates rows:", df.duplicated().sum())
    # Remove duplacates
    df = df.drop_duplicates()
    ```

-   **Justification**: Removing duplicates prevents skewed results and unnecessary row inflation.

-   **Impact**:

    -   Rows affected: 5513 rows

    -   Data distribution change: Slight reduction in row count, but no significant changes in distribution.

### Issue 3: Missing values

-   **Cleaning Method**: Replacing the missing values in columns with numeric data values with median and in columns with categorical values with mode.

-   **Implementation**:

    ``` python
    # Missing data counts per column
    print("Missing data per column:")
    print(df.isnull().sum())

    # Handle missing values
    for col in df:
            if df[col].dtype == 'float':
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
    ```

-   **Justification**: Filling missing values ensures completeness without significantly altering the data’s central tendency.

-   **Impact**:

    -   Rows affected: 'income_groups': 6064 rows with missing values,

        'age': 5906 rows with missing values,

        'gender': 0 rows with missing values,

        'year' : 5999 rows with missing values,

        'population': 4048 rows with missing values.

    -   Data distribution change: Minor changes in median and mode due to filling missing values.

### Issue 4: Outliers

-   **Cleaning Method**: Replacing the errors of a column with column mode or median (of correct values) or corrected version of the error (e.g. fixing the typo).

-   **Implementation**:

    ``` python
    # Outliers of a column (data points with z scores less than -3 or higher than 3)
    for col in df:
        if df[col].dtype == 'float':
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            outliers = len(df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)])
            print(f"{col} have {outliers} outliers.")

    # Remove outliers present in the population and year columns
    for col in df[['year', 'population']]:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        df = df[~((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr))]
    ```

-   **Justification**: Removing outliers ensures that extreme values do not distort the overall analysis.

-   **Impact**:

    -   Rows affected: 'year': 4612 rows with outliers, 'population': 2898 rows with outliers

    -   Data distribution change: Removal of extreme values leads to a more representative dataset.

### Issue 5: Inappropriate Data Types

-   **Cleaning Method**: Converting data types of the columns to the suitable types.

-   **Implementation**:

    ``` python
    # Convert data types
    df = df.astype({'year': 'int', 'gender': 'int', 'population': 'int'})
    df = df.astype({'gender': 'category', 'income_groups': 'category'})
    ```

-   **Justification**: Ensures proper analysis and optimizes data storage by using appropriate data types.

-   **Impact**:

    -   Rows affected: All rows.

    -   Data distribution change: No changes, but improved performance for categorical operations.

## 3. Final State Analysis

### Dataset Overview

-   **Name**: cleaned_population_data.csv (or whatever you named it)
-   **Rows**: 114291
-   **Columns**: 5

### Column Details

| Column Name   | Data Type | Non-Null Count | #Unique Values | Mean    |
|---------------|-----------|----------------|----------------|---------|
| income_groups | category  | 114291         | 4              | \-      |
| age           | float64   | 114291         | 101            | 50.27   |
| gender        | category  | 114291         | 2              | \-      |
| year          | int64     | 114291         | 71             | 2000    |
| population    | int64     | 114291         | 109288         | 9178508 |

### Summary of Changes

-   **Major changes made to the dataset**:
    1.  Fixed invalid values in 'year', 'gender', and 'income_groups'.
    2.  Removed 5513 duplicate rows.
    3.  Filled missing values in 'income_groups', 'age', 'year', and 'population' columns.
    4.  Removed 4612 outliers from 'year' and 2898 outliers from 'population'.
    5.  Converted 'income_groups' and 'gender' columns to categorical data types.
-   **Significant changes in data distribution**:
    1.  Reduction in the range of values for 'year' and 'population' due to the removal of outliers.
    2.  Minor shifts in the median of 'age' and 'population' due to handling missing values.
    3.  Improved data consistency and accuracy, particularly in 'income_groups' and 'gender' after error correction.
