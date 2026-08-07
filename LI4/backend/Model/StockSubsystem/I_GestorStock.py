from abc import ABC, abstractmethod

from Model.StockSubsystem.Peca import Peca


class I_GestorStock(ABC):

    @abstractmethod
    def consultarStock(self, peca_id):
        ...

    @abstractmethod
    def atualizarStock(self, peca_id, quantidade):
        ...

    @abstractmethod
    def listarPecas(self) -> list[Peca]:
        ...

    @abstractmethod
    def criarPeca(self, nome, descricao, fornecedor, categoria, preco, stock, quantidade_minima):
        ...

    @abstractmethod
    def atualizarPeca(self, peca_id, nome, descricao, fornecedor, categoria, stock, stock_minimo, preco):
        ...

    @abstractmethod
    def listarAlertasStock(self) -> list[Peca]:
        ...
