from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from typing import List, Optional, Dict, Any
import logging

# Schema imports
from trm_api.schemas.win import WIN, WINCreate, WINUpdate, WINList

# Service imports
from trm_api.services.win_service import WinService, win_service

# Adapter imports
from trm_api.adapters.enum_adapter import normalize_win_status, normalize_win_type
from trm_api.adapters.datetime_adapter import normalize_datetime, normalize_dict_datetimes
from trm_api.adapters.decorators import adapt_win_response

# Repository imports
from trm_api.repositories.win_repository import WINRepository

router = APIRouter()

@router.post("/", response_model=WIN, status_code=status.HTTP_201_CREATED)
@adapt_win_response()
async def create_win(
    win_in: WINCreate,
    service: WinService = Depends(lambda: win_service)
):
    """
    Create new WIN (Wisdom-Infused Narrative) - AGE Semantic Action
    
    AGE Philosophy: WINs represent measurable strategic outcomes achieved
    through Recognition → Event → WIN orchestration.
    """
    try:
        logging.info(f"AGE: Creating new WIN với dữ liệu: {win_in.model_dump()}")
        
        # Normalize enum values
        win_data = win_in.model_dump()
        win_data["status"] = normalize_win_status(win_data.get("status"))
        win_data["win_type"] = normalize_win_type(win_data.get("win_type"))
        
        # Create WIN through AGE orchestration
        result = await service.create_win(win_data=win_data)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AGE: Cannot create WIN. Check orchestration logs."
            )
            
        logging.debug(f"AGE: WIN created successfully: {result}")
        return result
        
    except Exception as e:
        logging.error(f"AGE: Error creating WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AGE: WIN creation failed: {str(e)}"
        )

@router.get("/{win_id}")
async def get_win(
    win_id: str,
    service: WinService = Depends(lambda: win_service)
):
    """
    Get WIN by ID - AGE Semantic Retrieval
    
    AGE Philosophy: Retrieve strategic WIN outcomes for validation and learning.
    """
    try:
        logging.info(f"AGE: Retrieving WIN with ID: {win_id}")
        db_win = await service.get_win(win_id=win_id)
        
        if db_win is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"AGE: WIN not found with ID: {win_id}"
            )
        
        # Normalize enum and datetime values
        win_data = db_win
        if isinstance(win_data, dict):
            # Normalize enum values
            if "status" in win_data:
                win_data["status"] = normalize_win_status(win_data.get("status"))
            if "win_type" in win_data:
                win_data["win_type"] = normalize_win_type(win_data.get("win_type"))
            
            # Normalize datetime values
            win_data = normalize_dict_datetimes(win_data)
            
        logging.debug(f"AGE: WIN retrieved successfully: {win_data}")
        return win_data
        
    except HTTPException as e:
        logging.error(f"AGE: HTTP Exception retrieving WIN: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"AGE: Error retrieving WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AGE: WIN retrieval failed: {str(e)}"
        )

@router.get("/")
async def list_wins(
    skip: int = Query(0, ge=0, description="Items to skip for pagination"),
    limit: int = Query(25, ge=1, le=100, description="Maximum items to return"),
    service: WinService = Depends(lambda: win_service)
):
    """
    List WINs - AGE Semantic Intelligence Retrieval
    
    AGE Philosophy: List strategic WIN outcomes for analysis and learning.
    """
    try:
        logging.info(f"AGE: Listing WINs. Skip: {skip}, Limit: {limit}")
        
        # Get data from AGE service
        wins = await service.list_wins(skip=skip, limit=limit)
        
        # Handle empty results
        if not wins:
            logging.info("AGE: No WINs found")
            return {"items": [], "count": 0}
        
        # Normalize data before returning
        normalized_items = []
        error_items = []
        
        for item in wins:
            try:
                if isinstance(item, dict):
                    # Normalize enum values
                    if "status" in item:
                        item["status"] = normalize_win_status(item.get("status"))
                    if "win_type" in item:
                        item["win_type"] = normalize_win_type(item.get("win_type"))
                        
                    # Normalize datetime values
                    normalized_item = normalize_dict_datetimes(item)
                    normalized_items.append(normalized_item)
                else:
                    # May already be Pydantic model
                    normalized_items.append(item)
            except Exception as e:
                logging.error(f"AGE: Error normalizing WIN item: {str(e)}. Item: {item}")
                error_items.append({"item": item, "error": str(e)})
        
        # Report errors if any
        if error_items:
            logging.warning(f"AGE: {len(error_items)} items had normalization errors")
            
        result = {"items": normalized_items, "count": len(wins)}
        logging.debug(f"AGE: WIN list result: {len(normalized_items)} items")
        return result
        
    except Exception as e:
        logging.error(f"AGE: Error listing WINs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AGE: WIN listing failed: {str(e)}"
        )

