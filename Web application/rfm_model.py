import pandas as pd
from datetime import timedelta

def compute_rfm(dataframe, customer_col, date_col, revenue_col):
    # Convert the date column to datetime
    dataframe[date_col] = pd.to_datetime(dataframe[date_col])

    # Define the snapshot date for recency calculation
    snapshot = dataframe[date_col].max() + timedelta(days=1)

    # Aggregate data to compute Recency, Frequency, and Monetary values
    rfm_table = dataframe.groupby(customer_col).agg({
        date_col: lambda dates: (snapshot - dates.max()).days,
        customer_col: 'count',
        revenue_col: 'sum'
    })

    rfm_table.rename(columns={
        date_col: 'Recency',
        customer_col: 'Frequency',
        revenue_col: 'Monetary'
    }, inplace=True)

    # Assign R, F, M scores using quintiles
    rfm_table['R_Score'] = pd.qcut(rfm_table['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm_table['F_Score'] = pd.qcut(rfm_table['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm_table['M_Score'] = pd.qcut(rfm_table['Monetary'], 5, labels=[1, 2, 3, 4, 5])

    # Create combined RFM segment
    rfm_table['RFM_Code'] = rfm_table['R_Score'].astype(str) + \
                             rfm_table['F_Score'].astype(str) + \
                             rfm_table['M_Score'].astype(str)

    return rfm_table
