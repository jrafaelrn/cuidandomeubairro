import pandas as pd

def lowercase_text(dataFrame: pd.DataFrame, column: str):
    
    for index, row in dataFrame.iterrows():
        dataFrame.loc[index, column] = row[column].lower()
        
    return dataFrame




def test_lowercase_text():
    
    data_frame_test = pd.DataFrame({"a": ["A", "b", "C"]})
    data_frame_test = lowercase_text(data_frame_test, "a")
    #print(data_frame_test)
    
    

if __name__ == '__main__':
    test_lowercase_text()