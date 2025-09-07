import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def pairplot(df: pd.DataFrame, target: str):
    fig, ax = plt.subplots(1, figsize=(16,8), dpi=150)
    sns.pairplot(df, corner=True, hue=target, diag_kind="kde")

def heatmap(df: pd.DataFrame):
    fig, ax = plt.subplots(1, figsize=(16,8), dpi=150)
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    
def boxplot(df: pd.DataFrame):
    fig, ax = plt.subplots(1, figsize=(16,8), dpi=150)
    sns.boxplot(df, legend=True)

def scatterplot(df: pd.DataFrame, x: str, y: str, target: str):
    fig, ax = plt.subplots(1, figsize=(16,8), dpi=150)
    sns.scatterplot(data=df, x="balance", y="income", hue=target, alpha=.8)
    
