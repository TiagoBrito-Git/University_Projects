"""Testes unitários dos modelos de domínio (sem dependências externas)."""
import pytest
from datetime import date, datetime

from Model.ClientSubsystem.Cliente import Cliente
from Model.StockSubsystem.Peca import Peca
from Model.PaymentsSubsystem.Fatura import Fatura
from Model.RepairSubsystem.Intervencao import Intervencao


# ─────────────────────────────────────────────────────────────────────────────
# CLIENTE
# ─────────────────────────────────────────────────────────────────────────────

class TestCliente:
    NIF_VALIDO = "123456789"

    def _cliente(self, **overrides):
        defaults = dict(
            id=1,
            nome="João Silva",
            nif=self.NIF_VALIDO,
            contacto="912345678",
            email="joao@example.com",
            morada="Rua das Flores, 1",
        )
        defaults.update(overrides)
        return Cliente(**defaults)

    # NIF
    def test_nif_valido_aceite(self):
        c = self._cliente()
        assert c.get_nif() == self.NIF_VALIDO

    def test_nif_com_digito_inicial_invalido_rejeitado(self):
        with pytest.raises(ValueError):
            self._cliente(nif="423456789")  # primeiro dígito 4 é inválido

    def test_nif_com_menos_de_9_digitos_rejeitado(self):
        with pytest.raises(ValueError):
            self._cliente(nif="12345678")

    def test_nif_com_checksum_errado_rejeitado(self):
        # NIF com formato correto mas checksum errado
        with pytest.raises(ValueError):
            self._cliente(nif="123456780")

    def test_nif_com_letras_rejeitado(self):
        with pytest.raises(ValueError):
            self._cliente(nif="12345678A")

    # Email
    def test_email_valido_aceite(self):
        c = self._cliente(email="user@domain.pt")
        assert c.get_email() == "user@domain.pt"

    def test_email_sem_arroba_rejeitado(self):
        with pytest.raises(ValueError):
            self._cliente(email="invalido.com")

    def test_email_sem_dominio_rejeitado(self):
        with pytest.raises(ValueError):
            self._cliente(email="user@")

    # Contacto
    def test_contacto_valido_aceite(self):
        c = self._cliente(contacto="961234567")
        assert c.get_contacto() == "961234567"

    def test_contacto_com_menos_de_9_digitos_rejeitado(self):
        with pytest.raises(ValueError):
            self._cliente(contacto="96123")

    def test_contacto_com_letras_rejeitado(self):
        with pytest.raises(ValueError):
            self._cliente(contacto="96123abc9")

    # Nome / Morada
    def test_nome_vazio_rejeitado(self):
        with pytest.raises(ValueError):
            self._cliente(nome="")


    # to_dict
    def test_to_dict_contem_campos_esperados(self):
        c = self._cliente()
        d = c.to_dict()
        assert d["nif"] == self.NIF_VALIDO
        assert d["email"] == "joao@example.com"
        assert d["nome"] == "João Silva"

    # validar_nif estático
    def test_validar_nif_retorna_true_para_nif_valido(self):
        assert Cliente.validar_nif(self.NIF_VALIDO) is True

    def test_validar_nif_retorna_false_para_nif_invalido(self):
        assert Cliente.validar_nif("000000000") is False


# ─────────────────────────────────────────────────────────────────────────────
# PECA
# ─────────────────────────────────────────────────────────────────────────────

class TestPeca:
    def _peca(self, **overrides):
        defaults = dict(
            id=1, nome="Bateria", descricao="Lítio 36V",
            fornecedor="Xiaomi", categoria="Baterias",
            preco=180.0, stock=8, quantidade_minima=3,
        )
        defaults.update(overrides)
        return Peca(**defaults)

    def test_peca_criada_com_sucesso(self):
        p = self._peca()
        assert p.nome == "Bateria"
        assert p.preco == 180.0

    def test_preco_negativo_via_setter_lanca_erro(self):
        p = self._peca()
        with pytest.raises(ValueError):
            p.preco = -10.0

    def test_stock_negativo_via_setter_lanca_erro(self):
        p = self._peca()
        with pytest.raises(ValueError):
            p.stock = -1

    def test_quantidade_minima_negativa_via_setter_lanca_erro(self):
        p = self._peca()
        with pytest.raises(ValueError):
            p.quantidade_minima = -1

    def test_nome_vazio_via_setter_lanca_erro(self):
        p = self._peca()
        with pytest.raises(ValueError):
            p.nome = ""

    def test_to_dict_contem_todos_os_campos(self):
        p = self._peca()
        d = p.to_dict()
        assert d["nome"] == "Bateria"
        assert d["preco"] == 180.0
        assert d["stock"] == 8


