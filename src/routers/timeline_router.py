from flask import Blueprint, request, jsonify
from services.timeline_service import TimelineService
from apptypes.timeline_types import PromptTypes
from typing import Dict, Any

timeline_bp = Blueprint('timeline', __name__)
timeline_service = TimelineService(db, redis_client, gemini)  # Pass the required arguments

@timeline_bp.route('/study-plan', methods=['POST'])
async def create_study_plan() -> Dict[str, Any]:
    try:
        data = request.get_json()
        prompt_data = PromptTypes(**data)
        user_id = request.headers.get('user-id')
        
        result = await timeline_service.create_study_plan(user_id, prompt_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "FAILURE",
            "error": str(e)
        }), 400

@timeline_bp.route('/progress/<int:plan_id>', methods=['POST'])
def update_progress(plan_id: int) -> Dict[str, Any]:
    try:
        data = request.get_json()
        completed_topics = data.get('completed_topics', [])
        
        result = timeline_service.update_progress(plan_id, completed_topics)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "FAILURE",
            "error": str(e)
        }), 400

@timeline_bp.route('/study-plan/<int:plan_id>', methods=['GET'])
def get_study_plan(plan_id: int) -> Dict[str, Any]:
    try:
        plan = timeline_service.get_study_plan(plan_id)
        if plan:
            return jsonify({
                "status": "SUCCESS",
                "study_plan": plan
            })
        return jsonify({
            "status": "FAILURE",
            "error": "Plan not found"
        }), 404
        
    except Exception as e:
        return jsonify({
            "status": "FAILURE",
            "error": str(e)
        }), 400
