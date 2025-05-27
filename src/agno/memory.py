from typing import List

import mysql.connector


class ExistingMySqlMemoryDb:
    def __init__(self, connection_config: dict, table_name: str = "conversaciones",
                 user_to_conversation_id: dict = None):
        self.conn = mysql.connector.connect(**connection_config)
        self.table = table_name
        self.user_to_conversation_id = user_to_conversation_id or {}

    def get_user_memories(self, user_id: str) -> List[dict]:
        conversation_id = self.user_to_conversation_id.get(user_id)
        if not conversation_id:
            return []

        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(f"""
            SELECT usuario, mensaje FROM {self.table}
            WHERE conversacion_id = %s
            ORDER BY fecha ASC
        """, (conversation_id,))

        return [
            {
                "role": "assistant" if row["usuario"] == "eva" else "user",
                "content": row["mensaje"]
            }
            for row in cursor.fetchall()
        ]

    def add_message(self, user_id: str, role: str, content: str):
        conversation_id = self.user_to_conversation_id.get(user_id)
        if not conversation_id:
            return

        usuario = "eva" if role == "assistant" else "usuario"
        cursor = self.conn.cursor()
        cursor.execute(f"""
            INSERT INTO {self.table} (conversacion_id, usuario, mensaje)
            VALUES (%s, %s, %s)
        """, (conversation_id, usuario, content))
        self.conn.commit()
