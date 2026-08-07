import io
from datetime import datetime
from Model.PaymentsSubsystem.FaturaDAO import FaturaDAO, Fatura
from Model.PaymentsSubsystem.GeradorFatura import gerar_pdf_fatura
from Model.PaymentsSubsystem.I_GestorPagamentos import I_GestorPagamentos


class GestorPagamentos(I_GestorPagamentos):
    def __init__(self, db_connection):
        self.dao = FaturaDAO(db_connection)

    def listar_faturas(self) -> list[Fatura]:
        return self.dao.listar()

    def consultar_fatura(self, id_fatura: int) -> Fatura | None:
        return self.dao.consultar_por_id(id_fatura)

    def obter_pdf_fatura(self, id_fatura: int) -> io.BytesIO | None:
        fatura = self.consultar_fatura(id_fatura)
        if not fatura:
            return None

        buffer = io.BytesIO()
        gerar_pdf_fatura(fatura, buffer)
        buffer.seek(0)
        return buffer

    def _proximo_numero(self):
        with self.dao.db.cursor() as cursor:
            cursor.execute(
                "SELECT COALESCE(MAX(CAST(SUBSTRING_INDEX(numero, '-', -1) AS UNSIGNED)), 0) FROM fatura WHERE numero LIKE %s",
                (f"FT-{datetime.now().year}-%",)
            )
            return f"FT-{datetime.now().year}-{cursor.fetchone()[0] + 1}"

    def _build_fatura(self, id_os, pecas, total_mao_obra, tipo_pagamento):
        subtotal_pecas = sum(
            d["quantidade"] * d["preco_unitario"]
            for d in pecas.values()
        )
        total = subtotal_pecas + total_mao_obra
        return Fatura(
            id=-1, numero=self._proximo_numero(), data=datetime.now().date(),
            sub_total_pecas=subtotal_pecas, sub_total_mao_obra=total_mao_obra,
            total=total, estado="pendente", tipo_pagamento=tipo_pagamento,
            id_os=id_os, pecas=pecas,
        )

    def criar_fatura(self, id_os, pecas, total_mao_obra, tipo_pagamento) -> int:
        return self.dao.inserir(self._build_fatura(id_os, pecas, total_mao_obra, tipo_pagamento))

    def criar_fatura_em_transacao(self, id_os, pecas, total_mao_obra, tipo_pagamento) -> int:
        return self.dao.inserir_em_transacao(self._build_fatura(id_os, pecas, total_mao_obra, tipo_pagamento))

    def obter_lucro_mes(self, mes: int, ano: int) -> float:
            return self.dao.obter_lucro_mes(mes, ano)
    
    def obter_taxa_crescimento_mensal(self, mes: int, ano: int) -> float:
        """
        Calcula a taxa de crescimento percentual face ao mês anterior.
        Exemplo: 0.50 representa um crescimento de 50%.
        """
        if mes == 1:
            mes_ant, ano_ant = 12, ano - 1
        else:
            mes_ant, ano_ant = mes - 1, ano

        lucro_atual = self.dao.obter_lucro_mes(mes, ano)
        lucro_anterior = self.dao.obter_lucro_mes(mes_ant, ano_ant)

        if lucro_anterior == 0:
            return 100.0 if lucro_atual > 0 else 0.0

        taxa = ((lucro_atual - lucro_anterior) / lucro_anterior) * 100
        return round(taxa, 2)