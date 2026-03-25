import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# config da página
st.set_page_config(
    page_title="Fraud Detection",
    page_icon="🚨",
    layout="wide"
)

# auto refresh
st_autorefresh(interval=5000, key="refresh")

# carregar dados
df = pd.read_csv("data/transacoes.csv")
df["data"] = pd.to_datetime(df["data"])

# regras
df["risco"] = df["valor"].apply(lambda x: 50 if x > 3000 else 0)

def classificar(score):
    if score >= 50:
        return "ALTO_RISCO"
    elif score >= 20:
        return "MEDIO_RISCO"
    return "BAIXO_RISCO"

df["classificacao"] = df["risco"].apply(classificar)

# SIDEBAR
st.sidebar.title("⚙️ Configurações")

filtro = st.sidebar.multiselect(
    "Classificação",
    df["classificacao"].unique(),
    default=df["classificacao"].unique()
)

df = df[df["classificacao"].isin(filtro)]

# HEADER
st.markdown("## 🚨 Fraud Detection System")
st.markdown("Monitoramento em tempo real de transações suspeitas")

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Transações", len(df))
col2.metric("Fraudes", len(df[df["classificacao"] == "ALTO_RISCO"]))
col3.metric("Ticket Médio", f"R$ {df['valor'].mean():.2f}")
col4.metric("Maior Transação", f"R$ {df['valor'].max():.2f}")

st.divider()

# GRÁFICOS
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌎 Fraudes por País")
    st.bar_chart(df[df["classificacao"] == "ALTO_RISCO"]["local"].value_counts())

with col2:
    st.subheader("📈 Evolução Temporal")
    st.line_chart(df.groupby(df["data"].dt.date).size())

st.divider()

# INSIGHTS
st.subheader("🧠 Insights Automáticos")

fraudes = df[df["classificacao"] == "ALTO_RISCO"]

if len(fraudes) > 100:
    st.error("🚨 Pico anormal de fraudes detectado")
elif len(fraudes) > 50:
    st.warning("⚠️ Aumento moderado de fraudes")
else:
    st.success("✅ Sistema sob controle")

# TABELA
st.subheader("🔍 Transações Suspeitas")
st.dataframe(fraudes.sort_values(by="valor", ascending=False).head(20))