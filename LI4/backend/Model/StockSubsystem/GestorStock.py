from Model.StockSubsystem.I_GestorStock import I_GestorStock
from Model.StockSubsystem.PecaDAO import PecaDAO
from Model.StockSubsystem.Peca import Peca

class GestorStock(I_GestorStock):
    
    def __init__(self, pecaDAO:PecaDAO):
        self.pecas = pecaDAO

    def consultarStock(self, peca_id):
        return self.pecas.consultar_por_id(peca_id)

    def atualizarStock(self, peca_id, quantidade):
        return self.pecas.atualizar_stock(peca_id,quantidade)


    def listarPecas(self) -> list[Peca]:
        return self.pecas.listar_pecas()


    def criarPeca(self, nome, descricao, fornecedor, categoria, preco, stock, quantidade_minima):
        p = Peca(-1, nome, descricao, fornecedor, categoria, preco, stock, quantidade_minima)
        return self.pecas.inserir(p)

    def atualizarPeca(self, peca_id, nome, descricao, fornecedor, categoria, stock, stock_minimo, preco):
        p = Peca(peca_id, nome, descricao, fornecedor, categoria, preco, stock, stock_minimo)
        return self.pecas.atualizar(p)

    def listarAlertasStock(self) -> list[Peca]:
        return self.pecas.consultar_abaixo_minimo()