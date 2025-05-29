from typing import Dict, List
import os
import boto3
from opensearchpy import RequestsHttpConnection, AWSV4SignerAuth
from mem0 import Memory #type: ignore
from src.config.const import MEM0_API_KEY, AWS_ACCESS_LINK


"""
expected input
messages = [
    {"role": "user", "content": "Hi, I'm Alex. I'm a vegetarian and I'm allergic to nuts."},
    {"role": "assistant", "content": "Hello Alex! I've noted that you're a vegetarian and have a nut allergy. I'll keep this in mind for any food-related recommendations or discussions."}
]
client.add(messages, user_id="alex", metadata={"food": "vegan"})

"""
# Configuración para OpenSearch en AWS
def get_mem0_config():
    # Región y servicio AWS
    region = os.environ.get('AWS_REGION', 'us-west-1')
    # Usar 'aoss' para Amazon OpenSearch Serverless o 'es' para OpenSearch Service
    service = os.environ.get('AWS_SERVICE', 'aoss')
    
    # Obtener credenciales AWS del entorno, archivo ~/.aws/credentials, o rol IAM
    session = boto3.Session()
    credentials = session.get_credentials()
    
    # Verificar si tenemos credenciales
    if not credentials:
        raise ValueError("No se pudieron encontrar credenciales AWS. Configura AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY")
    
    # Crear autenticación AWS v4
    auth = AWSV4SignerAuth(credentials, region, service)
    
    # Configuración para mem0 con OpenSearch
    config = {
        "vector_store": {
            "provider": "opensearch",
            "config": {           
                "collection_name": "mem0",
                "host": AWS_ACCESS_LINK,
                "port": 443,
                "http_auth": auth,
                "embedding_model_dims": 1024,
                "connection_class": RequestsHttpConnection,
                "pool_maxsize": 20,
                "use_ssl": True,
                "verify_certs": True
            }
        },
    }
    
    return config


class MemoryManager:
    def __init__(self, memory: Memory = None):
        try:
            # Usar memoria existente o crear una nueva con la configuración
            self.memory = memory if memory else Memory.from_config(get_mem0_config())
            print("✅ Conexión exitosa a la memoria con OpenSearch")
        except Exception as e:
            print(f"❌ Error al inicializar memoria: {str(e)}")
            # Fallback a memoria local si hay error
      

    
    def save_user_memory(
        self,
        user_id: str,
        conversation_id: str,
        memory_from_user: List[Dict[str, str]],
    ) -> bool:
        try:
            self.memory.add(
                memory_from_user,
                user_id=user_id,
                run_id=conversation_id,
            )

            return True

        except Exception as e:
            print(f"Error saving memories: {str(e)}")
            return False

    """query = "What should I cook for dinner today?"

        client.search(query, user_id="alex")"""

    def get_user_memory_conversation(
        self,
        query: str,
        user_id: str,
        conversation_id: str,
    ) -> List[str]:
        try:
            all_memories = self.memory.search(
                query, user_id=user_id, run_id=conversation_id
            )["results"]

            return [user_memory["memory"] for user_memory in all_memories]

        except Exception as e:
            print(f"Error retrieving memories: {str(e)}")
            return []

    def save_chat_memory(
        self,
        channel_id: str,
        conversation_id: str,
        chat_messages: List[Dict[str, str]],
    ) -> bool:
        try:
            self.memory.add(
                chat_messages,
                user_id=channel_id,
                run_id=conversation_id,
            )
            return True
        except Exception as e:
            print(f"Error saving chat memory: {str(e)}")
            return False

    def get_chat_memory(
        self,
        query: str,
        channel_id: str,
        conversation_id: str,
    ) -> List[str]:
        try:
            all_memories = self.memory.search(
                query, user_id=channel_id, run_id=conversation_id
            )["results"]

            return [user_memory["memory"] for user_memory in all_memories]

        except Exception as e:
            print(f"Error retrieving memories: {str(e)}")
            return []
