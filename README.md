# Final-Year-Project
A stock, HR, quotation, invoice, delivery and job management system built with Angular, FastAPI and Supabase.

## 1 Set Up virtual environment

*************************

 - open terminal in (vault-vision-api) directory 
 - create venv : python -m venv venv
 - activate venv : venv\Scripts\activate.bat
 - install reqs : pip install -r requirements.txt

 *************************

## 2 Running the API

*************************

- open terminal in (vault-vision-api) directory 

- run this : venv\Scripts\activate.bat&&set FASTAPI_ENV=dev&&python -m uvicorn api.main:app --reload

*************************

## 3 API DOCS

For swaggerUI, goto: http://127.0.0.1:8000/docs

<!-- pip install pandas xlsxwriter -->
<!-- pip install pandas openpyxl python-docx -->

<!-- pip install pytest pytest-asyncio httpx pytest-mock -->

## 4 Unit Testing

- run these command for testing : 
python -m pytest api/tests/test_employees.py -v
python -m pytest api/tests/test_customers.py -v
python -m pytest api/tests/test_invoices.py -v
python -m pytest api/tests/test_roles.py -v
python -m pytest api/tests/test_users.py -v

