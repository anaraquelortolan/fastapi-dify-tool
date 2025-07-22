from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# Verifica se o arquivo existe
CSV_PATH = "BI_Eventos.csv"
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    df["competencia"] = pd.to_datetime(df["competencia"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
else:
    df = pd.DataFrame(columns=["nome_beneficiario", "valor", "competencia"])

class FiltroEntrada(BaseModel):
    data_inicio: Optional[str] = None
    data_fim: Optional[str] = None
    top_n: Optional[int] = 10

@app.post("/top_beneficiarios")
def top_beneficiarios(filtro: FiltroEntrada = Body(...)):
    if df.empty:
        return {"erro": "Arquivo CSV não encontrado ou vazio."}

    df_filtrado = df.copy()

    if filtro.data_inicio:
        data_ini = pd.to_datetime(filtro.data_inicio)
        df_filtrado = df_filtrado[df_filtrado["competencia"] >= data_ini]

    if filtro.data_fim:
        data_fim = pd.to_datetime(filtro.data_fim)
        df_filtrado = df_filtrado[df_filtrado["competencia"] <= data_fim]

    resultado = (
        df_filtrado.groupby("nome_beneficiario")["valor"]
        .sum()
        .reset_index()
        .sort_values(by="valor", ascending=False)
        .head(filtro.top_n)
    )

    return {
        "total_eventos": len(df_filtrado),
        "top_beneficiarios": resultado.to_dict(orient="records")
    }

@app.get("/")
def root():
    return {"status": "API está rodando"}
