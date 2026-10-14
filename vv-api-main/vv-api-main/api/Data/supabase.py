from supabase import create_client
from ..config import settings
from ..models.role_model import role, role_claim, role_claim_line
from ..models.quotation_model import quotation
from ..models.job_card_model import JobCardCreate
from ..models.user_model import user, UserUpdate
from ..models.type_model import type
from ..models.employee_model import employee
from ..models.employee_pay_slip_model import employee_pay_slip
from ..models.employee_warning_model import employee_warning
from ..models.receipt_model import receipt 
from ..models.customers_model import customer, updateCustomer
from ..models.job_request_model import job_request, job_request_insert
from ..models.general_model import contact_us, logout_timer
from ..models.invoice_model import invoice
from ..models.stock_model import stock
from ..models.pattern_model import pattern
from ..models.delivery_note_model import delivery_note
from ..models.employee_time_log_model import EmployeeTimeLog
from datetime import datetime, timedelta
from fastapi import UploadFile
import uuid
import os
from fastapi import HTTPException
from datetime import datetime, timedelta


print_logs = True

# Connect To SB

def get_supabase_client(is_admin:bool = False):
    if is_admin:
        return create_client(settings.SUPA_URL,settings.SUPA_SERVICE_KEY)
    else:
        return create_client(settings.SUPA_URL,settings.SUPA_ANON_KEY)
    
    
# Error Logger

def log_error(message:str = None):
    if message is not None: 
        try:
            db = get_supabase_client(True)
            response = db.schema(settings.SUPA_SCHEMA) \
            .table("error_logs") \
            .insert({ 
                     "message": message
                     
                     
                    }) \
            .execute()          
       
            if print_logs is True:
                print(message)
     
        except Exception as error:
            print(error)
            return error
        
auth_users = [
    { "name":"Krishna","user_id":"d1952d0b-80d0-47f8-816f-dfce57e43d1f","phone": "27614639706"},
    { "name":"Jess","user_id":"7e8b435e-18a9-4b25-b63a-a6cd824fbd8f","phone": "27605446259"},
    { "name":"Joao","user_id":"de0575d4-8b2a-42cd-9708-0b4f01af958e","phone":"27713905806"},
    { "name":"Jarred","user_id":"247da2f8-1dd9-4245-930a-d389b0aa1a8a","phone":"27832092706"},
    { "name":"Ndumiso","user_id":"2f6c9f2d-7b1c-41d4-ae88-62fea7f47567","phone":"27813250429"},
    { "name":"Support","user_id":"dd7b36e7-b573-473a-a807-15c128b41816","phone":"27671728770"},
]

async def set_users():
    try:         
        db = get_supabase_client(True)
        for user in auth_users:        
            res = db.auth.admin.update_user_by_id( user["user_id"], {
                "phone": user["phone"],
                "email_confirm": True,
                "phone_confirm": True,
            })     
        return "completed"
    except Exception as error:
        log_error(error)
        return error
        
             
# Endpoints To SB


# General
def get_revenue_data_sb():
    try:
        db = get_supabase_client(True)

        # Call the SQL function we created
        response = db.rpc("get_revenue_last_six_months").execute()

        if hasattr(response, "data"):
            return response.data  
        return response

    except Exception as error:
        log_error(error)
        return {"error": str(error)}

def get_pending_job_requests_sb(filter_period: str):
    try:
        db = get_supabase_client(True)

        query = db.schema(settings.SUPA_SCHEMA) \
            .table("job_request") \
            .select("*, customers:customer_id(*, user(*))") \
            .eq("job_request_status_id", 1)  # Pending status

        # Calculate cutoff datetime in Python
        now = datetime.utcnow()
        if filter_period == 'week':
            cutoff = now - timedelta(weeks=1)
            query = query.gte('created_at', cutoff.isoformat())
        elif filter_period == 'month':
            cutoff = now - timedelta(days=30)
            query = query.gte('created_at', cutoff.isoformat())
        elif filter_period == 'year':
            cutoff = now - timedelta(days=365)
            query = query.gte('created_at', cutoff.isoformat())

        response = query.execute()
        return response.data

    except Exception as error:
        log_error(error)
        return error


def get_job_completion_timeline_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_completion_timeline") \
            .select("*") \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

def get_titles_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("title") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error

