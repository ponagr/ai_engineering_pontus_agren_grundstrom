import os
import pandas as pd


def save_txt(file, file_path: str, folder_path: str = None):
    if folder_path:
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_path)
        
    with open(f"{file_path}", "w", encoding="utf-8") as f:
        f.write(file) 


def load_txt(file_path: str) -> str:
    with open(f"{file_path}", "r", encoding="utf-8") as f:
        return f.read()



def save_csv(df: pd.DataFrame, file_path: str, folder_path: str = None, index: bool = False):
    if folder_path:
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_path)
    df.to_csv(file_path, index=index, encoding="utf-8")


def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, encoding="utf-8")