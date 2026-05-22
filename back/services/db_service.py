import os
import sqlite3
from datetime import datetime

# Determina o caminho para o arquivo do banco de dados na pasta do backend
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(base_dir, "pibot.db")

class DBService:
    @staticmethod
    def get_connection():
        """Retorna uma conexão ativa com o banco SQLite."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        return conn

    @staticmethod
    def init_db():
        """Inicializa as tabelas do banco de dados caso não existam."""
        conn = DBService.get_connection()
        cursor = conn.cursor()
        
        # Tabela para registrar o histórico de interações comuns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                mensagem TEXT NOT NULL,
                resposta TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        """)
        
        # Tabela para registrar incidentes de segurança (ataques/lockdown)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidentes_seguranca (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                termo_bloqueado TEXT NOT NULL,
                ip_address TEXT,
                acao TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"[DB] Banco de dados inicializado com sucesso em: {DB_PATH}")

    @staticmethod
    def registrar_conversa(mensagem, resposta, tipo):
        """Grava uma nova conversa no histórico."""
        try:
            conn = DBService.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversas (mensagem, resposta, tipo) VALUES (?, ?, ?)",
                (mensagem, resposta, tipo)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[DB Error] Erro ao registrar conversa: {e}")

    @staticmethod
    def registrar_incidente(termo_bloqueado, ip_address, acao):
        """Grava uma tentativa de invasão ou mudança de estado de segurança."""
        try:
            conn = DBService.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO incidentes_seguranca (termo_bloqueado, ip_address, acao) VALUES (?, ?, ?)",
                (termo_bloqueado, ip_address, acao)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[DB Error] Erro ao registrar incidente: {e}")

    @staticmethod
    def obter_estatisticas():
        """Retorna contadores de uso para o Dashboard."""
        stats = {
            "total": 0,
            "ia": 0,
            "local": 0,
            "fallback": 0,
            "attacks": 0
        }
        try:
            conn = DBService.get_connection()
            cursor = conn.cursor()
            
            # Total de conversas normais
            cursor.execute("SELECT COUNT(*) FROM conversas")
            stats["total"] = cursor.fetchone()[0]
            
            # Detalhamento por tipo de resposta
            cursor.execute("SELECT tipo, COUNT(*) FROM conversas GROUP BY tipo")
            for row in cursor.fetchall():
                tipo = row["tipo"]
                count = row[1]
                if tipo == "ia":
                    stats["ia"] = count
                elif tipo == "local":
                    stats["local"] = count
                elif tipo == "offline_fallback":
                    stats["fallback"] = count
            
            # Total de ataques registrados
            cursor.execute("SELECT COUNT(*) FROM incidentes_seguranca WHERE acao = 'lockdown_active'")
            stats["attacks"] = cursor.fetchone()[0]
            
            conn.close()
        except Exception as e:
            print(f"[DB Error] Erro ao buscar estatísticas: {e}")
        return stats

    @staticmethod
    def obter_logs(limite=50):
        """Retorna as conversas mais recentes em formato serializável."""
        logs = []
        try:
            conn = DBService.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT timestamp, mensagem, resposta, tipo FROM conversas ORDER BY id DESC LIMIT ?",
                (limite,)
            )
            for row in cursor.fetchall():
                logs.append({
                    "timestamp": row["timestamp"],
                    "mensagem": row["mensagem"],
                    "resposta": row["resposta"],
                    "tipo": row["tipo"]
                })
            conn.close()
        except Exception as e:
            print(f"[DB Error] Erro ao buscar logs de conversas: {e}")
        return logs

    @staticmethod
    def obter_incidentes(limite=50):
        """Retorna as tentativas de invasão registradas."""
        incidentes = []
        try:
            conn = DBService.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT timestamp, termo_bloqueado, ip_address, acao FROM incidentes_seguranca ORDER BY id DESC LIMIT ?",
                (limite,)
            )
            for row in cursor.fetchall():
                incidentes.append({
                    "timestamp": row["timestamp"],
                    "termo_bloqueado": row["termo_bloqueado"],
                    "ip_address": row["ip_address"],
                    "acao": row["acao"]
                })
            conn.close()
        except Exception as e:
            print(f"[DB Error] Erro ao buscar incidentes: {e}")
        return incidentes
    
    @classmethod
    def listar_conversas(cls):

        import sqlite3

        conn = sqlite3.connect(DB_PATH)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM conversas
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        return [
            dict(row)
            for row in rows
        ]