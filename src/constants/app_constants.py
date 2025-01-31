from enum import Enum

class ResponseStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class CacheKeys(Enum):
    STUDY_PLAN = "STUDY_PLAN:{}"
    USER_PROGRESS = "USER_PROGRESS:{}"

GEMINI_MODEL = "gemini-pro"
CACHE_EXPIRY = 60 * 60 * 24  # 24 hours
