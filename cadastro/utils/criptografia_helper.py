import bcrypt
import re

class CriptografiaHelper:
    # Regex para telefone com DDD e obrigatoriamente começando com 9
    REGEX_TELEFONE = r'^\(?\d{2}\)?[\s-]?9\d{4}[-\s]?\d{4}$'

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        return re.match(CriptografiaHelper.REGEX_TELEFONE, telefone) is not None

    @staticmethod
    def normalizar_telefone(telefone: str) -> str:
        """Remove qualquer caractere que não seja número."""
        return re.sub(r'\D', '', telefone)

    @staticmethod
    def hash_telefone(telefone: str) -> str:
        """Normaliza e criptografa o telefone com bcrypt."""
        telefone_normalizado = CriptografiaHelper.normalizar_telefone(telefone)
        telefone_bytes = telefone_normalizado.encode('utf-8')
        hashed = bcrypt.hashpw(telefone_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def verificar_telefone(telefone_inserido: str, telefone_hash: str) -> bool:
        """Compara o telefone inserido com o hash armazenado."""
        telefone_normalizado = CriptografiaHelper.normalizar_telefone(telefone_inserido)

        try:
            return bcrypt.checkpw(telefone_normalizado.encode('utf-8'), telefone_hash.encode('utf-8'))
        except ValueError:
            # Hash inválido (ex: valor vazio ou não gerado por bcrypt)
            return False
