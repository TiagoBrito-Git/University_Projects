import bcrypt
from datetime import date
from typing import Optional

from Model.SecuritySubsystem.UtilizadorDAO import UtilizadorDAO
from Model.SecuritySubsystem.Utilizador import Utilizador
from Model.SecuritySubsystem.I_GestorDeSeguranca import I_GestorDeSeguranca

ROLES = ["secretaria", "tecnico", "gestor", "administrador"]

class GestorDeSeguranca(I_GestorDeSeguranca):
    def __init__(self, utilizador_dao: UtilizadorDAO):
        self.utilizador_dao = utilizador_dao

    # 🔐 AUTENTICAÇÃO
    def autenticarUtilizador(self, username: str, password: str) -> Optional[Utilizador]:
        user = self.utilizador_dao.consultar_por_username(username)

        if not user:
            return None

        # comparar password com hash guardado
        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return user
        
        return None


    # ➕ CRIAR UTILIZADOR
    def criarUtilizador(self, nome: str, username: str, password: str, perfil: str) -> bool:
        if perfil not in ROLES:
            raise ValueError("Perfil inválido")

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)

        novo_user = Utilizador(
            id=0,
            nome=nome,
            username=username,
            password_hash=password_hash.decode(),
            password_salt=salt.decode(), 
            perfil=perfil,
            ativo=True,
            data_registo=date.today()
        )

        self.utilizador_dao.inserir(novo_user, salt)
        return True

    # 🔑 VERIFICAR PERMISSÕES
    def verificarPermissoes(self, user_id: int, operacao: str) -> bool:
        return self.utilizador_dao.verificar_permissao(user_id, operacao)


    def consultarUtilizador(self, user_id:int):
        return self.utilizador_dao.consultar_por_id(user_id)


    def alterarNomeUtilizador(self, user_id: int, novo_nome: str) -> bool:
        return self.utilizador_dao.alterar_nome(user_id, novo_nome)

    def alterarPerfilUtilizador(self, user_id: int, novo_perfil: str) -> bool:
        if novo_perfil not in ROLES:
            raise ValueError("Perfil inválido")

        return self.utilizador_dao.alterar_perfil(user_id, novo_perfil)

    def alterarPasswordUtilizador(self, user_id: int, nova_password: str) -> bool:
        salt = bcrypt.gensalt()

        password_hash = bcrypt.hashpw(
            nova_password.encode(),
            salt
        )

        return self.utilizador_dao.alterar_password(
            user_id,
            password_hash.decode(),
            salt.decode()
        )

    def listarUtilizadores(self) -> list[Utilizador]:
        return self.utilizador_dao.listar_utilizadores()

    def desativarUtilizador(self, user_id: int) -> bool:
        return self.utilizador_dao.desativar(user_id)
