import pandas as pd
import os 
import logging
from sklearn.model_selection import train_test_split

# Ensure the "logs" directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configure the logger
logger = logging.getLogger('data_ingestion')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_file_path = os.path.join(log_dir, 'data_ingestion.log') 
file_handler = logging.FileHandler(log_file_path)   
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')       
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_data(data_path: str) -> pd.DataFrame:
    """
    Load the data from the given URL.
    
    """
    try:
        df = pd.read_csv(data_path)
        logger.info("Data loaded successfully")
        return df
    except Exception as e:  
        logger.error(f"Error loading data: {str(e)}")
        raise e
    
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data.
    
    """
    try:
        df.drop(columns = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace = True, axis=1)
        df.rename(columns = {'v1': 'target', 'v2': 'text'}, inplace = True)
        logger.info("Data preprocessed successfully")
        return df
    except KeyError as e:
        logger.error(f"Error preprocessing data: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error preprocessing data: {str(e)}")
        raise e
    
def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str):
    """Save the train and test datasets to the given path."""
    try:
        raw_data_path = os.path.join(data_path, "raw")
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        logger.info("Data saved successfully")
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise e
    

def main():
    try:
        test_size = 0.2
        df = load_data('experiments\spam.csv')
        final_df = preprocess_data(df)
        train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=42)
        save_data(train_data, test_data, './data')
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise e
    
if __name__ == "__main__":
    main()



    
    
    
