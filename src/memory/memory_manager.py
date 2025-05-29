from typing import Dict, List

from mem0 import Memory #type: ignore
from src.config.const import MEM0_API_KEY, AWS_ACCESS_LINK
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


"""
expected input
messages = [
    {"role": "user", "content": "Hi, I'm Alex. I'm a vegetarian and I'm allergic to nuts."},
    {"role": "assistant", "content": "Hello Alex! I've noted that you're a vegetarian and have a nut allergy. I'll keep this in mind for any food-related recommendations or discussions."}
]
client.add(messages, user_id="alex", metadata={"food": "vegan"})

"""
region = 'us-west-2'
service = 'aoss'
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

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
    }
}


class MemoryManager:
    def __init__(self, memory: Memory = None):
        self.memory = memory if memory else Memory.from_config(config)


    
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
