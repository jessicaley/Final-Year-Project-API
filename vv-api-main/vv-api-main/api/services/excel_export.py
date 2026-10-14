from fastapi.responses import StreamingResponse
from io import BytesIO
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def export_stock_to_excel(data: list):
    try:
        # Create DataFrame with required columns
        required_columns = ['stock_id', 'name', 'stock_price', 'stock_level']  # Added stock_level
        df = pd.DataFrame(data)
        
        # Ensure required columns exist
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing columns in data: {missing_cols}")
            return None
        
        df = df[required_columns]
        
        # Create in-memory Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Stock Report')
            
            workbook = writer.book
            worksheet = writer.sheets['Stock Report']
            
            # Format headers
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            # Apply formatting to headers
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Auto-adjust column widths
            for idx, col in enumerate(df.columns):
                max_len = max(
                    df[col].astype(str).map(len).max(),
                    len(str(col)) + 2
                )
                worksheet.set_column(idx, idx, min(max_len, 50))
            
            # Format price column as South African Rand (ZAR)
            if 'price' in df.columns:
                zar_format = workbook.add_format({'num_format': 'R#,##0'})
                worksheet.set_column(2, 2, 15, zar_format)  # Column C (index 2)
            
            # Format stock_level with comma separators
            if 'stock_level' in df.columns:
                num_format = workbook.add_format({'num_format': '#,##0'})
                worksheet.set_column(3, 3, 15, num_format)  # Column D (index 3)
        
        output.seek(0)
        return output
    except Exception as e:
        logger.exception("Excel generation failed")
        return None
    
def export_materials_to_excel(data: list):
    try:
        # Create DataFrame with required columns
        required_columns = ['material_name']  # Only material_name column
        df = pd.DataFrame(data)
        
        # Ensure required columns exist
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing columns in material data: {missing_cols}")
            return None
        
        df = df[required_columns]
        
        # Create in-memory Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Materials')
            
            workbook = writer.book
            worksheet = writer.sheets['Materials']
            
            # Format headers
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            # Apply formatting to headers
            worksheet.write(0, 0, "Material Name", header_format)
            
            # Auto-adjust column width
            max_len = df['material_name'].astype(str).map(len).max()
            max_len = max(max_len, len("Material Name")) + 2
            worksheet.set_column(0, 0, min(max_len, 50))
        
        output.seek(0)
        return output
    except Exception as e:
        logger.exception("Material Excel generation failed")
        return None