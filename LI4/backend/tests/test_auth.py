"""Testes unitários do módulo auth.py (JWT)."""
import pytest
import time
from datetime import timedelta
from unittest.mock import patch, MagicMock

from fastapi import HTTPException
from jose import jwt

import auth
from auth import criar_token, _descodificar_token, SECRET_KEY, ALGORITHM


def _token(user_id: int) -> str:
    return criar_token({"sub": str(user_id)})


# ─────────────────────────────────────────────────────────────────────────────
# CRIAR TOKEN
# ─────────────────────────────────────────────────────────────────────────────

class TestCriarToken:
    def test_criar_token_retorna_string_nao_vazia(self):
        token = _token(1)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_contem_sub_com_id_correcto(self):
        token = _token(42)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "42"

    def test_tokens_de_ids_diferentes_sao_distintos(self):
        t1 = _token(1)
        t2 = _token(2)
        assert t1 != t2

    def test_token_tem_campo_exp(self):
        token = _token(1)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload


# ─────────────────────────────────────────────────────────────────────────────
# DESCODIFICAR TOKEN
# ─────────────────────────────────────────────────────────────────────────────

class TestDescodificarToken:
    def test_token_valido_retorna_payload(self):
        token = _token(10)
        payload = _descodificar_token(token)
        assert payload["sub"] == "10"

    def test_token_com_assinatura_invalida_lanca_401(self):
        token_falso = jwt.encode({"sub": "1"}, "chave_errada", algorithm=ALGORITHM)
        with pytest.raises(HTTPException) as exc_info:
            _descodificar_token(token_falso)
        assert exc_info.value.status_code == 401

    def test_token_expirado_lanca_401(self):
        from datetime import datetime, timezone
        payload = {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
        }
        token_expirado = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        with pytest.raises(HTTPException) as exc_info:
            _descodificar_token(token_expirado)
        assert exc_info.value.status_code == 401

    def test_token_completamente_invalido_lanca_401(self):
        with pytest.raises(HTTPException) as exc_info:
            _descodificar_token("nao.e.um.token.valido")
        assert exc_info.value.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# GET UTILIZADOR ATUAL
# ─────────────────────────────────────────────────────────────────────────────

class TestGetUtilizadorAtual:
    def test_retorna_id_utilizador_do_token(self):
        token = _token(7)
        mock_credentials = MagicMock()
        mock_credentials.credentials = token

        resultado = auth.get_utilizador_atual(mock_credentials)

        assert resultado == {"id_utilizador": 7}

    def test_token_invalido_lanca_401(self):
        mock_credentials = MagicMock()
        mock_credentials.credentials = "token.invalido.abc"

        with pytest.raises(HTTPException) as exc_info:
            auth.get_utilizador_atual(mock_credentials)
        assert exc_info.value.status_code == 401
