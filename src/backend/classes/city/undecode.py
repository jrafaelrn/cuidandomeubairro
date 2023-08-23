import pandas as pd
from unidecode import unidecode

def undecode_text(dataFrame: pd.DataFrame, column: str) -> pd.DataFrame:
    
    for index, row in dataFrame.iterrows():
        dataFrame.loc[index, column] = unidecode(row[column])
        
    return dataFrame