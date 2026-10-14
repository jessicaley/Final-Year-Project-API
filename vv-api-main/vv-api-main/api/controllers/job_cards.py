from http.client import HTTPException
from fastapi import APIRouter, UploadFile, File, HTTPException
import asyncio
from ..Data.supabase import (
    get_job_cards_sb,
    get_job_card_sb,
    create_job_card_sb,
    log_error,
    update_job_card_sb,
    get_job_card_statuses_sb,
    get_job_card_status_sb, 
    get_completed_job_cards_sb,
    get_job_card_with_materials_sb,
    get_job_card_artisans_sb,
    get_job_card_update_sb,
    get_job_cards_employee_sb,
    upload_progress_image_sb ,
    get_quotation_sb,
    get_job_request_sb,
    get_job_cards_employee_with_details_sb
)
from ..models.job_card_model import job_card, JobCardWithMaterials, JobCardUpdate, JobCardCreate

router = APIRouter()

@router.get('/get_job_card_statuses')
async def get_job_card_statuses():
    return get_job_card_statuses_sb()

@router.get('/get_job_card_status/{job_card_status_id}')
async def get_job_card_status(job_card_status_id: int):
    return get_job_card_status_sb(job_card_status_id)

# Job Card Endpoints
@router.get('/get_job_cards')
async def get_job_cards():
    return get_job_cards_sb()

@router.get('/get_job_card/{job_card_id}')
async def get_job_card(job_card_id: int):
    return get_job_card_sb(job_card_id)

@router.get('/get_job_card_update/{job_card_id}')
async def get_job_card_update(job_card_id: int):
    return get_job_card_update_sb(job_card_id)

@router.post('/create_job_card')
async def create_job_card(job_card: JobCardCreate):  
    return create_job_card_sb(job_card)

@router.put('/update_job_card/{job_card_id}')
async def update_job_card(job_card_id: int, update_data: JobCardUpdate):
    return update_job_card_sb(job_card_id, update_data.dict())

@router.get('/get_completed_job_cards')
async def get_completed_job_cards():
    return get_completed_job_cards_sb()

@router.get('/get_job_card_with_materials/{job_card_id}', response_model=JobCardWithMaterials)
async def get_job_card_with_materials(job_card_id: int):
    result = get_job_card_with_materials_sb(job_card_id)
    
    if isinstance(result, Exception):
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching job card: {str(result)}"
        )
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="Job card not found"
        )
    
    return result

@router.get('/get_job_card_artisans/{job_card_id}')
async def get_job_card_artisans(job_card_id: int):
    return get_job_card_artisans_sb(job_card_id)

@router.get('/get_job_cards_employee/{employee_id}')
async def get_job_cards_employee(employee_id: int):
    """Get job cards for employee with status_id = 1 (Processing)"""
    return get_job_cards_employee_sb(employee_id)

@router.post("/upload_progress_image/{job_card_id}")
async def upload_progress_image(job_card_id: int, file: UploadFile = File(...)):
    """
    Upload a progress image for a job card.
    Replaces existing progress_url if one exists.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
            
        # Read file content
        file_bytes = await file.read()
        if len(file_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
            
        # Validate file size (e.g., 10MB max)
        if len(file_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")
        
        result = upload_progress_image_sb(
            job_card_id=job_card_id,
            file_content=file_bytes,
            filename=file.filename,
            content_type=file.content_type
        )
        
        return {
            "status": "success",
            "progress_url": result["progress_url"],
            "job_request_id": result["job_request_id"],
            "filename": result["filename"],
            "message": result.get("message", "Image uploaded successfully")
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        log_error(f"Upload progress image endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get('/get_job_cards_employee_with_details/{employee_id}')
async def get_job_cards_employee_with_details(employee_id: int):
    """Get job cards for employee with full details including job request"""
    try:
        job_cards = get_job_cards_employee_with_details_sb(employee_id)
        
        if isinstance(job_cards, Exception):
            raise HTTPException(status_code=500, detail=f"Error fetching job cards: {str(job_cards)}")
        
        return job_cards
        
    except Exception as e:
        log_error(f"Error in get_job_cards_employee_with_details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load job cards with details: {str(e)}")