"""Fixtures partilhadas entre os módulos de teste."""
import os
os.environ.setdefault("DB_PORT", "3307")  # testes usam sempre o Docker MySQL
os.environ.setdefault("SECRET_KEY", "test_secret_key")

import pytest
from datetime import date, datetime
from unittest.mock import MagicMock

from Model.RepairSubsystem.OrdemDeServico import OrdemDeServico
from Model.RepairSubsystem.Diagnostico import Diagnostico
from Model.RepairSubsystem.Intervencao import Intervencao


@pytest.fixture
def ordem_aguarda_diagnostico():
    return OrdemDeServico(
        id=1,
        data_abertura=datetime(2024, 1, 10),
        data_conclusao=None,
        estado="Aguarda Diagnóstico",
        descricao="Trotinete não liga",
        id_trotinete=2,
        id_tecnico=3,
        id_cliente=1,
    )


@pytest.fixture
def ordem_aguarda_resposta():
    return OrdemDeServico(
        id=2,
        data_abertura=datetime(2024, 1, 10),
        data_conclusao=None,
        estado="Aguarda Resposta",
        descricao="Bateria fraca",
        id_trotinete=2,
        id_tecnico=3,
        id_cliente=1,
    )


@pytest.fixture
def ordem_em_reparacao():
    return OrdemDeServico(
        id=3,
        data_abertura=datetime(2024, 1, 10),
        data_conclusao=None,
        estado="Em Reparação",
        descricao="Travão avariado",
        id_trotinete=2,
        id_tecnico=3,
        id_cliente=1,
    )


@pytest.fixture
def diagnostico_exemplo():
    return Diagnostico(
        id=10,
        descricao="Bateria degradada",
        orcamento_estimado=220.0,
        horas_mao_de_obra=5,
        data=date(2024, 1, 11),
        id_os=1,
        id_tecnico=3,
    )


@pytest.fixture
def intervencao_exemplo():
    return Intervencao(
        id=20,
        descricao="Substituição da bateria",
        horas_trabalhadas=3,
        data=datetime(2024, 1, 12),
        id_os=1,
        id_tecnico=3,
        custo_total=110.0,
        pecas_usadas={1: {"quantidade": 1, "preco_unitario": 50.0}},
    )


@pytest.fixture
def mock_os_dao():
    return MagicMock()


@pytest.fixture
def mock_intervencao_dao():
    return MagicMock()


@pytest.fixture
def mock_diagnostico_dao():
    return MagicMock()


@pytest.fixture
def mock_cliente_dao():
    return MagicMock()


@pytest.fixture
def mock_trotinete_dao():
    return MagicMock()


@pytest.fixture
def mock_peca_dao():
    return MagicMock()


@pytest.fixture
def mock_utilizador_dao():
    return MagicMock()
