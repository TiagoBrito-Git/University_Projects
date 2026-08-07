from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from datetime import date
from database import get_db

from auth import requer_operacao
from Model.ClientSubsystem.GestorClientes import GestorClientes
from Model.ClientSubsystem.ClienteDAO import ClienteDAO
from Model.ClientSubsystem.TrotineteDAO import TrotineteDAO

router = APIRouter(prefix="/trotinetes", tags=["Trotinetes"])

# --- Schema de resposta Pydantic ---
class TrotineteResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    serie: str           # Antes era numero_serie
    registado: date      # Antes era data_registo
    clienteId: int       # Antes era id_cliente

    class Config:
        from_attributes = True


class TrotineteCreate(BaseModel):
    marca: str
    modelo: str
    serie: str
    clienteId: int

# --- Dependency injection do GestorClientes ---


def _gestor(db=Depends(get_db)) -> GestorClientes:
    return GestorClientes(ClienteDAO(db), TrotineteDAO(db))

# --- GET /trotinetes ---
# -------------------------------------------------------
# 🔐 LISTAR TODAS AS TROTINETES
# -------------------------------------------------------
@router.get("/", response_model=List[TrotineteResponse])
def listar_trotinetes(
    gestor: GestorClientes = Depends(_gestor),
    _=Depends(requer_operacao("lerTrotinete"))
):
    trotinetes_models = gestor.listar_trotinetes()  
    
    return [
            TrotineteResponse(
                id=t.get_id(),
                marca=t.get_marca(),
                modelo=t.get_modelo(),
                serie=t.get_numero_serie(),    # Mapeia numero_serie -> serie
                registado=t.get_data_registo(), # Mapeia data_registo -> registado
                clienteId=t.get_id_cliente()   # Mapeia id_cliente -> clienteId
            ) for t in trotinetes_models
        ]


@router.post("/", status_code=201)
def criar_trotinete(
    dados: TrotineteCreate,
    gestor: GestorClientes = Depends(_gestor),
    _=Depends(requer_operacao("criarTrotinete")),
):
    try:
        sucesso = gestor.registar_trotinete(
            marca=dados.marca,
            modelo=dados.modelo,
            numero_serie=dados.serie,
            id_cliente=dados.clienteId,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not sucesso:
        raise HTTPException(
            status_code=400,
            detail="Erro ao criar trotinete. Verifique se o número de série já existe ou se o cliente é válido.",
        )
    return {"message": "Trotinete criada com sucesso!"}


@router.put("/{id}")
def editar_trotinete(
    id: int,
    dados: TrotineteCreate,
    gestor: GestorClientes = Depends(_gestor),
    _=Depends(requer_operacao("editarTrotinete")),
):
    try:
        t = gestor.consultar_trotinete(id)
        if t:
            sucesso = gestor.editar_trotinete(id, dados.marca, dados.modelo, dados.serie, dados.clienteId)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not t:
        raise HTTPException(status_code=404, detail=f"Trotinete com ID {id} não encontrada.")
    if sucesso is False:
        raise HTTPException(status_code=400, detail="Número de série já existe noutra trotinete.")
    return {"message": "Trotinete atualizada com sucesso!"}


@router.delete("/{id}", status_code=200)
def remover_trotinete(
    id: int,
    gestor: GestorClientes = Depends(_gestor),
    _=Depends(requer_operacao("removerTrotinete")),
):
    sucesso = gestor.remover_trotinete(id)
    if sucesso is False:
        raise HTTPException(status_code=404, detail=f"Trotinete com ID {id} não encontrada.")
    return {"message": "Trotinete removida com sucesso!"}