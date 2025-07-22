from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Evento(BaseModel):
    beneficiario_id: int
    valor_pago: float

class Entrada(BaseModel):
    eventos: List[Evento]

@app.post("/calcular_total")
def calcular_total(data: Entrada):
    total = sum(evento.valor_pago for evento in data.eventos)
    return {"total_gasto": round(total, 2)}
