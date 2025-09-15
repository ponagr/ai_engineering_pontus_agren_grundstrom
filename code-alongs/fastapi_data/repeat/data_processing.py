from constants import DATA_PATH
import pandas as pd
from pprint import pprint
import json


df = pd.read_csv(DATA_PATH / "Sales.csv")

class DataExplorer:
    def __init__(self, limit=100):
        self._df = df.head(limit)
        self._df_full = df
        
    @property
    def df(self):
        return self._df

    
    def summary(self):
        self._df = self._df_full.describe().drop("count").T.drop(["Day", "Year"]).reset_index()
        
        return self
    
    
    def kpis(self, country):
        if country:
            df = self._df_full.query("Country.str.casefold() == @country.casefold()")

        return {
            "country": country.title(),
            "total_profit": str(df["Profit"].sum()),
            "total_cost": str(df["Cost"].sum()),
            "total_revenue": str(df["Revenue"].sum()),
            "number_of_purchases": str(len(df))
        }
    
    
    def json_response(self):
        json_data = self.df.to_json(orient="records")
        return json.loads(json_data)


if __name__ == "__main__":
    data_explorer = DataExplorer()
    
    pprint(data_explorer.json_response())