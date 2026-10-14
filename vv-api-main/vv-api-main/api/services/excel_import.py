import pandas as pd
from io import BytesIO
import logging
from ..Data.supabase import import_materials_sb

logger = logging.getLogger(__name__)

def import_materials_from_excel(file_content: bytes):
    try:
        # Read Excel using pandas
        df = pd.read_excel(BytesIO(file_content))
        
        # Extract material names from first column
        if len(df.columns) == 0:
            return {"error": "Excel file has no columns"}
        
        # Get materials from first column
        materials = df.iloc[:, 0].dropna().astype(str).str.strip().tolist()
        
        # Filter out empty strings and normalize case
        materials = [name.strip() for name in materials if name.strip()]
        
        if not materials:
            return {"inserted_count": 0, "duplicate_count": 0}
        
        # Insert into database
        result = import_materials_sb(materials)
        
        if isinstance(result, Exception):
            return result
        
        return result
    except Exception as e:
        logger.exception(f"Material import failed: {str(e)}")
        return Exception(f"Excel processing failed: {str(e)}")