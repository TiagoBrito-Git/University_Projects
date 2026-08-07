from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta

from database import get_db
from schemas import LoginRequest, LoginResponse
from auth import criar_token, ACCESS_TOKEN_EXPIRE_MINUTES

from Model.SecuritySubsystem.GestorSeguranca import GestorDeSeguranca
from Model.SecuritySubsystem.UtilizadorDAO import UtilizadorDAO

router = APIRouter(prefix="/auth", tags=["Autenticação"])

def _gestor(db) -> GestorDeSeguranca:
    return GestorDeSeguranca(UtilizadorDAO(db))


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db=Depends(get_db)):
    gestor = _gestor(db)

    utilizador = gestor.autenticarUtilizador(body.username, body.password)
    if not utilizador:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not utilizador.ativo:
        raise HTTPException(status_code=403, detail="Conta desativada")

    token = criar_token(
        {"sub": str(utilizador.id)},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return LoginResponse(
        access_token=token,
        nome=utilizador.nome,
        perfil=utilizador.perfil,
    )