from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from database import get_db

from auth import requer_operacao
from Model.StockSubsystem.GestorStock import GestorStock, PecaDAO


router = APIRouter(prefix="/stock", tags=["STOCK"])


class PecaResponse(BaseModel):
    codigo: int
    nome: str
    descricao: str
    fornecedor: str
    categoria: str
    stock: int
    stock_minimo: int
    preco: float

    class Config:
        from_attributes = True


class PecaCreate(BaseModel):
    nome: str
    descricao: str
    fornecedor: str
    categoria: str
    stock: int
    stock_minimo: int
    preco: float


class PecaAlter(BaseModel):
    nome: str
    descricao: str
    fornecedor: str
    categoria: str
    stock: int
    stock_minimo: int
    preco: float


def _gestor_stock(db=Depends(get_db)) -> GestorStock:
    return GestorStock(PecaDAO(db))


@router.get("/", response_model=List[PecaResponse])
def listar_pecas(
    gestor_pecas: GestorStock = Depends(_gestor_stock),
    _=Depends(requer_operacao("lerPeca")),
):
    pecas = gestor_pecas.listarPecas()
    return [
        PecaResponse(
            codigo=p.id,
            nome=p.nome,
            descricao=p.descricao,
            fornecedor=p.fornecedor,
            categoria=p.categoria,
            stock=p.stock,
            stock_minimo=p.quantidade_minima,
            preco=p.preco,
        )
        for p in pecas
    ]


@router.post("/", status_code=201)
def criar_peca(
    dados: PecaCreate,
    gestor_stock: GestorStock = Depends(_gestor_stock),
    _=Depends(requer_operacao("criarPeca")),
):
    sucesso = gestor_stock.criarPeca(
        nome=dados.nome,
        descricao=dados.descricao,
        fornecedor=dados.fornecedor,
        categoria=dados.categoria,
        preco=dados.preco,
        stock=dados.stock,
        quantidade_minima=dados.stock_minimo,
    )
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao criar peça.")
    return {"message": "Peça criada com sucesso!"}



@router.put("/{id}")
def editar_pecas(
    id: int,
    dados: PecaAlter,
    gestor_stock: GestorStock = Depends(_gestor_stock),
    _=Depends(requer_operacao("editarPeca")),
):
    sucesso = gestor_stock.atualizarPeca(
        id, dados.nome, dados.descricao,
        dados.fornecedor, dados.categoria, dados.stock,
        dados.stock_minimo, dados.preco,
    )
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao atualizar peça.")
    return {"message": "Peça atualizada com sucesso!"}
