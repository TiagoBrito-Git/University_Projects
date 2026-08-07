import re
from typing import Optional


class Cliente:
    def __init__(self, id: int, nome: str, nif: str, contacto: Optional[str], email: Optional[str], morada: Optional[str]):
        self._id = id
        self.set_nome(nome)
        self.set_nif(nif)
        self.set_contacto(contacto)
        self.set_email(email)
        self.set_morada(morada)

    # Getters
    def get_id(self) -> int:
        return self._id

    def get_nome(self) -> str:
        return self._nome

    def get_nif(self) -> str:
        return self._nif

    def get_contacto(self) -> str:
        return self._contacto

    def get_email(self) -> str:
        return self._email

    def get_morada(self) -> str:
        return self._morada

    # Setters
    def set_nome(self, nome: str):
        if not nome:
            raise ValueError("Nome inválido")
        self._nome = nome

    def set_nif(self, nif: str):
        if not self.validar_nif(nif):
            raise ValueError(f"NIF inválido: {nif}")
        self._nif = nif

    def set_contacto(self, contacto: str):
        if contacto is not None and (not contacto.isdigit() or len(contacto) < 9):
            raise ValueError("Contacto inválido")
        self._contacto = contacto

    def set_email(self, email: str):
        if email is not None and not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError(f"Email inválido: {email}")
        self._email = email

    def set_morada(self, morada: str):
        self._morada = morada


    @staticmethod
    def validar_nif(nif: str) -> bool:
        if not re.fullmatch(r"[12356789]\d{8}", nif):
            return False

        total = sum(int(nif[i]) * (9 - i) for i in range(8))
        check = 11 - (total % 11)
        if check >= 10:
            check = 0

        return check == int(nif[8])


    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "nif": self._nif,
            "contacto": self._contacto,
            "email": self._email,
            "morada": self._morada
        }