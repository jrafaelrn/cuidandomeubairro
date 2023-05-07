import pandas as pd

def lowercase_text(dataFrame: pd.DataFrame, column: str):
    dataFrame[column] = dataFrame[column].str.lower()
    return dataFrame