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
    
    # b) Make an API endpoint where you serve table 3 in JSON format for a read operation.
    # c) Make endpoints where you could filter out a particular school.
    # d) Make endpoints where you could filter out a particular field.
    def filter(self, school, field):
        self._df = self.df_full
        if school:
            self._df = self.df[self.df["Utbildningsanordnare administrativ enhet"].str.contains(school, case=False)]
        if field:
            self._df = self.df[self.df["Utbildningsområde"].str.contains(field, case=False)]
        
        return self.json_response()
    
    #e) Make endpoint for approved (beviljad) and one for not approved (avslag).
    def decision(self, approved: bool):
        if approved:
            df = self.df_full[self.df_full["Beviljade platser totalt"] > 0]
        else:
            df = self.df_full[self.df_full["Beviljade platser totalt"] == 0] 
        self._df = df
        
        return self.json_response()
    
    # f) Make an endpoint for some KPIs that you think is interesting for a particular stakeholder in mind.
    def kpis(self, column):
        if column:
            self._df = self.df_full
            if column.casefold() in self._df.columns.str.casefold():
                column = [c for c in self._df.columns if c.casefold() == column.casefold()][0]

                new_df = self._df.groupby(column)[["Sökta platser totalt", "Beviljade platser totalt"]].sum().reset_index()
                new_df["Beviljade platser %"] = round(new_df["Beviljade platser totalt"] / new_df["Sökta platser totalt"] * 100, 2)

                self._df = new_df.sort_values(by=["Beviljade platser %","Sökta platser totalt"], ascending=False)

        return self.json_response()  
        
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