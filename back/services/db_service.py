import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "pibot.db")

class DBService:
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def init_db():
        with DBService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    mensagem TEXT NOT NULL,
                    resposta TEXT NOT NULL,
                    tipo TEXT NOT NULL
                )
            """)
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
        print(f"[DB] Banco de dados inicializado em: {DB_PATH}")

    @staticmethod
    def registrar_conversa(mensagem, resposta, tipo):
        try:
            with DBService.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO conversas (mensagem, resposta, tipo) VALUES (?, ?, ?)",
                    (mensagem, resposta, tipo)
                )
                conn.commit()
        except Exception as e:
            print(f"[DB Error] registrar_conversa: {e}")

    @staticmethod
    def registrar_incidente(termo_bloqueado, ip_address, acao):
        try:
            with DBService.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO incidentes_seguranca (termo_bloqueado, ip_address, acao) VALUES (?, ?, ?)",
                    (termo_bloqueado, ip_address, acao)
                )
                conn.commit()
        except Exception as e:
            print(f"[DB Error] registrar_incidente: {e}")

    @staticmethod
    def obter_estatisticas():
        stats = {"total": 0, "ia": 0, "local": 0, "fallback": 0, "attacks": 0}
        try:
            with DBService.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM conversas")
                stats["total"] = cursor.fetchone()[0]
                
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
                
                cursor.execute("SELECT COUNT(*) FROM incidentes_seguranca WHERE acao = 'lockdown_active'")
                stats["attacks"] = cursor.fetchone()[0]
        except Exception as e:
            print(f"[DB Error] obter_estatisticas: {e}")
        return stats

    @staticmethod
    def obter_logs(limite=50):
        logs = []
        try:
            with DBService.get_connection() as conn:
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
        except Exception as e:
            print(f"[DB Error] obter_logs: {e}")
        return logs

    @staticmethod
    def obter_incidentes(limite=50):
        incidentes = []
        try:
            with DBService.get_connection() as conn:
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
        except Exception as e:
            print(f"[DB Error] obter_incidentes: {e}")
        return incidentes
    
    @staticmethod
    def listar_conversas():
        try:
            with DBService.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM conversas ORDER BY id DESC")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[DB Error] listar_conversas: {e}")
            return []