from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from datetime import datetime

app = FastAPI()

# Carrega o CSV uma vez ao iniciar
df = pd.read_csv("BI_Eventos.csv")
df["competencia"] = pd.to_datetime(df["competencia"])
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

class FiltroEntrada(BaseModel):
    data_inicio: Optional[str] = None  # formato: "2024-06-01"
    data_fim: Optional[str] = None
    top_n: Optional[int] = 10

@app.post("/top_beneficiarios")
def top_beneficiarios(filtro: FiltroEntrada = Body(...)):
    df_filtrado = df.copy()

    # Aplica filtros de data se fornecidos
    if filtro.data_inicio:
        data_ini = pd.to_datetime(filtro.data_inicio)
        df_filtrado = df_filtrado[df_filtrado["competencia"] >= data_ini]

    if filtro.data_fim:
        data_fim = pd.to_datetime(filtro.data_fim)
        df_filtrado = df_filtrado[df_filtrado["competencia"] <= data_fim]

    # Agrupa e soma
    resultado = (
        df_filtrado.groupby("nome_beneficiario")["valor"]
        .sum()
        .reset_index()
        .sort_values(by="valor", asc_

