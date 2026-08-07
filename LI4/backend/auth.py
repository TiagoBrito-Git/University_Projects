import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from Model.SecuritySubsystem.GestorSeguranca import GestorDeSeguranca
from Model.SecuritySubsystem.UtilizadorDAO import UtilizadorDAO
from database import get_db


from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

# Configurações
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # sessão expira em 30 minutos de inatividade

# Esquema de autenticação Bearer
bearer_scheme = HTTPBearer()



# Gera um token JWT com os dados do utilizador
def criar_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
            expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Descodifica e valida o token JWT


def _descodificar_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado",
        )
#
def get_utilizador_atual(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    payload = _descodificar_token(credentials.credentials)

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    return {"id_utilizador": int(user_id)}


def requer_operacao(operacao: str):
    def wrapper(
        user=Depends(get_utilizador_atual),
        db=Depends(get_db),
    ):
        gestor = GestorDeSeguranca(UtilizadorDAO(db))
        if not gestor.verificarPermissoes(user["id_utilizador"], operacao):
            raise HTTPException(status_code=403, detail="Sem permissões")
        return user

    return wrapper