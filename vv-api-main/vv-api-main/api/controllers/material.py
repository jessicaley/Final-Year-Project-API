from ..Data.supabase import get_material_sb, get_materials_sb, get_materials_export_sb
from fastapi import APIRouter, UploadFile, File
from ..models.material_model import material
from ..services.excel_export import export_materials_to_excel
from ..services.excel_import import import_materials_from_excel
import logging
from fastapi.responses import StreamingResponse



router = APIRouter()
logger = logging.getLogger(__name__)



@router.get('/get_materials')
async def get_materials():
    try:
        response = get_materials_sb()
        return response
    except Exception as error:
        return {"error": error }
    
@router.get('/get_material/{material_id}')
async def get_material(material_id:int):
    try:
        response = get_material_sb(material_id)
        return response
    except Exception as error:
        return {"error": error }    
    
@router.get('/export_material_excel')
async def export_material_excel():
    try:
        # Get material data
        material_data = get_materials_export_sb()
        
        # Handle errors
        if isinstance(material_data, Exception):
            logger.error(f"Material export error: {str(material_data)}")
            return {"error": "Failed to fetch material data"}
        if not material_data:
            return {"error": "No materials found"}
        
        # Generate Excel file
        excel_file = export_materials_to_excel(material_data)
        if not excel_file:
            return {"error": "Failed to generate Excel file"}
        
        # Return as downloadable response
        return StreamingResponse(
            content=excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=materials_export.xlsx",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as error:
        logger.exception("Material export failed")
        return {"error": str(error)}
    
@router.post('/import_material_excel')
async def import_material_excel(file: UploadFile = File(...)):
    try:
        # Verify file type
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return {"error": "Invalid file format. Only Excel files are accepted"}
        
        # Read uploaded file content
        content = await file.read()
        
        # Check file size
        if len(content) == 0:
            return {"error": "Uploaded file is empty"}
        
        # Process and import materials
        result = import_materials_from_excel(content)
        
        # Handle import results
        if isinstance(result, Exception):
            # Return detailed error message
            return {"error": f"Import failed: {str(result)}"}
        
        if "error" in result:
            return result
        
        return {
            "message": "Materials imported successfully",
            "new_materials": result["inserted_count"],
            "duplicates": result["duplicate_count"]
        }
    except Exception as error:
        logger.exception(f"Material import failed: {str(error)}")
        return {"error": f"Unexpected error: {str(error)}"}