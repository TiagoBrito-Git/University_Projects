from abc import ABC, abstractmethod
from typing import List, Optional

from .Cliente import Cliente
from .Trotinete import Trotinete


class I_GestorClientes(ABC):

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------

    @abstractmethod
    def criar_cliente(self, nome: str, nif: str, contacto: str, email: str, morada: str) -> int:
        ...

    @abstractmethod
    def consultar_cliente(self, id: str) -> Optional[Cliente]:
        ...

    @abstractmethod
    def consultar_cliente_nif(self, nif: str) -> Optional[Cliente]:
        ...

    @abstractmethod
    def editar_cliente(self, id: int, nome: str, nif: str, contacto: str, email: str, morada: str) -> bool:
        ...

    @abstractmethod
    def anonimizar_cliente(self, id: int) -> bool:
        ...

    @abstractmethod
    def remover_cliente(self, id: int) -> bool:
        ...

    @abstractmethod
    def listar_clientes(self) -> List[Cliente]:
        ...

    # ------------------------------------------------------------------
    # Trotinetes
    # ------------------------------------------------------------------

    @abstractmethod
    def registar_trotinete(self, marca: str, modelo: str, numero_serie: str, id_cliente: int) -> bool:
        ...

    @abstractmethod
    def consultar_trotinete(self, id: int) -> Trotinete:
        ...

    @abstractmethod
    def consultar_trotinete_numero_serie(self, numero_serie: str) -> Trotinete:
        ...

    @abstractmethod
    def editar_trotinete(self, id: int, marca: str, modelo: str, numero_serie: str, id_cliente: int):
        ...

    @abstractmethod
    def remover_trotinete(self, id: int) -> bool:
        ...

    @abstractmethod
    def listar_trotinetes(self) -> List[Trotinete]:
        ...

    @abstractmethod
    def listar_trotinetes_cliente(self, id_cliente: int) -> List[Trotinete]:
        ...
