import bcrypt
import re

class CriptografiaHelper:
    REGEX_TELEFONE = r'^\(?\d{2}\)?[\s-]?9\d{4}[-\s]?\d{4}$'

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        return re.match(CriptografiaHelper.REGEX_TELEFONE, telefone) is not None

    @staticmethod
    def normalizar_telefone(telefone: str) -> str:
        return re.sub(r'\D', '', telefone)  # Remove tudo que não for dígito

    @staticmethod
    def hash_telefone(telefone: str) -> str:
        telefone_normalizado = CriptografiaHelper.normalizar_telefone(telefone)
        telefone_bytes = telefone_normalizado.encode('utf-8')
        hashed = bcrypt.hashpw(telefone_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def verificar_telefone(telefone_inserido: str, telefone_hash: str) -> bool:
        telefone_normalizado = CriptografiaHelper.normalizar_telefone(telefone_inserido)
        return bcrypt.checkpw(telefone_normalizado.encode('utf-8'), telefone_hash.encode('utf-8'))
