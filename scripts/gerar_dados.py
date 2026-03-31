import pandas as pd
import random
from datetime import datetime, timedelta

dados = []

for i in range(2000):
    usuario = random.randint(1, 100)

    if random.random() < 0.05:
        valor = random.uniform(3000, 10000)
    else:
        valor = random.uniform(10, 1000)

    data = datetime.now() - timedelta(minutes=random.randint(0, 10000))
    local = random.choice(["BR", "US", "UK", "FR"])

    dados.append([usuario, round(valor, 2), data, local])

df = pd.DataFrame(dados, columns=["usuario_id", "valor", "data", "local"])

df.to_csv("data/transacoes.csv", index=False)

print("Dados gerados!")
