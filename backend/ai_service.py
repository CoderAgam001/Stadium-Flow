from google import genai
from pydantic import BaseModel
from backend.config import GEMINI_MODEL

class RoutingResponse(BaseModel):
    recommendation: str
    key_note: str
    distance: int

class AIService:
    def __init__(self):
        try:
            self.client = genai.Client()
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini Client: {e}")
            self.client = None

    def get_structured_recommendation(self, user_zone, dest_zone, stadium_context, trends, dist_to_dest):
        if not self.client:
            return RoutingResponse(
                recommendation=f"Head towards {dest_zone['zone_name']}.",
                key_note="AI Service Offline. Follow physical signs.",
                distance=dist_to_dest
            )

        prompt = f"""
        You are an AI Crowd Controller for a Cricket Stadium.
        User is at: {user_zone['zone_name']}
        User wants to go to: {dest_zone['zone_name']} (Current Occupancy: {dest_zone['current_occupancy']}/{dest_zone['capacity']}, Trend: {trends.get(dest_zone['zone_id'], 'stable')})
        Direct Distance: {dist_to_dest} meters.

        Stadium State:
        {stadium_context}
        
        TASK:
        1. Analyze if the destination or the path to it is overcrowded.
        2. Suggest the BEST route. If the destination is too full, suggest a nearby alternative or a specific route to avoid bottlenecks.
        3. Provide clear, step-by-step navigation instruction.
        """

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config={'response_mime_type': 'application/json', 'response_schema': RoutingResponse}
            )
            return response.parsed
        except Exception as e:
            print(f"AI Error: {e}")
            return RoutingResponse(
                recommendation=f"Proceed to {dest_zone['zone_name']}.",
                key_note=f"Routing logic error: {e}",
                distance=dist_to_dest
            )

ai_service = AIService()
