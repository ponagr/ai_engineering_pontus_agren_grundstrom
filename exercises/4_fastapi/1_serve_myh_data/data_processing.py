import json
from fastapi.responses import JSONResponse


class DataExplorer:
    def __init__(self, df, limit=100):
        self._df_full = df
        self._df = df.head(limit)
    
    @property
    def df(self):
        return self._df
    
    @property
    def df_full(self):
        return self._df_full
    
    def summary(self):
        self._df = self.df_full.describe().drop("count").T.reset_index()
        return self.json_response()
    
    
    def filter(self, school, field):
        self._df = self.df_full
        if school:
            self._df = self.df[self.df["Utbildningsanordnare administrativ enhet"].str.contains(school, case=False)]
        if field:
            self._df = self.df[self.df["Utbildningsområde"].str.contains(field, case=False)]
        
        return self.json_response()
    
    
    def kpis(self, column):
        self._df = self.df_full
        
        if column.casefold() in self._df.columns.str.casefold():
            # hitta rätt faktisk kolumn (behöver pga casefold)
            column = [c for c in self._df.columns if c.casefold() == column.casefold()][0]
            new_df = self._df.groupby(column)["Beslut"].value_counts().reset_index()
                        # df
            new_df = new_df.pivot(
                index=column, 
                columns="Beslut", 
                values="count"
            ).reset_index()

            # byt namn på kolumner om du vill
            new_df = new_df.rename(columns={
                "Avslag": "Antal Avslag",
                "Beviljad": "Antal Beviljade"
            })
            json_data = new_df.to_json(orient="records")
            return JSONResponse(json.loads(json_data)) 
        
        return self.summary()
        
            # för varje skola, % på hur många beviljade, baserat på sökta utbildningsomgångar.sum()/beviljade utbildningsomgångar, och sökta/beviljade platser totalt
            # mest avslagna/beviljade ansökningar
    
    def json_response(self):
        json_data = self.df.to_json(orient="records")
        return JSONResponse(json.loads(json_data))


# utbildningsområde: str
# sun5_inriktning: str
# sun5_inriktning_namn: str
# utbildningsnamn: str
# beslut: str
# diarienummer: str
# flera_kommuner: str
# antal_kommuner: int
# län: str
# kommun: str
# yh-poäng: int
# studieform: str
# studietakt_%: int
# typ_av_examen: str
# seqf_nivå: float
# smalt_yrkesområde: str
# utbildningsanordnare_administrativ_enhet: str
# huvudmannatyp: str
# sökta_utbildningsomgångar: int
# beviljade_utbildningsomgångar: int
# sökta_platser_per_utbildningsomgång: int
# sökta_platser_totalt: int
# beviljade_platser_utbildningsomgång_1: int
# beviljade_platser_utbildningsomgång_2: int
# beviljade_platser_utbildningsomgång_3: int
# beviljade_platser_utbildningsomgång_4: int
# beviljade_platser_utbildningsomgång_5: int
# beviljade_platser_totalt: int


# def read_excel(filename=FILE_NAME, nr=3):
#     df = pd.read_excel(FOLDER_PATH/filename, sheet_name=f"Tabell {nr}", header=5)
#     df.columns = df.columns.str.strip().str.replace("\n", " ")
#     # data.columns = (data.columns.str.replace(" ", "_", regex=False).str.replace("-", "_", regex=False).str.replace("_%", "").str.strip().str.casefold())
#     return df.drop(columns=['Diarienummer','SeQF nivå','Sökta platser per utbildningsomgång','Beviljade platser utbildningsomgång 1','Beviljade platser utbildningsomgång 2','Beviljade platser utbildningsomgång 3','Beviljade platser utbildningsomgång 4','Beviljade platser utbildningsomgång 5'])


# def tabell_data():
#     df = read_excel()
#     return df.to_dict(orient="records")
    

# class Tabell(BaseModel):
#     utbildningsområde: str
#     sun5_inriktning: str
#     sun5_inriktning_namn: str
#     utbildningsnamn: str
#     beslut: str
#     flera_kommuner: str
#     antal_kommuner: int
#     län: str
#     kommun: str
#     yh_poäng: int
#     studieform: str
#     studietakt: int
#     typ_av_examen: str
#     utbildningsanordnare_administrativ_enhet: str
#     huvudmannatyp: str
#     sökta_utbildningsomgångar: int
#     beviljade_utbildningsomgångar: int
#     sökta_platser_totalt: int
#     beviljade_platser_totalt: int

# class Tabell(BaseModel):
#     diarienummer: str
#     utbildningsområde: str
#     utbildningsnamn: str
#     sun5_inriktning_namn: str
#     beslut: str
#     flera_kommuner: str
#     antal_kommuner: int = Field(gt=-1)
#     län: str
#     kommun: str
#     sökta_platser_totalt: int = Field(gt=-1)
#     beviljade_platser_totalt: int = Field(gt=-1)

# class TabellList(BaseModel):
#     tabell_nr: int = Field(gt=0, lt=5)
#     information: list[Tabell]