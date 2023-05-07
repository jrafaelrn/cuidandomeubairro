import pandas as pd
from unidecode import unidecode

def undecode_text(dataFrame: pd.DataFrame, column: str) -> pd.DataFrame:
    dataFrame[column] = dataFrame[column].apply(unidecode)
    return dataFrame