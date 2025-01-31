import google.generativeai as genai
from typing import Optional
from constants.app_constants import GEMINI_MODEL
from functools import lru_cache

class GeminiConnection:
    _instance: Optional['GeminiConnection'] = None
    
    def __new__(cls, api_key: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(api_key)
        return cls._instance
    
    def _initialize(self, api_key: str) -> None:
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    @lru_cache(maxsize=100)
    def get_model(self):
        return self.model
