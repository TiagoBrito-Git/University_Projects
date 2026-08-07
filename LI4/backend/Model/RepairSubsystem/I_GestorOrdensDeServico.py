from abc import ABC, abstractmethod

from Model.RepairSubsystem.OrdemDeServico import OrdemDeServico


class I_GestorOrdensDeServico(ABC):

    @abstractmethod
    def criar_ordem_de_servico(self, data_conclusao, descricao, id_trotinete, id_tecnico, id_cliente) -> int:
        ...

    @abstractmethod
    def avancar_estado_ordem_de_servico(self, id: int) -> bool:
        ...

    @abstractmethod
    def alterar_estado_ordem_de_servico(self, id, estado) -> bool:
        ...

    @abstractmethod
    def atualizar_ordem_de_servico(self, id, data_conclusao, descricao) -> bool:
        ...

    @abstractmethod
    def consultar_os(self, id) -> OrdemDeServico:
        ...

    @abstractmethod
    def listar_ordens_de_servico(self) -> list[OrdemDeServico]:
        ...

    @abstractmethod
    def remover_ordem_de_servico(self, id) -> bool:
        ...

    @abstractmethod
    def criar_intervencao(self, id_os, id_tecnico, descricao, tempo: float, custo_pecas, pecas):
        ...

    @abstractmethod
    def criar_diagnostico(self, id_os, id_tecnico, descricao, orcamento_pecas, pecas, tempo_estimado: float):
        ...

    @abstractmethod
    def alterar_diagnostico(self, id, id_os, id_tecnico, descricao, orcamento_pecas, pecas, tempo_estimado: float):
        ...

    @abstractmethod
    def obter_resumo_pecas_intervencoes(self, id_os: int):
        ...

    @abstractmethod
    def preparar_dados_finalizacao(self, id_os: int, estado_final: str):
        ...

    @abstractmethod
    def obter_detalhes_completos_os(self, id_os: int):
        ...

    @abstractmethod
    def obter_contagem_ordens_mes_atual(self, mes, ano) -> int:
        ...

    @abstractmethod
    def obter_pecas_usadas(self, mes: int, ano: int) -> dict:
        ...

    @abstractmethod
    def obter_dados_performance(self, mes: int, ano: int) -> dict:
        ...

    @abstractmethod
    def alterar_estado_em_transacao(self, id: int, estado: str) -> bool:
        ...
