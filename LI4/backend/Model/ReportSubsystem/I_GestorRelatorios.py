from abc import ABC, abstractmethod

from Model.ReportSubsystem.Relatorio import Relatorio


class I_GestorRelatorios(ABC):

    @abstractmethod
    def listar_relatorios(self) -> list[Relatorio]:
        ...

    @abstractmethod
    def get_caminho_relatorio(self, id: int) -> str | None:
        ...

    @abstractmethod
    def gerar_economico(self, ordens: int, lucro: float, crescimento: float, mes_referencia: str = None) -> int:
        ...

    @abstractmethod
    def gerar_stock(self, pecas_usadas: dict, mes_referencia: str = None) -> int:
        ...

    @abstractmethod
    def gerar_performance(
        self,
        tempo_medio: float,
        diff_tempo: float,
        pct_nao_avancadas: float,
        diff_nao_avancadas: float,
        num_ordens: int,
        diff_ordens: float,
        mes_referencia: str = None,
    ) -> int:
        ...
