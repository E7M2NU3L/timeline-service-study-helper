from typing import Dict, Optional, List, Any
from datetime import datetime
from models.timeline_model import StudyPlan, Progress
from apptypes.timeline_types import PromptTypes
from config.connectDb import Database
from config.connectRedis import Redis
from config.connectGemini import GeminiConnection
from services.gemini_service import PromptGenerator
from constants.app_constants import CacheKeys, ResponseStatus
import json

class TimelineService:
    def __init__(
        self,
        db: Database,
        redis_client: Redis,
        gemini: GeminiConnection
    ):
        self.db = db
        self.redis = redis_client
        self.gemini = gemini

    async def create_study_plan(
        self,
        user_id: str,
        prompt_data: PromptTypes
    ) -> Dict[str, Any]:
        try:
            # Generate prompt
            prompt_generator = PromptGenerator(prompt_data)
            prompt = prompt_generator.generate_prompt()
            
            # Get response from Gemini
            model = self.gemini.get_model()
            response = await model.generate_content(prompt)
            
            # Parse and validate response
            study_plan = json.loads(response.text)
            
            # Store in database
            session = self.db.get_session()
            db_plan = StudyPlan(
                user_id=user_id,
                prompt_data=prompt_data.__dict__,
                generated_plan=study_plan
            )
            session.add(db_plan)
            session.commit()
            
            # Cache the result
            cache_key = CacheKeys.STUDY_PLAN.value.format(db_plan.id)
            self.redis.get_client().setex(
                cache_key,
                3600,  # 1 hour
                json.dumps(study_plan)
            )
            
            return {
                "status": ResponseStatus.SUCCESS.value,
                "plan_id": db_plan.id,
                "study_plan": study_plan
            }
            
        except Exception as e:
            return {
                "status": ResponseStatus.FAILURE.value,
                "error": str(e)
            }

    def update_progress(
        self,
        plan_id: int,
        completed_topics: List[str]
    ) -> Dict[str, Any]:
        try:
            session = self.db.get_session()
            
            # Get total topics from study plan
            study_plan = session.query(StudyPlan).filter_by(id=plan_id).first()
            total_topics = len(study_plan.generated_plan["timeline"])
            
            # Calculate progress
            progress_percentage = (len(completed_topics) / total_topics) * 100
            
            # Update progress
            progress = Progress(
                study_plan_id=plan_id,
                completed_topics=completed_topics,
                progress_percentage=progress_percentage
            )
            session.add(progress)
            session.commit()
            
            return {
                "status": ResponseStatus.SUCCESS.value,
                "progress": progress_percentage
            }
            
        except Exception as e:
            return {
                "status": ResponseStatus.FAILURE.value,
                "error": str(e)
            }

    def get_study_plan(self, plan_id: int) -> Optional[Dict[str, Any]]:
        # Try cache first
        cache_key = CacheKeys.STUDY_PLAN.value.format(plan_id)
        cached_plan = self.redis.get_client().get(cache_key)
        
        if cached_plan:
            return json.loads(cached_plan)
        
        # If not in cache, get from DB
        session = self.db.get_session()
        plan = session.query(StudyPlan).filter_by(id=plan_id).first()
        
        if plan:
            # Update cache
            self.redis.get_client().setex(
                cache_key,
                3600,
                json.dumps(plan.generated_plan)
            )
            return plan.generated_plan
            
        return None