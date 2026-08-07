from abc import ABC, abstractmethod
import io

from Model.PaymentsSubsystem.FaturaDAO import Fatura


class I_GestorPagamentos(ABC):

    @abstractmethod
    def listar_faturas(self) -> list[Fatura]:
        ...

    @abstractmethod
    def obter_pdf_fatura(self, id_fatura: int) -> io.BytesIO | None:
        ...

    @abstractmethod
    def consultar_fatura(self, id_fatura: int) -> Fatura | None:
        ...

    @abstractmethod
    def criar_fatura(self, id_os: int, pecas: dict, total_mao_obra: float, tipo_pagamento: str) -> int:
        ...

    @abstractmethod
    def obter_lucro_mes(self, mes: int, ano: int) -> float:
        ...

    @abstractmethod
    def obter_taxa_crescimento_mensal(self, mes: int, ano: int) -> float:
        ...

    @abstractmethod
    def criar_fatura_em_transacao(self, id_os: int, pecas: dict, total_mao_obra: float, tipo_pagamento: str) -> int:
        ...