def contact_us_sb(contact:contact_us):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("contact") \
        .insert({ 
                    "subject": contact.subject,
                    "message": contact.message,
                    "user_id": contact.user_id,                                
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
 

#Timer

def get_logout_timer_sb(timer_id:int):
        try:
            db = get_supabase_client(True)
            response = db.schema(settings.SUPA_SCHEMA) \
                .table("logout_timer") \
                .select("*") \
                .eq("timer_id",timer_id) \
                .execute() 
            return response.data          
        except Exception as error:
            log_error(error)
            return error
 
 
def update_logout_timer_sb(timer_id:int,logout_timer:logout_timer):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("logout_timer") \
        .update({ 
                "time": logout_timer.time
                
                }) \
        .eq("timer_id", timer_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error

# Stock type

def get_stock_types_sb():   
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("stock_type") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def get_stock_type_sb(stock_type_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("stock_type") \
        .select("*") \
        .eq("stock_type_id",stock_type_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error
    
# Stock Structure
def get_stock_structure_sb():   
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("stock_structure") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
# Stock Categories
def create_stock_category_sb(category_name: str):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock_category") \
            .insert({
                "category_name": category_name
            }) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

def update_stock_category_sb(category_id: int, category_name: str):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock_category") \
            .update({
                "category_name": category_name
            }) \
            .eq("stock_category_id", category_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

def delete_stock_category_sb(category_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock_category") \
            .delete() \
            .eq("stock_category_id", category_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

# Stock Types
def create_stock_type_sb(type_name: str, category_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock_type") \
            .insert({
                "type_name": type_name,
                "stock_category_id": category_id
            }) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

def update_stock_type_sb(type_id: int, type_name: str, category_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock_type") \
            .update({
                "type_name": type_name,
                "stock_category_id": category_id
            }) \
            .eq("stock_type_id", type_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

def delete_stock_type_sb(type_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock_type") \
            .delete() \
            .eq("stock_type_id", type_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

# Stock Items (already have create/update, need delete)
def delete_stock_sb(stock_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock") \
            .delete() \
            .eq("stock_id", stock_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

# Move stock item to different type
def move_stock_to_type_sb(stock_id: int, new_type_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock") \
            .update({
                "stock_type_id": new_type_id
            }) \
            .eq("stock_id", stock_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

# Move stock type to different category
def move_type_to_category_sb(type_id: int, new_category_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock_type") \
            .update({
                "stock_category_id": new_category_id
            }) \
            .eq("stock_type_id", type_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error


# Stock

def get_all_stock_sb():   
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("stock_with_details") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def get_stock_sb(stock_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("stock_with_details") \
        .select("*") \
        .eq("stock_id",stock_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error
    
def get_stock_categories_sb():   
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("stock_category") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error

    
def create_stock_sb(stock:stock):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("stock") \
        .insert({ 
                # "stock_id": stock.stock_id,
                "stock_type_id": stock.stock_type_id,
                "material_id": stock.material_id,
                "name": stock.name,
                "description": stock.description,
                "stock_level": stock.stock_level,
                "stock_price": stock.stock_price,               
                     
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def update_stock_sb(stock_id:int,stock:stock):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("stock") \
        .update({ 
                #"stock_id": stock.stock_id,
                "stock_type_id": stock.stock_type_id,
                "material_id": stock.material_id,
                "name": stock.name,
                "description": stock.description,
                "stock_level": stock.stock_level,
                "stock_price": stock.stock_price, 
                
                }) \
        .eq("stock_id", stock_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def get_stock_export_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("stock") \
            .select("stock_id, name, stock_price, stock_level") \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error
    
# Roles

def get_roles_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("role") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error

def get_role_sb(role_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("role") \
        .select("*") \
        .eq("role_id",role_id) \
        .execute() 
        return response.data          
    except Exception as error:
        log_error(error)
        return error
    
def create_role_sb(role:role):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("role") \
            .insert({
                "role_name": role.role_name,
                "description": role.description
            }) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

def update_role_sb(role_id:int, role:role):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("role") \
            .update({
                "role_name": role.role_name,
                "description": role.description
            }) \
            .eq("role_id", role_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error
    
def delete_role_sb(role_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("role") \
            .delete() \
            .eq("role_id", role_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error
    
# Role Claims

def get_role_claims_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("role_claim") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error

# Role Claim Lines

def get_role_claim_lines_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("role_claim_line") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def create_role_claim_line_sb(role_claim_line:role_claim_line):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("role_claim_line") \
        .insert({ 
                "role_claim_id": role_claim_line.role_claim_id,
                "role_id": role_claim_line.role_id,
                "view": role_claim_line.view,
                "create": role_claim_line.create,
                "update": role_claim_line.update,
                "delete": role_claim_line.delete
                     
                     
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error

def update_role_claim_line_sb(role_claim_id:int,role_id:int,role_claim_line:role_claim_line):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("role_claim_line") \
        .update({ 
                "role_claim_id": role_claim_line.role_claim_id,
                "role_id": role_claim_line.role_id,
                "view": role_claim_line.view,
                "create": role_claim_line.create,
                "update": role_claim_line.update,
                "delete": role_claim_line.delete
                        
                        
                }) \
        .eq("role_claim_id", role_claim_id) \
        .eq("role_id", role_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
    
# Quotes

def get_quotations_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("quotations_view") \
            .select("*") \
            .execute()        
        return response.data        
    except Exception as error:
        log_error(error)
        return error

def get_quotations_user_sb(user_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("quotations_view") \
        .select("*") \
        .eq("user_id",user_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error

def get_quotation_sb(quotation_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("quotations_view") \
        .select("*") \
        .eq("quotation_id",quotation_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error
 
def create_quotation_sb(quotation:quotation):
    try:
        db = get_supabase_client(True)
     
        response_update = db.schema(settings.SUPA_SCHEMA) \
        .table("job_request") \
        .update({ "job_request_status_id": 2}).eq("job_request_id", quotation.job_request_id) \
        .execute() 
        
        response_insert = db.schema(settings.SUPA_SCHEMA) \
        .table("quotations") \
        .insert({ 
                    "job_request_id": quotation.job_request_id,
                    # "deposit": quotation.deposit,
                    "total_cost": quotation.total_cost,
                    "quotation_status_id": 1,
                    "quotation_url": quotation.quotation_url,
                    "quotation_number": quotation.quotation_number                   
                }).execute() 
        
        return response_insert.data    
    
    except Exception as error:
        print(error)
        log_error(error)
        return error
    
def update_quotation_sb(quotation_id:int,quotation:quotation):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("quotations") \
        .update({ 
                "deposit": quotation.deposit,
                "total_cost": quotation.total_cost,
                "quotation_url": quotation.quotation_url,
                "quotation_number": quotation.quotation_number,       
                "quotation_status_id": quotation.quotation_status_id                            
                }) \
        .eq("quotation_id", quotation_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error  

def accept_quotation_sb(quotation_id:int):
    try:
        db = get_supabase_client(True)
        response_quote = db.schema(settings.SUPA_SCHEMA) \
        .table("quotations") \
        .update({ 
                "quotation_status_id": 2                                    
                }) \
        .eq("quotation_id", quotation_id) \
        .execute() 
        
        
        response_job = db.schema(settings.SUPA_SCHEMA) \
        .table("job_card") \
        .insert({ 
                "job_card_status_id": 5,
                "quotation_id": quotation_id
                }) \
        .execute() 
        
        

        return {"message": "Success"}   
    except Exception as error:
        log_error(error)
        return error  

def reject_quotation_sb(quotation_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("quotations") \
        .update({ 
                "quotation_status_id": 3                                    
                }) \
        .eq("quotation_id", quotation_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error  
    
def get_pending_quotes_sb():
    try:
        db = get_supabase_client(True)
        
        response = db.rpc('fn_get_pending_quotes').execute()
        
        return response.data
        
    except Exception as error:
        log_error(error)
        return {"error": str(error)}


# Invoices

def get_invoices_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("invoices_with_details") \
        .select("*") \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error
    
def get_invoices_user_sb(user_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("invoices_with_details") \
        .select("*") \
        .eq("user_id",user_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error

def get_invoice_by_quotation_sb(quotation_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("invoices") \
            .select("*") \
            .eq("quote_id", quotation_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return {"error": str(error)}

def get_invoice_by_job_card_sb(job_card_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
                     .table("invoices") \
                     .select("*") \
                     .eq("job_card_id", job_card_id) \
                     .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return []

def update_invoice_sb(invoice_id:int,invoice:invoice):
     try:
         db = get_supabase_client(True)
         response = db.schema(settings.SUPA_SCHEMA) \
         .table("invoices") \
         .update({ 
                 "job_card_id": invoice.job_card_id,
                 "total": invoice.total,
                 "invoice_status_id": invoice.invoice_status_id,
                 "invoice_url": invoice.invoice_url,
                 "invoice_number": invoice.invoice_number,  
                 "pop": invoice.pop  
                 }) \
         .eq("invoice_id", invoice_id) \
         .execute() 
         return response.data    
     except Exception as error:
         log_error(error)
         return error  
     
def update_invoice_status_sb(invoice_id: int):
    try:
        db = get_supabase_client(True)
        # Only pass parameters in a single dictionary
        response = db.rpc(
            "update_invoice_status",
            {'p_invoice_id': invoice_id}
        ).execute()
        
        return {"status": "success", "message": f"Invoice {invoice_id} status updated to 1"}
    except Exception as error:
        log_error(error)
        return {"status": "error", "message": str(error)}

def get_unpaid_invoices():
    try:
        db = get_supabase_client(True)
        
        # Call the PostgreSQL function
        response = db.rpc('fn_get_unpaid_invoices').execute()
        
        return response.data
        
    except Exception as error:
        log_error(error)
        return {"error": str(error)}
    
def create_invoice_sb(invoice: invoice):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("invoices") \
        .insert({ 
                "total": invoice.total,
                "invoice_url": invoice.invoice_url,
                "invoice_status_id": invoice.invoice_status_id,
                "invoice_number": invoice.invoice_number,
                "quote_id": invoice.quote_id 
                                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
# Add to supabase.py
def update_invoice_pop_sb(invoice_id: int, pop_url: str):
    """
    Update only the POP field of an invoice
    """
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("invoices") \
            .update({"pop": pop_url}) \
            .eq("invoice_id", invoice_id) \
            .execute()
            
        if response.data:
            return {"status": "success", "message": "POP updated"}
        return {"error": "No rows updated"}
    except Exception as error:
        log_error(f"Supabase POP update error: {error}")
        return {"error": str(error)}

# Quotation status

def get_quotation_statuses_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("quotation_status") \
        .select("*") \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error
    
def get_quotation_status_sb(quotation_status_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("quotation_status") \
        .select("*") \
        .eq("quotation_status_id",quotation_status_id) \
        .execute()    
        return response.data      
    except Exception as error:
        log_error(error)
        return error


# Job cards 

def get_job_cards_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_cards_with_details") \
            .select("*") \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

def get_job_card_sb(job_card_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_cards_with_details") \
            .select("*") \
            .eq("job_card_id", job_card_id) \
            .execute()
        return response.data[0] if response.data else None
    except Exception as error:
        log_error(error)
        return error

def update_invoice_job_card_sb(invoice_id: int, job_card_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("invoices") \
            .update({
                "job_card_id": job_card_id
            }) \
            .eq("invoice_id", invoice_id) \
            .execute()
        
        # Check if the update was successful
        if response.data:
            return response.data[0]  # Return the updated invoice
        else:
            return None
    except Exception as error:
        log_error(error)
        return error
    
def get_job_card_update_sb(job_card_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_cards_with_details_update") \
            .select("*") \
            .eq("job_card_id", job_card_id) \
            .execute()
        return response.data[0] if response.data else None
    except Exception as error:
        log_error(error)
        return error

def create_job_card_sb(job_card: JobCardCreate):
    try:
        db = get_supabase_client(True)
        
        # Prepare the main job card data with default status
        job_card_data = {
            "pattern_id": job_card.pattern_id,
            "job_card_status_id": 5,  # Default to Pending status
            "quotation_id": job_card.quotation_id,
            "special_instructions": job_card.special_instructions,
            # completed_at is intentionally left null
        }
        
        # Create main job card
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_card") \
            .insert(job_card_data) \
            .execute()
        
        if not response.data:
            return None
            
        new_job_card = response.data[0]
        job_card_id = new_job_card['job_card_id']
        
        # Insert materials into bridging table
        if job_card.materials:
            material_records = [{"job_card_id": job_card_id, "material_id": material_id} 
                               for material_id in job_card.materials]
            db.schema(settings.SUPA_SCHEMA) \
                .table("job_card_material") \
                .insert(material_records) \
                .execute()
        
        # Insert artisans into bridging table
        if job_card.artisans:
            artisan_records = [{"job_card_id": job_card_id, "employee_id": employee_id} 
                              for employee_id in job_card.artisans]
            db.schema(settings.SUPA_SCHEMA) \
                .table("job_card_artisan") \
                .insert(artisan_records) \
                .execute()
        
        return new_job_card
    except Exception as error:
        log_error(error)
        return error

    
def update_job_card_sb(job_card_id: int, update_data: dict):
    try:
        db = get_supabase_client(True)
        
        # Extract job card fields
        update_fields = {}
        if 'pattern_id' in update_data and update_data['pattern_id'] is not None:
            update_fields["pattern_id"] = update_data['pattern_id']
        if 'job_card_status_id' in update_data and update_data['job_card_status_id'] is not None:
            update_fields["job_card_status_id"] = update_data['job_card_status_id']
        if 'quotation_id' in update_data and update_data['quotation_id'] is not None:
            update_fields["quotation_id"] = update_data['quotation_id']
        if 'special_instructions' in update_data and update_data['special_instructions'] is not None:
            update_fields["special_instructions"] = update_data['special_instructions']
        if 'completed_at' in update_data and update_data['completed_at'] is not None:
            update_fields["completed_at"] = update_data['completed_at']
        
        # Extract materials and artisans
        materials = update_data.get('materials', []) or []
        artisans = update_data.get('artisans', []) or []
        
        # Only update job card if there are changes
        if update_fields:
            db.schema(settings.SUPA_SCHEMA) \
                .table("job_card") \
                .update(update_fields) \
                .eq("job_card_id", job_card_id) \
                .execute()
        
        # Update materials
        # Delete existing materials
        db.schema(settings.SUPA_SCHEMA) \
            .table("job_card_material") \
            .delete() \
            .eq("job_card_id", job_card_id) \
            .execute()
        
        # Insert new materials if any
        if materials:
            # Prepare batch insert
            material_records = [{"job_card_id": job_card_id, "material_id": mid} for mid in materials]
            db.schema(settings.SUPA_SCHEMA) \
                .table("job_card_material") \
                .insert(material_records) \
                .execute()
        
        # Update artisans
        # Delete existing artisans
        db.schema(settings.SUPA_SCHEMA) \
            .table("job_card_artisan") \
            .delete() \
            .eq("job_card_id", job_card_id) \
            .execute()
        
        # Insert new artisans if any
        if artisans:
            artisan_records = [{"job_card_id": job_card_id, "employee_id": eid} for eid in artisans]
            db.schema(settings.SUPA_SCHEMA) \
                .table("job_card_artisan") \
                .insert(artisan_records) \
                .execute()
        
        # Fetch updated record
        get_response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_cards_with_details") \
            .select("*") \
            .eq("job_card_id", job_card_id) \
            .execute()
        
        return get_response.data[0] if get_response.data else None
        
    except Exception as error:
        log_error(f"Update job card error: {str(error)}")
        return {"error": str(error)}
    
    
def get_completed_job_cards_sb():
    try:
        db = get_supabase_client(True)
        response = db.rpc(
            "get_completed_job_cards",
            {}
        ).execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error
    
def get_job_card_with_materials_sb(job_card_id: int):
    try:
        db = get_supabase_client(True)
        
        # Get job card details
        job_card_response = db.schema(settings.SUPA_SCHEMA) \
            .from_("job_card") \
            .select("*") \
            .eq("job_card_id", job_card_id) \
            .execute()
        
        if not job_card_response.data:
            return None
            
        job_card = job_card_response.data[0]
        
        # Get associated materials
        materials_response = db.schema(settings.SUPA_SCHEMA) \
            .from_("job_card_material") \
            .select("material: materials(material_id, material_name)") \
            .eq("job_card_id", job_card_id) \
            .execute()
            
        job_card["materials"] = [item["material"] for item in materials_response.data]
        return job_card
        
    except Exception as error:
        log_error(error)
        return error
 
def get_job_cards_employee_with_details_sb(employee_id: int):
    """Get job cards for employee with full details"""
    try:
        db = get_supabase_client(True)

        # First, get all job_card_ids where this employee is assigned
        artisan_response = (
            db.schema(settings.SUPA_SCHEMA)
            .from_("job_card_artisan")
            .select("job_card_id")
            .eq("employee_id", employee_id)
            .execute()
        )

        if not artisan_response.data:
            return []

        job_card_ids = [item["job_card_id"] for item in artisan_response.data]

        # Now get the full job card details for these IDs
        job_cards_response = (
            db.schema(settings.SUPA_SCHEMA)
            .from_("job_card")
            .select("*")
            .in_("job_card_id", job_card_ids)
            .execute()
        )

        if not job_cards_response.data:
            return []

        job_cards = []
        
        for job_card in job_cards_response.data:
            job_card_id = job_card["job_card_id"]
            
            # Get quotation details
            quotation_data = None
            if job_card.get("quotation_id"):
                quotation_response = (
                    db.schema(settings.SUPA_SCHEMA)
                    .from_("quotations")
                    .select("*")
                    .eq("quotation_id", job_card["quotation_id"])
                    .execute()
                )
                quotation_data = quotation_response.data[0] if quotation_response.data else None
                
                # Get job request details if quotation exists
                job_request_data = None
                if quotation_data and quotation_data.get("job_request_id"):
                    job_request_response = (
                        db.schema(settings.SUPA_SCHEMA)
                        .from_("job_request")
                        .select("*")
                        .eq("job_request_id", quotation_data["job_request_id"])
                        .execute()
                    )
                    job_request_data = job_request_response.data[0] if job_request_response.data else None
                    
                    # Add job request to quotation
                    if quotation_data:
                        quotation_data["job_request"] = job_request_data
            
            # Get materials for this job card
            materials_response = (
                db.schema(settings.SUPA_SCHEMA)
                .from_("job_card_material")
                .select("*, materials:material_id(*)")
                .eq("job_card_id", job_card_id)
                .execute()
            )
            
            # Get artisans for this job card
            artisans_response = (
                db.schema(settings.SUPA_SCHEMA)
                .from_("job_card_artisan")
                .select("*, employees:employee_id(*, users:user_id(*))")
                .eq("job_card_id", job_card_id)
                .execute()
            )
            
            # Build the complete job card object
            complete_job_card = {
                **job_card,
                "quotations": quotation_data,
                "job_card_materials": materials_response.data if materials_response.data else [],
                "job_card_artisans": artisans_response.data if artisans_response.data else []
            }
            
            job_cards.append(complete_job_card)

        return job_cards

    except Exception as error:
        log_error(f"Error in get_job_cards_employee_with_details_sb: {str(error)}")
        return {"error": str(error)}   

    
def get_job_cards_employee_sb(employee_id: int):
    try:
        db = get_supabase_client(True)

        # Get job_card_artisan entries for this employee
        artisan_entries = (
            db.schema(settings.SUPA_SCHEMA)
            .from_("job_card_artisan")
            .select("job_card_id")
            .eq("employee_id", employee_id)
            .execute()
        )

        job_card_ids = [item["job_card_id"] for item in artisan_entries.data] if artisan_entries.data else []

        if not job_card_ids:
            return []

        # Fetch job cards by IDs
        job_cards_response = (
            db.schema(settings.SUPA_SCHEMA)
            .from_("job_card")
            .select("*")
            .in_("job_card_id", job_card_ids)
            .execute()
        )

        return job_cards_response.data if job_cards_response.data else []

    except Exception as error:
        log_error(error)
        return {"error": str(error)}
    
def get_job_card_artisans_sb(job_card_id: int):
    """Return all artisans for a job card with full employee info"""
    try:
        db = get_supabase_client(True)
        # join job_card_artisan (bridging table) with employee table
        resp = (
            db.schema(settings.SUPA_SCHEMA)
              .table("job_card_artisan")
              .select("employee_id, created_at, job_card_artisan_id, employee(name, role, image)")
              .eq("job_card_id", job_card_id)
              .execute()
        )
        if resp.data:
            # flatten employee info
            artisans = []
            for row in resp.data:
                artisan = row.get("employee", {})
                artisan["employee_id"] = row.get("employee_id")
                artisan["job_card_artisan_id"] = row.get("job_card_artisan_id")
                artisans.append(artisan)
            return artisans
        return []
    except Exception as e:
        log_error(f"Error fetching job card artisans: {str(e)}")
        return []


def upload_progress_image_sb(job_card_id: int, file_content: bytes, filename: str, content_type: str = None):
    """
    Supabase helper function for uploading progress images
    Handles all database and storage operations
    Replaces existing progress_url if one exists
    """
    try:
        db = get_supabase_client(True)

        # 1. Get job card details
        job_card_response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_card") \
            .select("job_card_id, quotation_id") \
            .eq("job_card_id", job_card_id) \
            .execute()

        if not job_card_response.data:
            raise HTTPException(status_code=404, detail="Job card not found")

        job_card = job_card_response.data[0]
        quotation_id = job_card.get('quotation_id')
        
        if not quotation_id:
            raise HTTPException(status_code=404, detail="No quotation found for this job card")

        # 2. Get job_request_id from quotation
        quotation_response = db.schema(settings.SUPA_SCHEMA) \
            .table("quotations") \
            .select("job_request_id") \
            .eq("quotation_id", quotation_id) \
            .execute()
            
        if not quotation_response.data:
            raise HTTPException(status_code=404, detail="Quotation not found")
            
        job_request_id = quotation_response.data[0].get("job_request_id")
        
        if not job_request_id:
            raise HTTPException(status_code=404, detail="Job request not found for this quotation")

        # 3. Validate file type
        file_extension = os.path.splitext(filename)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )

        # 4. Generate unique filename
        unique_filename = f"progress_{job_card_id}_{uuid.uuid4()}{file_extension}"

        # 5. Upload to Supabase Storage with proper error handling
        try:
            storage_response = db.storage.from_("progress-images").upload(
                unique_filename,
                file_content,
                {"content-type": content_type or "image/jpeg"}
            )
            
            # Check if upload was successful
            if hasattr(storage_response, 'error') and storage_response.error:
                raise Exception(f"Storage upload error: {storage_response.error}")
                
        except Exception as storage_error:
            raise Exception(f"Failed to upload to storage: {str(storage_error)}")

        # 6. Get public URL
        public_url = db.storage.from_("progress-images").get_public_url(unique_filename)

        # 7. Update job_request.progress_url (REMOVED updated_at field)
        try:
            update_response = db.schema(settings.SUPA_SCHEMA) \
                .table("job_request") \
                .update({
                    "progress_url": public_url
                    # Removed: "updated_at": "now()" - this column might not exist
                }) \
                .eq("job_request_id", job_request_id) \
                .execute()

            # Check for database update errors
            if hasattr(update_response, 'error') and update_response.error:
                raise Exception(f"Database update error: {update_response.error}")
                
        except Exception as db_error:
            # Try to delete the uploaded file if database update fails
            try:
                db.storage.from_("progress-images").remove([unique_filename])
            except:
                pass  # Ignore errors during cleanup
            raise Exception(f"Failed to update database: {str(db_error)}")

        return {
            "progress_url": public_url,
            "job_card_id": job_card_id,
            "job_request_id": job_request_id,
            "filename": unique_filename,
            "message": "Progress image uploaded successfully"
        }

    except HTTPException:
        raise
    except Exception as error:
        log_error(f"Supabase upload progress image error: {str(error)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload progress image: {str(error)}")
    
def update_invoice_job_card_sb(invoice_id, job_card_id):
    try:
        db = get_supabase_client(True)
        
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("invoices") \
            .update({"job_card_id": job_card_id}) \
            .eq("invoice_id", invoice_id) \
            .execute()
        
        if not response.data:
            return None
            
        return response.data[0]
    except Exception as error:
        log_error(error)
        return error
    
# Job Card Status Functions
def get_job_card_statuses_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_card_status") \
            .select("*") \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error

def get_job_card_status_sb(job_card_status_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("job_card_status") \
            .select("*") \
            .eq("job_card_status_id", job_card_status_id) \
            .execute()
        return response.data[0] if response.data else None
    except Exception as error:
        log_error(error)
        return error
    
# Users

def get_users_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("users_with_details") \
        .select("*") \
        .execute()          
        return response.data
    except Exception as error:
        log_error(error)
        return error
    
def get_user_sb(user_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("user") \
        .select("*") \
        .eq("user_id",user_id) \
        .execute()   
        return response.data       
    except Exception as error:
        log_error(error)
        return error
 
def get_user_employee_sb(user_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee") \
        .select("*,user:user_id(*)") \
        .eq("user_id",user_id) \
        .execute()   
        return response.data       
    except Exception as error:
        log_error(error)
        return error
 
def get_user_customer_sb(user_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("customers") \
        .select("*,user:user_id(*)") \
        .eq("user_id",user_id) \
        .execute()        
        return response.data  
    except Exception as error:
        log_error(error)
        return error
   
def create_user_sb(user:user):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("user") \
        .insert({ 
                "name": user.name,
                "surname": user.surname,
                "email_address": user.email_address,
                "phone_number": user.phone_number,
                "role_id": user.role_id,
                "title_id": user.title_id,
                "image": user.image,
                "uuid": user.uuid,
                "is_employee": user.is_employee
                

                     
                     
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def update_user_sb(user_id: int, user: UserUpdate):
    try:
        # Create update dictionary with only provided fields
        update_data = {}
        if user.email_address is not None:
            update_data["email_address"] = user.email_address
        if user.phone_number is not None:
            update_data["phone_number"] = user.phone_number
        if user.name is not None:
            update_data["name"] = user.name
        if user.surname is not None:
            update_data["surname"] = user.surname
        if user.image is not None:
            # Handle image deletion when empty string or null is passed
            update_data["image"] = user.image if user.image != "" else None
        
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("user") \
            .update(update_data) \
            .eq("user_id", user_id) \
            .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
    
     
# Employee_Type

def get_types_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("type") \
        .select("*") \
        .execute()    
        return response.data       
    except Exception as error:
        log_error(error)
        return error

def get_type_sb(type_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("type") \
        .select("*") \
        .eq("type_id",type_id) \
        .execute()  
        return response.data         
    except Exception as error:
        log_error(error)
        return error
    
def create_type_sb(type:type):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("type") \
        .insert({ 
                "type_name": type.type_name
                     
                     
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def update_type_sb(type_id:int,type:type):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("type") \
        .update({ 
                "type_name": type.type_name
                        
                        
                }) \
        .eq("type_id", type_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error 
    
    
# Employee

def get_employees_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("users_with_details") \
        .select("*") \
        .execute()          
        return response.data 
    except Exception as error:
        log_error(error)
        return error
    
def get_employee_sb(employee_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee") \
        .select("*") \
        .eq("employee_id",employee_id) \
        .execute()   
        return response.data        
    except Exception as error:
        log_error(error)
        return error
    
def get_employee_by_phone_sb(phone: str):
    try:
        # Convert to digits-only format and ensure proper prefix
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Handle South African numbers starting with 0
        if clean_phone.startswith('0') and len(clean_phone) == 10:
            clean_phone = '27' + clean_phone[1:]
        elif clean_phone.startswith('27') and len(clean_phone) == 11:
            # Already in correct format
            pass
        else:
            # Handle other formats
            clean_phone = clean_phone.lstrip('+')
            if not clean_phone.startswith('27') and len(clean_phone) == 9:
                clean_phone = '27' + clean_phone
        
        db = get_supabase_client(True)
        
        # Query to get employee by phone number
        response = db.schema(settings.SUPA_SCHEMA) \
            .from_("user") \
            .select("employee(employee_id, user_id)") \
            .eq("phone_number", clean_phone) \
            .execute()
        
        # Check if we got results
        if response.data and len(response.data) > 0:
            user_data = response.data[0]
            if user_data.get("employee") and len(user_data["employee"]) > 0:
                return user_data["employee"][0]  # Return first employee record
        return None
        
    except Exception as error:
        log_error(f"Error in get_employee_by_phone_sb: {str(error)}")
        return None
    
def create_employee_sb(employee:employee):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee") \
        .insert({ 
                "job_scope": employee.job_scope,
                "address": employee.address,
                "user_id": employee.user_id,
                "emergency_contact": employee.emergency_contact,
                "hourly_rate": employee.hourly_rate              
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def get_employee_info_sb(employee_id: int):

    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee") \
            .select("*") \
            .eq("employee_id", employee_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return {"error": str(error)}
    
def get_employee_by_user_id_sb(user_id: int):

    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return {"error": str(error)}

def get_user_by_phone_sb(phone: str):

    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("user") \
            .select("*") \
            .eq("phone_number", phone) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return {"error": str(error)}

def update_employee_sb(employee_id: int, employee_data: dict):

    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee") \
            .update({
                "emergency_contact": employee_data.get("emergency_contact"),
                "address": employee_data.get("address")
            }) \
            .eq("employee_id", employee_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return {"error": str(error)}
    
def get_user_sb(user_id: int):

    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("user") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return {"error": str(error)}
    
def get_time_logs_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_time_log") \
        .select("*,employee:employee_id(*,user:user_id(*))") \
        .execute()          
        return response.data 
    except Exception as error:
        log_error(error)
        return error     
    
def create_clock_code_sb(code: int, type: str, expires_at: datetime):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee_clock_codes") \
            .insert({ 
                "code": code,
                "type": type,
                "expires_at": expires_at.isoformat() + "Z" 
            }) \
            .execute()
        
        return response.data[0] if response.data else None
    except Exception as error:
        log_error(f"create_clock_code_sb error: {error}")
        raise error

def verify_clock_code_sb(code: int, type: str):
    try:
        db = get_supabase_client(True)
        current_time = datetime.utcnow().isoformat() + "Z"
        
        # Check for valid code
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee_clock_codes") \
            .select("*") \
            .eq("code", code) \
            .eq("type", type) \
            .gt("expires_at", current_time) \
            .execute()
        
        if not response.data or len(response.data) == 0:
            return {
                "valid": False,
                "message": "Invalid or expired code"
            }
        
        return {"valid": True, "message": "Code verified"}
    
    except Exception as error:
        return {
            "valid": False,
            "message": f"Verification error: {str(error)}"
        }

def clock_in_sb(employee_id: int, clock_in_time: str):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee_time_log") \
            .insert({
                "employee_id": employee_id,
                "clock_in": clock_in_time
            }) \
            .execute()
        return response.data[0] if response.data else None
    except Exception as error:
        log_error(f"clock_in_sb error: {error}")
        raise error

def clock_out_sb(employee_id: int, clock_out_time: str):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee_time_log") \
            .select("employee_time_log_id") \
            .eq("employee_id", employee_id) \
            .is_("clock_out", "null") \
            .order("clock_in", desc=True) \
            .limit(1) \
            .execute()
        
        if not response.data or len(response.data) == 0:
            raise ValueError("No active clock-in found")
        
        log_id = response.data[0]['employee_time_log_id']
        
        update_response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee_time_log") \
            .update({"clock_out": clock_out_time}) \
            .eq("employee_time_log_id", log_id) \
            .execute()
        
        return update_response.data[0] if update_response.data else None
    except Exception as error:
        log_error(f"clock_out_sb error: {error}")
        raise error

def invalidate_previous_codes(employee_id: int, type: str):
    try:
        db = get_supabase_client(True)
        db.schema(settings.SUPA_SCHEMA) \
            .table("employee_clock_codes") \
            .update({"used": True}) \
            .eq("employee_id", employee_id) \
            .eq("type", type) \
            .eq("used", False) \
            .execute()
    except Exception as error:
        log_error(f"invalidate_previous_codes error: {error}")
        raise error


def get_employee_time_logs_by_id_sb(employee_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema("development") \
            .table("employee_time_log") \
            .select("*") \
            .eq("employee_id", employee_id) \
            .order("clock_in", desc=True) \
            .execute()
        
        return response.data
    except Exception as error:
        print(f"Error fetching employee logs: {str(error)}")
        return {"error": str(error)}
# def clock_in_sb(employee:employee):
#     try:
#         db = get_supabase_client(True)
#         response = db.schema(settings.SUPA_SCHEMA) \
#         .table("employee") \
#         .insert({ 
#                 "job_scope": employee.job_scope,
#                 "address": employee.address,
#                 "user_id": employee.user_id,
#                 "emergency_contact": employee.emergency_contact,
#                 "hourly_rate": employee.hourly_rate              
#                 }) \
#         .execute() 
#         return response.data    
#     except Exception as error:
#         log_error(error)
#         return error   

# def clock_out_sb(employee:employee):
#     try:
#         db = get_supabase_client(True)
#         response = db.schema(settings.SUPA_SCHEMA) \
#         .table("employee") \
#         .insert({ 
#                 "job_scope": employee.job_scope,
#                 "address": employee.address,
#                 "user_id": employee.user_id,
#                 "emergency_contact": employee.emergency_contact,
#                 "hourly_rate": employee.hourly_rate              
#                 }) \
#         .execute() 
#         return response.data    
#     except Exception as error:
#         log_error(error)
#         return error   
    
def get_artisans_sb():
    try:
        db = get_supabase_client(True)
        
        # Fetch all employees with their user details
        response = db.schema(settings.SUPA_SCHEMA) \
            .from_("employee") \
            .select("employee_id, user:user_id!inner(name, surname, role_id)") \
            .execute()
        
        # Filter artisans locally (role_id = 5)
        artisans = []
        for item in response.data:
            user = item.get("user", {})
            if user.get("role_id") == 5:  # Artisan role
                artisans.append({
                    "employee_id": item["employee_id"],
                    "name": user.get("name", ""),
                    "surname": user.get("surname", ""),
                    "role_id": user.get("role_id")
                })
                
        return artisans
    except Exception as error:
        log_error(error)
        return error
   
     
# Employee_pay_slip

def get_pay_slips_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_pay_slip") \
        .select("*") \
        .execute()  
        return response.data         
    except Exception as error:
        log_error(error)
        return error
    
def get_pay_slip_sb(employee_pay_slip_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_pay_slip") \
        .select("*") \
        .eq("employee_pay_slip_id",employee_pay_slip_id) \
        .execute() 
        return response.data          
    except Exception as error:
        log_error(error)
        return error
    
def create_pay_slip_sb(employee_pay_slip:employee_pay_slip):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_pay_slip") \
        .insert({ 
                "salary": employee_pay_slip.salary,
                "employee_id": employee_pay_slip.employee_id,
                "payslip_url": employee_pay_slip.payslip_url

                     
                     
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def update_pay_slip_sb(employee_pay_slip_id:int,employee_pay_slip:employee_pay_slip):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_pay_slip") \
        .update({ 
                "salary": employee_pay_slip.salary,
                "employee_id": employee_pay_slip.employee_id
                        
                        
                }) \
        .eq("employee_pay_slip_id", employee_pay_slip_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
    
    
# Employee_warning

def get_employee_warnings_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_warning") \
        .select("*") \
        .execute() 
        return response.data          
    except Exception as error:
        log_error(error)
        return error
    
def get_employee_warning_sb(employee_warning_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_warning") \
        .select("*") \
        .eq("employee_warning_id",employee_warning_id) \
        .execute()          
        return response.data 
    except Exception as error:
        log_error(error)
        return error
    
def create_employee_warning_sb(employee_warning:employee_warning):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_warning") \
        .insert({ 
                "reason": employee_warning.reason,
                "employee_warning_type_id": employee_warning.employee_warning_type_id,
                "employee_id": employee_warning.employee_id,
                "is_disputed": employee_warning.is_disputed

                     
                     
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def update_employee_warning_sb(employee_warning_id:int,employee_warning:employee_warning):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_warning") \
        .update({ 
                "reason": employee_warning.reason,
                "employee_warning_type_id": employee_warning.employee_warning_type_id,
                "employee_id": employee_warning.employee_id,
                "is_disputed": employee_warning.is_disputed
                        
                        
                }) \
        .eq("employee_warning_id", employee_warning_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def delete_employee_warning_sb(employee_warning_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("employee_warning") \
            .delete() \
            .eq("employee_warning_id", employee_warning_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error
    
# receipt

def get_receipts_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("receipts") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error

def get_receipt_sb(receipt_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("receipts") \
        .select("*") \
        .eq("receipt_id",receipt_id) \
        .execute()          
    except Exception as error:
        log_error(error)
        return error
    
def create_receipt_sb(receipt:receipt):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("receipts") \
        .insert({ 
                "receipt_id": receipt.receipt_id,
                "quotation_id": receipt.quotation_id,
                'amount_paid': receipt.amount_paid

                }) \
        .execute() 
        return response.data
    except Exception as error:
        log_error(error)
        return error 
    
def update_receipt_sb(receipt_id:int,receipt:receipt):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("receipts") \
        .update({ 
                "receipt_name": receipt.receipt_name
                        
                        
                }) \
        .eq("receipt_id", receipt_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
             
            
# Customer
def get_customers_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("customers_with_details") \
        .select("*") \
        .execute()   
        return response.data        
    except Exception as error:
        log_error(error)
        return error
                 
def get_customer_sb(customer_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("customers") \
        .select("*") \
        .eq("customer_id",customer_id) \
        .execute()          
        return response.data 
    except Exception as error:
        log_error(error)
        return error

def create_customer_sb(customer:customer):
    try:
        db = get_supabase_client(True)
        
        auth_payload = {
            "email":customer.email_address,
            "phone":customer.phone_number,
            "email_confirm": True,
            "phone_confirm": True,
        }
        auth_user = db.auth.admin.create_user(auth_payload)
        
        print(auth_user)
        print('*****************')
    
        user_data = { 
            "role_id":6,
            "title_id": customer.title_id,
            "name": customer.name,
            "surname": customer.surname,
            "email_address": customer.email_address,
            "phone_number": customer.phone_number,
            "uuid": auth_user.user.id,
            "is_employee":False
        } 
        response_user = db.schema(settings.SUPA_SCHEMA).table("user").insert(user_data).execute()
        
        print(response_user.data)
        print('*****************')
        
        customer_data = { 
            "user_id": response_user.data[0]["user_id"],  
            "address": customer.address,
            "company_name": customer.company_name, 
            "registration_number": customer.registration_number, 
            "vat_number": customer.vat_number,  
            "telephone": customer.telephone,   
        }
        response_customer = db.schema(settings.SUPA_SCHEMA).table("customers").insert(customer_data).execute()
        
        print(response_customer)
        print('*****************') 
        
        
        if len(response_user.data) > 0 and len (response_customer.data) > 0:  
            return {"message": "Customer created and OTP auth enabled", "auth_user_id": auth_user.user.id}
        else:
            return {"error": "Failed to Create Account, Please contact Admin"}
    
    except Exception as error:
        log_error(error)
        print(error)
        return {"error": error} 
                     
def update_customer_sb(customer_id:int,customer:updateCustomer):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("customers") \
        .update({ 
                "user_id": customer.user_id,
                "address": customer.address,
                "company_name": customer.company_name,
                "registration_number": customer.registration_number,
                "telephone": customer.telephone,
                "vat_number": customer.vat_number
                        
                        
                }) \
        .eq("customer_id", customer_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
       
def get_customer_types_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("customer_types") \
        .select("*") \
        .execute()   
        return response.data        
    except Exception as error:
        log_error(error)
        return error
                
                  
# Job_request


def get_job_requests_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("job_requests_with_items") \
        .select("*") \
        .execute()   
        return response.data        
    except Exception as error:
        log_error(error)
        return error
    
def get_job_requests_user_sb(user:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("job_requests_with_items") \
        .select("*") \
        .eq("user_id",user) \
        .execute()   
        return response.data        
    except Exception as error:
        log_error(error)
        return error
               
def get_job_request_sb(job_request_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("job_request") \
        .select("*") \
        .eq("job_request_id",job_request_id) \
        .execute()          
        return response.data 
    except Exception as error:
        log_error(error)
        return error

def create_job_request_sb(job_request:job_request_insert):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("job_request") \
        .insert({ 
                "customer_id": job_request.customer_id,
                "finish_date": job_request.finish_date,
                "description": job_request.description,
                "job_request_status_id": 1,
                "title": job_request.title,
                "quantity": job_request.quantity  
                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
                     
def update_job_request_sb(job_request_id:int,job_request:job_request):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("job_request") \
        .update({ 
                "customer_id": job_request.customer_id,
                "design": job_request.design,
                "finish_date": job_request.finish_date,
                "status": job_request.status               
                }) \
        .eq("job_request_id", job_request_id) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def reject_job_request_sb(job_request_id:int):
    try:
        db = get_supabase_client(True)
        response =  db.schema(settings.SUPA_SCHEMA) \
        .from_("job_request") \
        .update({ "job_request_status_id": 3}) \
        .eq("job_request_id", job_request_id) \
        .execute() 
        return response.data    
    except Exception as error: 
        print(error) 
        # log_error(error)
        return error
    

def cancel_job_request_sb(job_request_id: int):
    try:
        db = get_supabase_client(True)
        # Execute the update
        update_response = db.schema(settings.SUPA_SCHEMA) \
            .from_("job_request") \
            .update({"job_request_status_id": 4}) \
            .eq("job_request_id", job_request_id) \
            .execute()
        
        # Verify update was successful - use the actual response attributes
        if hasattr(update_response, 'error') and update_response.error:
            return {"error": f"Supabase error: {update_response.error.message}"}
        
        # Fetch and return the updated record
        get_response = db.schema(settings.SUPA_SCHEMA) \
            .from_("job_request") \
            .select("*") \
            .eq("job_request_id", job_request_id) \
            .execute()
            
        if hasattr(get_response, 'data') and get_response.data:
            return get_response.data[0]
        
        return {"error": "Failed to fetch updated job request"}
    except Exception as error: 
        print(f"Error in cancel_job_request_sb: {str(error)}")
        return {"error": str(error)}
    
# Patterns 

def get_patterns_sb():   
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("patterns") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def get_pattern_sb(pattern_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("patterns") \
        .select("*") \
        .eq("pattern_id",pattern_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error
    
def get_pattern_types_sb():   
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("pattern_type") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def get_pattern_type_sb(pattern_type_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("pattern_type") \
        .select("*") \
        .eq("pattern_type_id",pattern_type_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error

def create_pattern_sb(pattern:pattern):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("patterns") \
        .insert({ 
                "pattern_type_id": pattern.pattern_type_id,
                "design": pattern.design
                                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def delete_pattern_sb(pattern_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("patterns") \
            .delete() \
            .eq("pattern_id", pattern_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error
    
# Materials

def get_materials_sb():   
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("materials") \
        .select("*") \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def get_material_sb(material_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("materials") \
        .select("*") \
        .eq("material_id",material_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error
    
def get_materials_export_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("materials") \
            .select("material_name") \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error
    
def import_materials_sb(materials: list):
    try:
        db = get_supabase_client(True)
        inserted_count = 0
        duplicate_count = 0
        
        for name in materials:
            try:
                # Check if  exists
                exists = db.schema(settings.SUPA_SCHEMA).table("materials") \
                    .select("material_name") \
                    .eq("material_name", name) \
                    .execute()
                
                if exists.data:
                    duplicate_count += 1
                    continue
                
                response = db.schema(settings.SUPA_SCHEMA).table("materials") \
                    .insert({"material_name": name}) \
                    .execute()
                
                if response.data:
                    inserted_count += 1
                else:
                    duplicate_count += 1
                    
            except Exception as e:
                log_error(f"Error inserting material '{name}': {str(e)}")
                duplicate_count += 1
        
        return {
            "inserted_count": inserted_count,
            "duplicate_count": duplicate_count
        }
    except Exception as error:
        log_error(f"Material import error: {error}")
        return Exception(f"Supabase import failed: {str(error)}")

# Delivery Notes

def get_delivery_notes_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("delivery_notes_with_details") \
        .select("*") \
        .execute() 
        return response.data         
    except Exception as error:
        log_error(error)
        return error
    
def get_delivery_notes_user_sb(user:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("delivery_notes_with_details") \
        .select("*") \
        .eq("user_id",user) \
        .execute()   
        return response.data        
    except Exception as error:
        log_error(error)
        return error

def get_delivery_note_sb(delivery_note_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("delivery_note") \
        .select("*") \
        .eq("delivery_note_id",delivery_note_id) \
        .execute()   
        return response.data       
    except Exception as error:
        log_error(error)
        return error

    
def create_delivery_note_sb(delivery_note:delivery_note):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("delivery_note") \
        .insert({ 
                "delivery_note_url": delivery_note.delivery_note_url,
                "job_card_id": delivery_note.job_card_id   
                                }) \
        .execute() 
        return response.data    
    except Exception as error:
        log_error(error)
        return error
    
def delete_delivery_note_sb(delivery_note_id: int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
            .table("delivery_note") \
            .delete() \
            .eq("delivery_note_id", delivery_note_id) \
            .execute()
        return response.data
    except Exception as error:
        log_error(error)
        return error
    


# General
def get_faqs_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("faq") \
        .select("*") \
        .execute() 
        return response.data         
    except Exception as error:
        log_error(error)
        return error



def get_admin_stats_sb():
    try:
        db = get_supabase_client(True)

        # --- Job Requests (status_id = 1 = new/pending) ---
        response_job_requests = (
            db.schema(settings.SUPA_SCHEMA)
              .table("job_request")
              .select("job_request_id")
              .eq("job_request_status_id", 1)
              .execute()
        )
        new_requests = len(response_job_requests.data)

        today = datetime.utcnow()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        start_str = start_of_week.strftime('%Y-%m-%d')
        end_str = end_of_week.strftime('%Y-%m-%d')

        response_job_cards = (
            db.schema(settings.SUPA_SCHEMA)
            .table("job_card")
            .select("job_card_id, completed_at")
            .eq("job_card_status_id", 2)  
            .gte("completed_at", start_str)
            .lt("completed_at", end_str)
            .execute()
        )
        completed_job_cards_week = len(response_job_cards.data)

        # --- Total Customers ---
        response_total_customers = (
            db.schema(settings.SUPA_SCHEMA)
              .table("customers")
              .select("customer_id")
              .execute()
        )
        total_customers = len(response_total_customers.data)

        # --- Employees Clocked In Today ---
        today_date = datetime.utcnow().date()
        tomorrow_date = today_date + timedelta(days=1)
        today_str = today_date.isoformat()
        tomorrow_str = tomorrow_date.isoformat()

        response_employees = (
            db.schema(settings.SUPA_SCHEMA)
              .table("employee_time_log")
              .select("employee_time_log_id")
              .gte("clock_in", today_str)
              .lt("clock_in", tomorrow_str)
              .execute()
        )
        employees_clocked_in_today = len(response_employees.data)

        # --- Pending Quotations (status_id = 1 = pending) ---
        response_pending_quotes = (
            db.schema(settings.SUPA_SCHEMA)
              .table("quotations")
              .select("quotation_id")
              .eq("quotation_status_id", 1)
              .execute()
        )
        pending_quotations = len(response_pending_quotes.data)

        # --- Unpaid Invoices (status_id = 2 = unpaid) ---
        response_unpaid_invoices = (
            db.schema(settings.SUPA_SCHEMA)
              .table("invoices")
              .select("invoice_id")
              .eq("invoice_status_id", 2)
              .execute()
        )
        unpaid_invoices = len(response_unpaid_invoices.data)

        # --- Low Stock Items (stock_level < 10) ---
        response_low_stock = (
            db.schema(settings.SUPA_SCHEMA)
              .table("stock")
              .select("stock_id, stock_level")
              .lt("stock_level", 10)
              .execute()
        )
        low_stock_items = len(response_low_stock.data)
        
        response_pending_job_cards = (
            db.schema(settings.SUPA_SCHEMA)
              .table("job_card")
              .select("job_card_id")
              .eq("job_card_status_id", 5)
              .execute()
        )
        pending_job_cards = len(response_pending_job_cards.data)

        # --- Final Response ---
        resp = {
            "new_requests": new_requests,
            "completed_job_cards_week": completed_job_cards_week,
            "total_customers": total_customers,
            "employees_clocked_in_today": employees_clocked_in_today,
            "pending_quotations": pending_quotations,
            "unpaid_invoices": unpaid_invoices,
            "low_stock_items": low_stock_items,
            "pending_job_cards": pending_job_cards

        }

        return resp

    except Exception as error:
        log_error(error)
        return {"error": str(error)}


       
def get_artisan_stats_sb(user_id: int):
    try:
        db = get_supabase_client(True)

        # get employee
        response_employee = db.schema(settings.SUPA_SCHEMA).table("employee").select("employee_id").eq("user_id",user_id).execute() 
        employee_id = response_employee["data"][0]["employee_id"]
        print(employee_id)
        
           
        # Jobs cards
        response_job_cards = db.schema(settings.SUPA_SCHEMA).table("job_card_artisan").select("*").eq("employee_id",employee_id).execute() 
        # ,job_card_id(*)
        print(response_job_cards["data"])

        
        jobs_completed = len(response_job_cards.data)
        
        
        #Completed Job Cards
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=7)          # next Monday (exclusive)
        start_str = start_of_week.strftime('%Y-%m-%d')
        end_str = end_of_week.strftime('%Y-%m-%d')
        response_job_cards = db.schema(settings.SUPA_SCHEMA).table("job_card").select("*").eq("job_card_status_id", 3).gte("completed_at", start_str).lt("completed_at", end_str).execute()
        completed_job_cards_week = len(response_job_cards.data)

        
       # Customers
        response_total_customers = db.schema(settings.SUPA_SCHEMA).table("customers").select("*").execute() 
        total_customers = len(response_total_customers.data)
        
        
        #Employees
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        today_str = today.isoformat()         # '2025-05-23'
        tomorrow_str = tomorrow.isoformat()   # '2025-05-24' 
        response_employees= db.schema(settings.SUPA_SCHEMA).table("employee_time_log").select("*").gte("clock_in", today_str).lt("clock_in", tomorrow_str).execute()
        employees_clocked_in_today = len(response_employees.data)


        resp = {
            "jobs_completed":jobs_completed,
            # "hours_worked":completed_job_cards_week,
            # "accumulated_pay":total_customers,
        }
        
        
        return resp        
    except Exception as error:
        log_error(error)
        return error    
    
    

    
    #Time logs
  
def get_employee_time_logs_sb():
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_time_log") \
        .select("*") \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error


def get_employee_time_log_sb(employee_time_log_id:int):
    try:
        db = get_supabase_client(True)
        response = db.schema(settings.SUPA_SCHEMA) \
        .table("employee_time_log") \
        .select("*") \
        .eq("employee_time_log_id",employee_time_log_id) \
        .execute()  
        return response.data        
    except Exception as error:
        log_error(error)
        return error


def get_monthly_hours_worked(year: int):
    try:
        db = get_supabase_client(True)
        
        # Call the PostgreSQL function we created
        response = db.rpc('fn_monthly_hours_worked_year', {
            'p_year': year
        }).execute()
        
        return response.data
        
    except Exception as error:
        log_error(error)
        return {"error": str(error)}



# Timer