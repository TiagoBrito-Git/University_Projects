from abc import ABC, abstractmethod
from typing import Optional, List

from Model.SecuritySubsystem.Utilizador import Utilizador


class I_GestorDeSeguranca(ABC):

    @abstractmethod
    def autenticarUtilizador(self, username: str, password: str) -> Optional[Utilizador]:
        ...

    @abstractmethod
    def criarUtilizador(self, nome: str, username: str, password: str, perfil: str) -> bool:
        ...

    @abstractmethod
    def verificarPermissoes(self, user_id: int, operacao: str) -> bool:
        ...

    @abstractmethod
    def consultarUtilizador(self, user_id: int) -> Optional[Utilizador]:
        ...

    @abstractmethod
    def alterarNomeUtilizador(self, user_id: int, novo_nome: str) -> bool:
        ...

    @abstractmethod
    def alterarPerfilUtilizador(self, user_id: int, novo_perfil: str) -> bool:
        ...

    @abstractmethod
    def alterarPasswordUtilizador(self, user_id: int, nova_password: str) -> bool:
        ...

    @abstractmethod
    def listarUtilizadores(self) -> List[Utilizador]:
        ...

    @abstractmethod
    def desativarUtilizador(self, user_id: int) -> bool:
        ...
