import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv(r"C:\Users\Jonatas\Documents\Projetos\Projetos Portfolio\fraud-detection\data\transacoes.csv")

engine = create_engine("postgresql+psycopg2://postgres:jonatas12@localhost:54321/fraude_db")

df.to_sql("transacoes", engine, if_exists="append", index=False)

print("Dados inseridos no PostgreSQL!")
