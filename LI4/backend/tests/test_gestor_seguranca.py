"""Testes unitários do GestorDeSeguranca."""
import pytest
import bcrypt
from datetime import date
from unittest.mock import MagicMock, patch

from Model.SecuritySubsystem.GestorSeguranca import GestorDeSeguranca
from Model.SecuritySubsystem.Utilizador import Utilizador


def _gestor(utilizador_dao=None):
    return GestorDeSeguranca(utilizador_dao or MagicMock())


def _utilizador_com_password(password: str, id: int = 1) -> Utilizador:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
    u = MagicMock(spec=Utilizador)
    u.id = id
    u.password_hash = password_hash.decode()
    u.ativo = True
    return u


# ─────────────────────────────────────────────────────────────────────────────
# AUTENTICAR UTILIZADOR
# ─────────────────────────────────────────────────────────────────────────────

class TestAutenticarUtilizador:
    def test_autenticar_com_password_correcta_retorna_utilizador(self, mock_utilizador_dao):
        u = _utilizador_com_password("admin123")
        mock_utilizador_dao.consultar_por_username.return_value = u

        gestor = _gestor(mock_utilizador_dao)
        resultado = gestor.autenticarUtilizador("joao@oficina.pt", "admin123")

        assert resultado is u

    def test_autenticar_com_password_errada_retorna_none(self, mock_utilizador_dao):
        u = _utilizador_com_password("admin123")
        mock_utilizador_dao.consultar_por_username.return_value = u

        gestor = _gestor(mock_utilizador_dao)
        resultado = gestor.autenticarUtilizador("joao@oficina.pt", "errada")

        assert resultado is None

    def test_autenticar_username_inexistente_retorna_none(self, mock_utilizador_dao):
        mock_utilizador_dao.consultar_por_username.return_value = None

        gestor = _gestor(mock_utilizador_dao)
        resultado = gestor.autenticarUtilizador("ninguem@oficina.pt", "qualquer")

        assert resultado is None


# ─────────────────────────────────────────────────────────────────────────────
# CRIAR UTILIZADOR
# ─────────────────────────────────────────────────────────────────────────────

class TestCriarUtilizador:
    @pytest.mark.parametrize("perfil", ["secretaria", "tecnico", "gestor", "administrador"])
    def test_criar_utilizador_com_perfil_valido(self, perfil, mock_utilizador_dao):
        mock_utilizador_dao.inserir.return_value = None

        gestor = _gestor(mock_utilizador_dao)
        resultado = gestor.criarUtilizador("Nome", "user@test.pt", "pass123", perfil)

        assert resultado is True
        mock_utilizador_dao.inserir.assert_called_once()

    def test_criar_utilizador_com_perfil_invalido_lanca_valor_error(self, mock_utilizador_dao):
        gestor = _gestor(mock_utilizador_dao)

        with pytest.raises(ValueError):
            gestor.criarUtilizador("Nome", "user@test.pt", "pass123", "superadmin")

    def test_criar_utilizador_nao_chama_dao_com_perfil_invalido(self, mock_utilizador_dao):
        gestor = _gestor(mock_utilizador_dao)

        try:
            gestor.criarUtilizador("Nome", "user@test.pt", "pass123", "hacker")
        except ValueError:
            pass

        mock_utilizador_dao.inserir.assert_not_called()

    def test_password_guardada_como_hash(self, mock_utilizador_dao):
        mock_utilizador_dao.inserir.return_value = None

        gestor = _gestor(mock_utilizador_dao)
        gestor.criarUtilizador("Nome", "user@test.pt", "minhapass", "tecnico")

        utilizador_inserido = mock_utilizador_dao.inserir.call_args[0][0]
        # O hash não deve ser igual à password em texto claro
        assert utilizador_inserido.password_hash != "minhapass"
        # Mas deve ser verificável com bcrypt
        assert bcrypt.checkpw(b"minhapass", utilizador_inserido.password_hash.encode())


# ─────────────────────────────────────────────────────────────────────────────
# ALTERAR PERFIL
# ─────────────────────────────────────────────────────────────────────────────

class TestAlterarPerfil:
    def test_alterar_para_perfil_valido(self, mock_utilizador_dao):
        mock_utilizador_dao.alterar_perfil.return_value = True

        gestor = _gestor(mock_utilizador_dao)
        resultado = gestor.alterarPerfilUtilizador(1, "gestor")

        assert resultado is True
        mock_utilizador_dao.alterar_perfil.assert_called_once_with(1, "gestor")

    def test_alterar_para_perfil_invalido_lanca_erro(self, mock_utilizador_dao):
        gestor = _gestor(mock_utilizador_dao)

        with pytest.raises(ValueError):
            gestor.alterarPerfilUtilizador(1, "root")


# ─────────────────────────────────────────────────────────────────────────────
# VERIFICAR PERMISSÕES
# ─────────────────────────────────────────────────────────────────────────────

class TestVerificarPermissoes:
    def test_verifica_permissao_delega_ao_dao(self, mock_utilizador_dao):
        mock_utilizador_dao.verificar_permissao.return_value = True

        gestor = _gestor(mock_utilizador_dao)
        resultado = gestor.verificarPermissoes(1, "ler")

        assert resultado is True
        mock_utilizador_dao.verificar_permissao.assert_called_once_with(1, "ler")

    def test_permissao_negada_retorna_false(self, mock_utilizador_dao):
        mock_utilizador_dao.verificar_permissao.return_value = False

        gestor = _gestor(mock_utilizador_dao)
        assert gestor.verificarPermissoes(1, "remover") is False
