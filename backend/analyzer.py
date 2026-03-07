import pandas as pd
import numpy as np

class DataAnalyzer:
    """
    A basic data analyzer for student projects using pandas and numpy.
    It takes a pandas DataFrame and generates insights about the data.
    """
    def __init__(self, df):
        self.df = df
        # Select only numerical columns for math operations to avoid errors
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()

    def get_descriptive_statistics(self):
        """
        1. Descriptive statistics generation
        Calculates mean, std, min, max, and quartiles for numerical columns.
        """
        if not self.numeric_cols:
            return {"message": "No numerical columns found to generate statistics."}
        
        # describe() creates a nice summary of numerical data
        stats = self.df[self.numeric_cols].describe().to_dict()
        return stats

    def get_missing_value_report(self):
        """
        2. Missing value report
        Counts how many missing (null/NaN) values are in each column.
        """
        missing_counts = self.df.isnull().sum()
        total_rows = len(self.df)
        
        report = {}
        for col, count in missing_counts.items():
            if count > 0:
                percentage = round((count / total_rows) * 100, 2)
                report[col] = {"missing_count": int(count), "percentage": percentage}
        
        if not report:
            return {"message": "No missing values found in the dataset!"}
            
        return report

    def get_correlation_matrix(self):
        """
        3. Correlation matrix computation
        Finds how numerically related different columns are to each other.
        Returns a dictionary representation of the matrix.
        """
        if len(self.numeric_cols) < 2:
            return {"message": "Need at least 2 numerical columns for correlation."}
            
        # Compute Pearson correlation matrix
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # Replace NaN with None so it can be converted to JSON properly by FastAPI later
        corr_matrix = corr_matrix.replace({np.nan: None})
        
        return corr_matrix.to_dict()

    def get_outlier_detection(self):
        """
        4. Outlier detection
        Uses the Interquartile Range (IQR) method to find extreme values (outliers) in numerical columns.
        """
        outliers_report = {}
        
        for col in self.numeric_cols:
            # Drop missing values before calculating IQR
            col_data = self.df[col].dropna()
            
            if len(col_data) < 4:
                continue # Not enough data to find meaningful outliers
                
            # Calculate Q1 (25th percentile) and Q3 (75th percentile)
            Q1 = np.percentile(col_data, 25)
            Q3 = np.percentile(col_data, 75)
            
            # Calculate Interquartile Range
            IQR = Q3 - Q1
            
            # Define lower and upper bounds for outliers
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Find the actual outlier values
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            
            if not outliers.empty:
                outliers_report[col] = {
                    "outlier_count": len(outliers),
                    "lower_bound": float(lower_bound),
                    "upper_bound": float(upper_bound),
                    # Provide a small sample of the outliers found
                    "sample_outliers": outliers.head(5).tolist() 
                }
                
        if not outliers_report:
            return {"message": "No significant outliers detected."}
            
        return outliers_report

    def get_column_summary(self):
        """
        5. Column-level analytical summary
        Provides basic info for every column (data type, unique values, missing values).
        """
        summary = {}
        
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            unique_count = self.df[col].nunique()
            missing_count = int(self.df[col].isnull().sum())
            
            summary[col] = {
                "data_type": dtype,
                "unique_values": unique_count,
                "missing_values": missing_count
            }
            
        return summary

    def get_data_quality_score(self):
        """
        6. Basic data quality scoring
        A simple score out of 100 representing how "clean" the data is.
        Deducts points for missing values.
        """
        total_cells = self.df.size
        # If the dataframe is completely empty
        if total_cells == 0:
            return {"score": 0, "grade": "F", "reason": "Dataset is completely empty."}

        total_missing = int(self.df.isnull().sum().sum())
        missing_percentage = (total_missing / total_cells) * 100
        
        # Start with 100 points
        score = 100
        
        # Deduct points based on the percentage of missing values.
        # e.g., if 10% of data is missing, deduct 20 points
        point_deduction = min(100, missing_percentage * 2) 
        
        score = max(0, int(score - point_deduction))
        
        # Assign a simple letter grade based on the score
        if score >= 90: grade = "A (Excellent)"
        elif score >= 80: grade = "B (Good)"
        elif score >= 70: grade = "C (Fair)"
        elif score >= 60: grade = "D (Poor)"
        else: grade = "F (Very Poor)"
            
        return {
            "score": score,
            "max_score": 100,
            "grade": grade,
            "total_missing_cells": total_missing,
            "missing_percentage": round(missing_percentage, 2)
        }

    def generate_full_report(self):
        """
        Runs all analysis functions and bundles them into one big dictionary.
        This is what the FastAPI endpoint will eventually return as JSON.
        """
        return {
            "row_count": len(self.df),
            "column_count": len(self.df.columns),
            "column_summary": self.get_column_summary(),
            "data_quality": self.get_data_quality_score(),
            "descriptive_statistics": self.get_descriptive_statistics(),
            "missing_values": self.get_missing_value_report(),
            "outliers": self.get_outlier_detection(),
            "correlation_matrix": self.get_correlation_matrix()
        }

# =====================================================================
# EXAMPLE USAGE (For the Backend Team implementing FastAPI)
# =====================================================================
if __name__ == "__main__":
    import json
    
    # 1. Provide an example CSV file
    # Usually, a FastAPI backend would read the uploaded file using pd.read_csv()
    print("Loading test data...")
    try:
        # Create a tiny dummy dataframe to test our code if no CSV exists
        df = pd.DataFrame({
            "Age": [25, 30, 35, 40, np.nan, 120, 28, 32], 
            "Salary": [50000, 60000, 75000, 90000, 55000, np.nan, 52000, 300000], # 300000 is an outlier
            "Department": ["IT", "HR", "IT", "Sales", "HR", "Sales", "IT", "HR"],
            "Experience_Years": [2, 5, 8, 12, np.nan, 40, 3, 7]
        })
        
        print(f"Dataframe created successfully with {len(df)} rows and {len(df.columns)} columns.\n")
        
        # 2. Feed the dataframe to our analyzer class
        analyzer = DataAnalyzer(df)
        
        # 3. Get the complete report
        report = analyzer.generate_full_report()
        
        # 4. Print the result nicely formatted (FastAPI will do this automatically via JSONResponse)
        print("--- GENERATING FULL ANALYTICAL REPORT ---\n")
        print(json.dumps(report, indent=4))
        
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
