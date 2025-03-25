from db import get_connection

class FuncoesUteis:

    @staticmethod
    def verificar_existencia(tabela, coluna, valor):
        """Verifica se um registro existe no banco de dados."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM cadastro.{tabela} WHERE {coluna} = %s", (valor,))
        existe = cur.fetchone() is not None
        cur.close()
        conn.close()
        return existe
