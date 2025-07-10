#!/usr/bin/env python3
"""
WIN Repository - AGE Semantic Architecture
Handles WIN phase của Recognition → Event → WIN pattern
"""

from typing import List, Optional, Dict, Any
from neomodel import DoesNotExist

from trm_api.graph_models.win import WIN as GraphWIN
from trm_api.models.win import WinCreate, WinUpdate
from trm_api.graph_models.strategic_project import GraphStrategicProject  # Replaced legacy Project
from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)

class WINRepository:
    """AGE WIN Repository - Semantic WIN achievement tracking"""
    
    def create_win(self, win_data: WinCreate) -> GraphWIN:
        """Create WIN achievement in AGE semantic context"""
        try:
            win = GraphWIN(
                title=win_data.title,
                description=win_data.description,
                win_type=win_data.win_type,
                strategic_value=win_data.strategic_value,
                impact_scope=win_data.impact_scope,
                verification_status=win_data.verification_status or "pending",
                achieved_date=win_data.achieved_date,
                strategic_context=win_data.strategic_context or {},
                measurable_outcomes=win_data.measurable_outcomes or {},
                learning_insights=win_data.learning_insights or []
            ).save()
            
            logger.info(f"AGE WIN created: {win.uid} - {win.title}")
            return win
            
        except Exception as e:
            logger.error(f"AGE WIN creation error: {str(e)}")
            raise

    def get_win_by_id(self, win_id: str) -> Optional[GraphWIN]:
        """Get WIN by ID with AGE semantic validation"""
        try:
            return GraphWIN.nodes.get_or_none(uid=win_id)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"AGE WIN retrieval error: {str(e)}")
            return None

    def list_wins(self, skip: int = 0, limit: int = 100) -> List[GraphWIN]:
        """List WINs with AGE semantic context"""
        try:
            wins = GraphWIN.nodes.all()[skip:skip+limit]
            logger.info(f"AGE WIN Repository: Listed {len(wins)} strategic WINs")
            return wins
        except Exception as e:
            logger.error(f"AGE WIN listing error: {str(e)}")
            return []

    def update_win(self, uid: str, win_data: WinUpdate) -> Optional[GraphWIN]:
        """Update WIN with AGE strategic enhancements"""
        try:
            win = self.get_win_by_id(uid)
            if not win:
                return None
            
            update_fields = win_data.dict(exclude_unset=True)
            for field, value in update_fields.items():
                if hasattr(win, field):
                    setattr(win, field, value)
            
            win.save()
            logger.info(f"AGE WIN updated: {win.uid}")
            return win
            
        except Exception as e:
            logger.error(f"AGE WIN update error: {str(e)}")
            return None

    def delete_win(self, uid: str) -> bool:
        """Delete WIN with AGE semantic validation"""
        try:
            win = self.get_win_by_id(uid)
            if win:
                win.delete()
                logger.info(f"AGE WIN deleted: {uid}")
                return True
            return False
        except Exception as e:
            logger.error(f"AGE WIN deletion error: {str(e)}")
            return False
