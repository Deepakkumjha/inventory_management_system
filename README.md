# Inventory Management System (Django + DRF)

A simple Inventory Management System built using Django and Django REST Framework (DRF). This project provides REST APIs for managing inventory items and supports exporting data to PDF and Excel formats.

### FEATURES
- Create, Read, Update, Delete (CRUD) inventory items
- RESTfull APIs using Django REST Framework
- PDF report generation of all items
- Excel export of inventory data
- SQLite database
- Clean and readable code structure

## TECH STACK
### Backend:
Django, Django REST Framework
### Database:
SQLite
### PDF Generation:
ReportLab
### Excel Export: 
openpyxl
### Python Version:
3.10+

## SETUP INSTRUCTIONS
#### 1. Clone the repository - 

git clone https://github.com/Deepakkumjha/inventory_management_system.git

cd inventory_management_system

#### 2. Create and activate virtual environment - 

python -m venv venv

source venv/bin/activate   (macOS / Linux)

venv\Scripts\activate      (Windows)

#### 3. Install dependencies -

pip install -r requirements.txt

#### 4. Apply database migrations

python manage.py makemigrations

python manage.py migrate

#### 5. Run the development server

python manage.py runserver

#### Server URL - http://127.0.0.1:8000/

## API ENDPOINTS

### Create Item

POST -  /api/items/

Request Body:

{
  "name": "Laptop",
  "description": "Dell Inspiron",
  "quantity": 10,
  "price": 55000.00
}

### Get All Items
GET -  /api/items/

### Get Single Item
GET /api/items/{id}/

### Update Item
PUT /api/items/{id}/

Request Body:

{
  "name": "Laptop",
  "description": "Dell Inspiron",
  "quantity": 10,
  "price": 55000.00
}

PATCH /api/items/{id}/

Request Body:
{
  "quantity": 15
}

### Delete Item
DELETE - /api/items/{id}/

## PDF EXPORT
GET -  /api/items/export/pdf/

Downloads file: items_report.pdf

Includes fields: id, name, quantity, price, created_at

## EXCEL EXPORT
GET - /api/items/export/excel/

Downloads file: items_report.xlsx

Includes fields: id, name, quantity, price, created_at

## API TESTING
APIs can be tested using Postman, cURL, or browser for GET requests.
Example:
curl http://127.0.0.1:8000/api/items/

NOTES
- SQLite is used for simplicity.
- Virtual environment, IDE files, and database files should not be committed.
- Filtering and pagination can be added as future improvements.


### CONCLUSION
This project fulfills the requirements of the Django Developer Practical Test, including CRUD APIs, PDF generation, and Excel export using Django REST Framework.
