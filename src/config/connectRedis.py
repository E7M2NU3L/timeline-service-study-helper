import redis
from typing import Optional
import os

class Redis:
    _instance: Optional['Redis'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize Redis connection with Redis Cloud credentials"""
        self.client = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
            username=os.getenv('REDIS_USERNAME'),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True,  # Automatically decode responses to Python strings
            ssl=True,  # Enable SSL for Redis Cloud
            ssl_cert_reqs=None  # Skip certificate verification
        )
    
    def get_client(self) -> redis.Redis:
        """Get Redis client instance"""
        return self.client
    
    def test_connection(self) -> bool:
        """Test if Redis connection is working"""
        try:
            self.client.ping()
            return True
        except redis.ConnectionError:
            return False