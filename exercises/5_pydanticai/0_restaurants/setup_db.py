#%%
from utils import query_duckdb

if __name__ == "__main__":
    query_duckdb("""
        CREATE TABLE IF NOT EXISTS restaurants (
            name TEXT,
            cuisine TEXT,
            price_level TEXT,
            rating TINYINT,
            opening_hours TEXT,
            location TEXT
        );
    """)
    
    print(query_duckdb("desc table restaurants;"))