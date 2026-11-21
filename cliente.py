"""
cliente.py
==========
Clase Cliente: encapsula los datos personales y los valida con rigor.
Cada setter valida el dato antes de guardarlo (ENCAPSULACIÓN).
"""

import re  # Expresiones regulares para validar texto

from entidad_base import EntidadBase
from excepciones import ClienteInvalidoError, ParametroFaltanteError

# Solo letras (con tildes y ñ) y espacios.
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$")
# Estructura básica de un correo: algo@dominio.ext
PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ con datos personales protegidos."""

    def __init__(self, nombre=None, documento=None, email=None, telefono=None):
        # Usamos los setters (self.nombre = ...) para que validen al crear.
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono  # Este dato es opcional
        # El ID se genera al final: si algún dato es inválido no se gasta un número.
        super().__init__("CLI")

    # ---------- Nombre ----------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        valor = str(valor).strip()
        if len(valor) < 3 or not PATRON_NOMBRE.match(valor):
            raise ClienteInvalidoError(
                f"Nombre inválido '{valor}': mínimo 3 letras, sin números ni símbolos."
            )
        self.__nombre = valor.title()  # Guardamos con formato Nombre Apellido

    # ---------- Documento ----------
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")
        valor = str(valor).strip()
        if not valor.isdigit() or not (5 <= len(valor) <= 12):
            raise ClienteInvalidoError(
                f"Documento inválido '{valor}': solo dígitos, entre 5 y 12."
            )
        self.__documento = valor

    # ---------- Email ----------
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        valor = str(valor).strip().lower()
        if not PATRON_EMAIL.match(valor):
            raise ClienteInvalidoError(f"Correo inválido '{valor}'.")
        self.__email = valor

    # ---------- Teléfono (opcional) ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:  # Es opcional: permitimos que no exista
            self.__telefono = None
            return
        valor = str(valor).strip()
        if not valor.isdigit() or not (7 <= len(valor) <= 10):
            raise ClienteInvalidoError(
                f"Teléfono inválido '{valor}': solo dígitos, entre 7 y 10."
            )
        self.__telefono = valor

    # ---------- Método abstracto implementado ----------
    def describir(self) -> str:
        tel = self.telefono if self.telefono else "sin teléfono"
        return f"[{self.id}] {self.nombre} | Doc: {self.documento} | {self.email} | {tel}"
