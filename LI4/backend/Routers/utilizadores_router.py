from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from schemas import UtilizadorResponse, CriarUtilizador, EditarUtilizador
from auth import get_utilizador_atual, requer_operacao

from Model.SecuritySubsystem.GestorSeguranca import GestorDeSeguranca, UtilizadorDAO, Utilizador

router = APIRouter(prefix="/utilizadores", tags=["Utilizadores"])


def _gestor_utilizadores(db=Depends(get_db)) -> GestorDeSeguranca:
    return GestorDeSeguranca(UtilizadorDAO(db))

def _validar_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password deve ter pelo menos 8 caracteres")
    if not any(c.isupper() for c in password):
        raise HTTPException(status_code=400, detail="Password deve ter pelo menos 1 letra maiúscula")
    if not any(c.isdigit() for c in password):
        raise HTTPException(status_code=400, detail="Password deve ter pelo menos 1 número")


@router.get("/", response_model=list[UtilizadorResponse], summary="Listar utilizadores")
def listar_utilizadores(
    gest_usr: GestorDeSeguranca = Depends(_gestor_utilizadores),
    _=Depends(requer_operacao("lerUtilizador")),
):
    utilizadores = gest_usr.listarUtilizadores()
    return [
        UtilizadorResponse(
            id=u.id, nome=u.nome, username=u.username,
            perfil=u.perfil, ativo=u.ativo, data_registo=u.data_registo
        )
        for u in utilizadores
    ]


@router.post("/", response_model=UtilizadorResponse, status_code=201, summary="Criar conta de utilizador")
def criar_utilizador(
    body: CriarUtilizador,
    db=Depends(get_db),
    gest_utilizadores: GestorDeSeguranca = Depends(_gestor_utilizadores),
    _=Depends(requer_operacao("criarUtilizador")),
):
    dao = UtilizadorDAO(db)
    if dao.consultar_por_username(body.username):
        raise HTTPException(status_code=409, detail="Username já existe no sistema")

    _validar_password(body.password)

    gestor = GestorDeSeguranca(dao)
    try:
        gestor.criarUtilizador(body.nome, body.username, body.password, body.perfil)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    novo_utilizador = dao.consultar_por_username(body.username)
    return UtilizadorResponse(
        id=novo_utilizador.id, nome=novo_utilizador.nome, username=novo_utilizador.username,
        perfil=novo_utilizador.perfil, ativo=novo_utilizador.ativo, data_registo=novo_utilizador.data_registo
    )


@router.put("/{id}", response_model=UtilizadorResponse, summary="Editar conta de utilizador")
def editar_utilizador(
    id: int,
    body: EditarUtilizador,
    gest_utilizadores: GestorDeSeguranca = Depends(_gestor_utilizadores),
    _=Depends(requer_operacao("editarUtilizador")),
):
    utilizador = gest_utilizadores.consultarUtilizador(id)
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    if body.nome:
        gest_utilizadores.alterarNomeUtilizador(id, body.nome)

    if body.perfil:
        gest_utilizadores.alterarPerfilUtilizador(id, body.perfil)

    if body.password:
        _validar_password(body.password)
        gest_utilizadores.alterarPasswordUtilizador(id, body.password)

    novo_usr: Utilizador = gest_utilizadores.consultarUtilizador(id)
    return UtilizadorResponse(
        id=novo_usr.id, nome=novo_usr.nome, username=novo_usr.username,
        perfil=novo_usr.perfil, ativo=novo_usr.ativo, data_registo=novo_usr.data_registo
    )


@router.put("/{id}/desativar", summary="Desativar conta de utilizador (não apaga histórico)")
def desativar_utilizador(
    id: int,
    gest_utilizadores: GestorDeSeguranca = Depends(_gestor_utilizadores),
    user=Depends(requer_operacao("desativarUtilizador")),
):
    if id == user["id_utilizador"]:
        raise HTTPException(status_code=400, detail="Não pode desativar a própria conta")

    utilizador = gest_utilizadores.consultarUtilizador(id)
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    if not utilizador.ativo:
        raise HTTPException(status_code=400, detail="Utilizador já está desativado")

    gest_utilizadores.desativarUtilizador(id)
    return {"message": f"Utilizador '{utilizador.nome}' desativado com sucesso"}
