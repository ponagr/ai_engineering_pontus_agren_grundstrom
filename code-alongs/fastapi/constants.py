from pathlib import Path

DATA_PATH = Path(__file__).parents[2] / "data" #"/Sales.csv"

if __name__ == "__main__":
    print(DATA_PATH)