# ─────────────────────────────────────────────────────────────────────────────
# FATURA
# ─────────────────────────────────────────────────────────────────────────────

class TestFatura:
    def _fatura(self, **overrides):
        defaults = dict(
            id=1,
            numero="FT-2024-1",
            data=date(2024, 3, 15),
            sub_total_pecas=100.0,
            sub_total_mao_obra=60.0,
            total=160.0,
            estado="pendente",
            tipo_pagamento="dinheiro",
            id_os=1,
        )
        defaults.update(overrides)
        return Fatura(**defaults)

    def test_fatura_criada_com_sucesso(self):
        f = self._fatura()
        assert f.numero == "FT-2024-1"
        assert f.estado == "pendente"

    def test_estado_invalido_lanca_erro(self):
        with pytest.raises(ValueError):
            self._fatura(estado="desconhecido")

    def test_estado_normalizado_para_minusculas(self):
        f = self._fatura(estado="Pendente")
        assert f.estado == "pendente"

    def test_tipo_pagamento_invalido_lanca_erro(self):
        with pytest.raises(ValueError):
            self._fatura(tipo_pagamento="bitcoin")

    def test_numero_vazio_lanca_erro(self):
        with pytest.raises(ValueError):
            self._fatura(numero="")

    def test_subtotal_negativo_lanca_erro(self):
        with pytest.raises(ValueError):
            self._fatura(sub_total_pecas=-1.0)

    def test_data_invalida_lanca_erro(self):
        with pytest.raises(ValueError):
            self._fatura(data="2024-01-01")  # string em vez de date


# ─────────────────────────────────────────────────────────────────────────────
# INTERVENCAO
# ─────────────────────────────────────────────────────────────────────────────

class TestIntervencao:
    def _intervencao(self, **overrides):
        defaults = dict(
            id=1,
            descricao="Troca de bateria",
            horas_trabalhadas=2.0,
            data=datetime(2024, 3, 15),
            id_os=1,
            id_tecnico=2,
            custo_total=80.0,
            pecas_usadas={1: {"quantidade": 1, "preco_unitario": 40.0}},
        )
        defaults.update(overrides)
        return Intervencao(**defaults)

    def test_intervencao_criada_com_sucesso(self):
        i = self._intervencao()
        assert i.descricao == "Troca de bateria"
        assert i.horas_trabalhadas == 2.0

    def test_horas_negativas_via_setter_lanca_erro(self):
        i = self._intervencao()
        with pytest.raises(ValueError):
            i.horas_trabalhadas = -1.0

    def test_descricao_vazia_via_setter_lanca_erro(self):
        i = self._intervencao()
        with pytest.raises(ValueError):
            i.descricao = ""

    def test_descricao_so_espacos_via_setter_lanca_erro(self):
        i = self._intervencao()
        with pytest.raises(ValueError):
            i.descricao = "   "

    def test_pecas_nao_dict_via_setter_lanca_erro(self):
        i = self._intervencao()
        with pytest.raises(ValueError):
            i.pecas_usadas = [1, 2, 3]

    def test_custo_negativo_via_setter_lanca_erro(self):
        i = self._intervencao()
        with pytest.raises(ValueError):
            i.custo_total = -5.0

    def test_to_dict_contem_pecas_como_lista(self):
        i = self._intervencao()
        d = i.to_dict()
        assert isinstance(d["pecas_usadas"], list)
        assert d["pecas_usadas"][0]["id_peca"] == 1
