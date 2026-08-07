from typing import List, Optional
from datetime import datetime
from .Cliente import Cliente
from .ClienteDAO import ClienteDAO
from .TrotineteDAO import TrotineteDAO
from .Trotinete import Trotinete
from .I_GestorClientes import I_GestorClientes


class GestorClientes(I_GestorClientes):
    def __init__(self, cliente_dao: ClienteDAO, trotinete_dao: TrotineteDAO):
        self._cliente_dao = cliente_dao
        self._trotinete_dao = trotinete_dao

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------

    def criar_cliente(self,nome: str,nif: str,contacto: str,email: str,morada: str,) -> int:
        cliente = Cliente(
            id=None,
            nome=nome,
            nif=nif,
            contacto=contacto,
            email=email,
            morada=morada,
        )
        return self._cliente_dao.criarCliente(cliente)
        


    def consultar_cliente(self, id: str) -> Optional[Cliente]:
        return self._cliente_dao.consultarCliente(id)

    def consultar_cliente_nif(self, nif: str) -> Optional[Cliente]:
        return self._cliente_dao.consultarClienteNIF(nif)



    def editar_cliente(self, id: int, nome: str, nif: str, contacto: str, email: str, morada: str) -> bool:
        if not self.consultar_cliente(id):
            return 0

        return self._cliente_dao.editarCliente(
            id=id,
            nome=nome,
            nif=nif,
            contacto=contacto,
            email=email,
            morada=morada,
        )

    def anonimizar_cliente(self, id: int) -> bool:
        """Anonimiza dados pessoais do cliente e das suas trotinetes (RGPD Art. 17.º)."""
        cliente = self._cliente_dao.consultarCliente(id)
        if cliente is None:
            return False
        self._trotinete_dao.anonimizarTrotinetesPorCliente(id)
        return self._cliente_dao.anonimizarCliente(id)

    def remover_cliente(self, id: int) -> bool:
        cliente = self._cliente_dao.consultarCliente(id)
        if cliente is None:
            return False

        id_cliente = cliente.get_id()
        tem_historico = self._cliente_dao.tem_historico(id_cliente)
        conn = self._cliente_dao.db
        try:
            conn.rollback()
        except Exception:
            pass
        try:
            with conn.cursor() as cursor:
                if tem_historico:
                    self._trotinete_dao._exec_anonimizar_por_cliente(cursor, id_cliente)
                    resultado = self._cliente_dao._exec_anonimizar(cursor, id_cliente)
                else:
                    self._trotinete_dao._exec_remover_por_cliente(cursor, id_cliente)
                    resultado = self._cliente_dao._exec_remover(cursor, id_cliente)
            conn.commit()
            return resultado
        except Exception:
            try:
                conn.rollback()
            except Exception:
                pass
            raise

    def listar_clientes(self) -> List[Cliente]:
        return self._cliente_dao.listarClientes()

    # ------------------------------------------------------------------
    # Trotinetes
    # ------------------------------------------------------------------

    def registar_trotinete(self,marca: str,modelo: str,numero_serie: str,id_cliente: int,) -> bool:
        clientes = self._cliente_dao.listarClientes()
        ids_validos = {c.get_id() for c in clientes}
        if id_cliente not in ids_validos:
            return False

        trotinete = Trotinete(
            id=-1,
            marca=marca,
            modelo=modelo,
            numero_serie=numero_serie,
            data_registo=datetime.now(),
            id_cliente=id_cliente,
        )
        return self._trotinete_dao.criarTrotinete(trotinete)

    def consultar_trotinete(self,id:int) -> Trotinete:
        return self._trotinete_dao.consultarTrotinete(id)
    
    def consultar_trotinete_numero_serie(self, numero_serie: str) -> Trotinete:
        return self._trotinete_dao.consultarTrotinete_numero_serie(numero_serie)

    def editar_trotinete(self, id: int, marca: str, modelo: str, numero_serie: str, id_cliente: int) -> bool:
        if not self._trotinete_dao.consultarTrotinete(id):
            return False
        return self._trotinete_dao.editarTrotineteById(id, marca, modelo, numero_serie, id_cliente)

    def remover_trotinete(self, id: int) -> bool:
        if not self._trotinete_dao.consultarTrotinete(id):
            return False
        if self._trotinete_dao.temOrdensAssociadas(id):
            return self._trotinete_dao.anonimizarTrotinete(id)
        return self._trotinete_dao.removerTrotineteById(id)
    
    def listar_trotinetes(self) -> List[Trotinete]:
        return self._trotinete_dao.listarTrotinetes()

    def listar_trotinetes_cliente(self, id_cliente: int) -> List[Trotinete]:
        return self._trotinete_dao.listarTrotinetesPorCliente(id_cliente)