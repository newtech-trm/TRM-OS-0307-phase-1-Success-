from fastapi import APIRouter

# Sử dụng lazy import để tránh vòng lặp import
api_router = APIRouter()

# --- Active Routers ---

# Import các router khi cần sử dụng để tránh vòng lặp import
from trm_api.api.v1.endpoints import project
api_router.include_router(project.router, prefix="/projects", tags=["Projects"])

from trm_api.api.v1.endpoints import user
api_router.include_router(user.router, prefix="/users", tags=["users"])

from trm_api.api.v1.endpoints import task
api_router.include_router(task.router, prefix="/tasks", tags=["Tasks"])

from trm_api.api.v1.endpoints import team
api_router.include_router(team.router, prefix="/teams", tags=["Teams"])

from trm_api.api.v1.endpoints import skill
api_router.include_router(skill.router, prefix="/skills", tags=["Skills"])

from trm_api.api.v1.endpoints import tension
api_router.include_router(tension.router, prefix="/tensions", tags=["Tensions"])

from trm_api.api.v1.endpoints import resource
api_router.include_router(resource.router, prefix="/resources", tags=["Resources"])

# --- Deprecated Routers ---

# --- TODO: Re-enable these routers after they are refactored to use repositories ---
from trm_api.api.v1.endpoints import win
api_router.include_router(win.router, prefix="/wins", tags=["WINs"])

from trm_api.api.v1.endpoints import recognition
api_router.include_router(recognition.router, prefix="/recognitions", tags=["Recognitions"])

from trm_api.api.v1.endpoints import relationship
api_router.include_router(relationship.router, prefix="/relationships", tags=["Relationships"])

from trm_api.api.v1.endpoints import knowledge_snippet
api_router.include_router(knowledge_snippet.router, prefix="/knowledge-snippets", tags=["Knowledge Snippets"])

from trm_api.api.v1.endpoints import agent
api_router.include_router(agent.router, prefix="/agents", tags=["Agents"])

from trm_api.api.v1.endpoints import event
api_router.include_router(event.router, prefix="/events", tags=["Events"])
# api_router.include_router(tool.router, prefix="/tools", tags=["Tools"])

from trm_api.api.v1.endpoints import validate
api_router.include_router(validate.router, tags=["Validation"])
