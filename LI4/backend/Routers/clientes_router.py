from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from database import get_db
from auth import requer_operacao
from Model.ClientSubsystem.GestorClientes import GestorClientes, ClienteDAO, TrotineteDAO


router = APIRouter(prefix="/clientes", tags=["CLIENTES"])


class ClienteResponse(BaseModel):
    id: int
    nome: str
    nif: str
    contacto: Optional[str] = None
    email: Optional[str] = None
    morada: Optional[str] = None

    class Config:
        from_attributes = True


class ClienteCreate(BaseModel):
    nome: str
    nif: str
    contacto: str
    email: str
    morada: str


class ClienteAlter(BaseModel):
    nome: str
    nif: str
    contacto: str
    email: str
    morada: str


def _gestor_clientes(db=Depends(get_db)) -> GestorClientes:
    return GestorClientes(ClienteDAO(db), TrotineteDAO(db))


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(
    gestor_cli: GestorClientes = Depends(_gestor_clientes),
    _=Depends(requer_operacao("lerCliente")),
):
    clientes = gestor_cli.listar_clientes()
    return [
        ClienteResponse(
            id=c.get_id(),
            nome=c.get_nome(),
            nif=c.get_nif(),
            contacto=c.get_contacto(),
            email=c.get_email(),
            morada=c.get_morada(),
        )
        for c in clientes
    ]


@router.post("/", status_code=201)
def criar_cliente(
    dados: ClienteCreate,
    gestor_cli: GestorClientes = Depends(_gestor_clientes),
    _=Depends(requer_operacao("criarCliente")),
):
    try:
        sucesso = gestor_cli.criar_cliente(dados.nome, dados.nif, dados.contacto, dados.email, dados.morada)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not sucesso:
        raise HTTPException(status_code=400, detail="NIF já existe na base de dados.")
    return {"message": "Cliente criado com sucesso!"}


@router.put("/{id}")
def editar_cliente(
    id: int,
    dados: ClienteAlter,
    gestor_cli: GestorClientes = Depends(_gestor_clientes),
    _=Depends(requer_operacao("editarCliente")),
):
    sucesso = gestor_cli.editar_cliente(id, dados.nome, dados.nif, dados.contacto, dados.email, dados.morada)
    if sucesso is False:
        raise HTTPException(status_code=400, detail="Erro ao editar cliente.")
    if sucesso == 0:
        raise HTTPException(status_code=404, detail="Erro: Cliente não encontrado.")
    return {"message": "Cliente editado com sucesso!"}


@router.delete("/{id}", status_code=200)
def remover_cliente(
    id: int,
    gestor_cli: GestorClientes = Depends(_gestor_clientes),
    _=Depends(requer_operacao("removerCliente")),
):
    try:
        sucesso = gestor_cli.remover_cliente(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover cliente: {e}")
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Cliente com ID {id} não encontrado.")
    return {"message": "Cliente removido com sucesso!"}


