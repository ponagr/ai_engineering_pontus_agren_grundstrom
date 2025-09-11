import pandas as pd
from constants import FOLDER_PATH, FILE_NAME
from pydantic import BaseModel, Field
import json


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


def read_excel(filename=FILE_NAME, nr=3):
    df = pd.read_excel(FOLDER_PATH/filename, sheet_name=f"Tabell {nr}", header=5)
    df.columns = df.columns.str.strip().str.replace("\n", " ")
    # data.columns = (data.columns.str.replace(" ", "_", regex=False).str.replace("-", "_", regex=False).str.replace("_%", "").str.strip().str.casefold())
    return df.drop(columns=['Diarienummer','SeQF nivå','Sökta platser per utbildningsomgång','Beviljade platser utbildningsomgång 1','Beviljade platser utbildningsomgång 2','Beviljade platser utbildningsomgång 3','Beviljade platser utbildningsomgång 4','Beviljade platser utbildningsomgång 5'])


def tabell_data():
    df = read_excel()
    return df.to_dict(orient="records")
    

class Tabell(BaseModel):
    utbildningsområde: str
    sun5_inriktning: str
    sun5_inriktning_namn: str
    utbildningsnamn: str
    beslut: str
    flera_kommuner: str
    antal_kommuner: int
    län: str
    kommun: str
    yh_poäng: int
    studieform: str
    studietakt: int
    typ_av_examen: str
    utbildningsanordnare_administrativ_enhet: str
    huvudmannatyp: str
    sökta_utbildningsomgångar: int
    beviljade_utbildningsomgångar: int
    sökta_platser_totalt: int
    beviljade_platser_totalt: int

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