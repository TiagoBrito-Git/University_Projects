from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nome: str
    perfil: str

class Permissao(BaseModel):
    permissao: str
    ativo: bool

class PermissoesUpdate(BaseModel):
    permissoes: list[Permissao]

class CriarUtilizador(BaseModel):
    nome: str
    username: str
    password: str
    perfil: Literal["secretaria", "gestor", "tecnico", "administrador"]

class EditarUtilizador(BaseModel):
    nome: Optional[str] = None
    password: Optional[str] = None
    perfil: Optional[Literal["secretaria", "gestor", "tecnico", "administrador"]] = None

class UtilizadorResponse(BaseModel):
    id: int
    nome: str
    username: str
    perfil: str
    ativo: bool
    data_registo: date

