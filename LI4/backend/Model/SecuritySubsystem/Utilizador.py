from datetime import date

class Utilizador:
    def __init__(
        self,
        id: int,
        nome: str,
        username: str,
        password_hash: str = "",
        password_salt: str = "",
        perfil: str = "", 
        data_registo: date = "",
        ativo: bool = False
    ):
        self._id = id
        self._nome = nome
        self._username = username
        self._password_hash = password_hash
        self._password_salt = password_salt
        self._perfil = perfil
        self._data_registo = data_registo
        self._ativo = ativo

    # ID (Geralmente apenas Getter, pois o ID não deve mudar)
    @property
    def id(self):
        return self._id

    # Nome
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, valor):
        self._nome = valor

    # Username
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, valor):
        self._username = valor

    # perfil (Antigo Perfil)
    @property
    def perfil(self):
        return self._perfil
    
    @perfil.setter
    def perfil(self, valor):
        self._perfil = valor

    # Ativo
    @property
    def ativo(self):
        return self._ativo
    
    @ativo.setter
    def ativo(self, valor):
        self._ativo = bool(valor)

    @property
    def data_registo(self):
        return self._data_registo

    @property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, valor):
        self._password_hash = valor