@router.put("/{win_id}")
async def update_win(
    win_id: str,
    win_in: WINUpdate,
    service: WinService = Depends(lambda: win_service)
):
    """
    Update WIN - AGE Semantic Modification
    
    AGE Philosophy: Update strategic WIN outcomes for enhanced accuracy.
    """
    try:
        logging.info(f"AGE: Updating WIN with ID: {win_id}. Data: {win_in.model_dump()}")
        
        # Check if WIN exists
        db_win = await service.get_win(win_id=win_id)
        if db_win is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"AGE: WIN not found with ID: {win_id}"
            )
        
        # Update WIN through AGE orchestration
        updated_win = await service.update_win(win_id=win_id, win_update=win_in)
        
        if not updated_win:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="AGE: WIN update failed. Check orchestration logs."
            )
        
        # Normalize data before returning
        normalized_result = normalize_dict_datetimes(updated_win)
        logging.debug(f"AGE: WIN updated successfully. Result: {normalized_result}")
        return normalized_result
        
    except HTTPException as e:
        logging.error(f"AGE: HTTP Exception updating WIN: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"AGE: Error updating WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AGE: WIN update failed: {str(e)}"
        )

@router.delete("/{win_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_win(
    win_id: str,
    service: WinService = Depends(lambda: win_service)
):
    """
    Delete WIN - AGE Semantic Removal
    
    AGE Philosophy: Remove WIN outcomes that are no longer valid or needed.
    """
    try:
        logging.info(f"AGE: Deleting WIN with ID: {win_id}")
        
        # Check if WIN exists
        db_win = await service.get_win(win_id=win_id)
        if db_win is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"AGE: WIN not found with ID: {win_id}"
            )
        
        # Delete WIN through AGE orchestration
        success = await service.delete_win(win_id=win_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="AGE: WIN deletion failed. Check orchestration logs."
            )
        
        logging.debug(f"AGE: WIN deleted successfully: {win_id}")
        return None
        
    except HTTPException as e:
        logging.error(f"AGE: HTTP Exception deleting WIN: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"AGE: Error deleting WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AGE: WIN deletion failed: {str(e)}"
        )

@router.get("/{win_id}/sources", response_model=Dict[str, List])
def get_win_sources(
    win_id: str,
    repository: WINRepository = Depends(lambda: WINRepository())
):
    """
    Get WIN sources - AGE Semantic Source Tracking
    
    AGE Philosophy: Track sources contributing to WIN achievement for learning.
    """
    try:
        logging.info(f"AGE: Getting sources for WIN: {win_id}")
        return repository.get_win_sources(win_id)
    except Exception as e:
        logging.error(f"AGE: Error getting WIN sources: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AGE: Source retrieval failed: {str(e)}")

@router.post("/{win_id}/source-projects/{project_id}", status_code=status.HTTP_201_CREATED)
def connect_project_to_win(
    win_id: str,
    project_id: str,
    relationship_data: Dict[str, Any] = Body(...),
    repository: WINRepository = Depends(lambda: WINRepository())
):
    """
    Connect Strategic Unit to WIN - AGE Semantic Relationship
    
    AGE Philosophy: Connect Strategic Units to WINs for outcome tracking.
    """
    try:
        logging.info(f"AGE: Connecting Strategic Unit {project_id} to WIN {win_id}")
        
        # Validate required fields
        if not relationship_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="AGE: Relationship data is required"
            )
        
        # Create relationship through AGE orchestration
        result = repository.connect_project_to_win(
            win_id=win_id,
            project_id=project_id,
            relationship_data=relationship_data
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AGE: Failed to connect Strategic Unit to WIN"
            )
        
        logging.debug(f"AGE: Strategic Unit connected to WIN successfully")
        return {"message": "AGE: Strategic Unit connected to WIN successfully", "relationship": result}
        
    except HTTPException as e:
        raise
    except Exception as e:
        logging.error(f"AGE: Error connecting Strategic Unit to WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AGE: Connection failed: {str(e)}"
        )

@router.delete("/{win_id}/source-projects/{project_id}")
def disconnect_project_from_win(
    win_id: str,
    project_id: str,
    repository: WINRepository = Depends(lambda: WINRepository())
):
    """
    Disconnect Strategic Unit from WIN - AGE Semantic Relationship Removal
    
    AGE Philosophy: Remove Strategic Unit connections that are no longer valid.
    """
    try:
        logging.info(f"AGE: Disconnecting Strategic Unit {project_id} from WIN {win_id}")
        
        success = repository.disconnect_project_from_win(
            win_id=win_id,
            project_id=project_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AGE: Connection not found or disconnection failed"
            )
        
        logging.debug(f"AGE: Strategic Unit disconnected from WIN successfully")
        return {"message": "AGE: Strategic Unit disconnected from WIN successfully"}
        
    except HTTPException as e:
        raise
    except Exception as e:
        logging.error(f"AGE: Error disconnecting Strategic Unit from WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AGE: Disconnection failed: {str(e)}"
        )
