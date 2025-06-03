from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Product Pricing Calculator", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Product Calculation Models
class ProductCalculationRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100, description="Name of the product")
    quantity: float = Field(..., gt=0, description="Quantity of the product")
    unit_price_before_tax: float = Field(..., ge=0, description="Unit price before tax")
    gst_percentage: float = Field(..., ge=0, le=100, description="GST percentage (0-100)")
    sales_price_mrp_per_unit: float = Field(..., gt=0, description="Sales price/MRP per unit")

    @validator('gst_percentage')
    def validate_gst_percentage(cls, v):
        # Common GST rates in India, but allow custom rates too
        return v

class ProductCalculationResult(BaseModel):
    # Input data
    product_name: str
    quantity: float
    unit_price_before_tax: float
    gst_percentage: float
    sales_price_mrp_per_unit: float
    
    # Calculated values
    subtotal_before_tax: float
    tax_name: str
    tax_rate_decimal: float
    unit_price_after_tax: float
    subtotal_after_tax: float
    effective_rate_per_unit: float
    margin_percentage: float
    markup_percentage: float
    
    # Metadata
    calculation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BulkCalculationRequest(BaseModel):
    products: List[ProductCalculationRequest]

class BulkCalculationResult(BaseModel):
    calculations: List[ProductCalculationResult]
    total_products: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CalculationHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    calculation_result: ProductCalculationResult
    saved_at: datetime = Field(default_factory=datetime.utcnow)


# Calculation Functions (converted from the provided Python code)
def calculate_subtotal_before_tax(quantity: float, unit_price_before_tax: float) -> float:
    """Calculates the subtotal before any taxes are applied."""
    return quantity * unit_price_before_tax

def calculate_product_unit_price_after_tax(unit_price_before_tax: float, tax_rate_decimal: float) -> float:
    """Calculates the unit price after applying tax."""
    return unit_price_before_tax * (1 + tax_rate_decimal)

def calculate_subtotal_after_tax(quantity: float, unit_price_after_tax: float) -> float:
    """Calculates the subtotal after tax has been applied."""
    return quantity * unit_price_after_tax

def calculate_margin_percentage(sales_price_mrp_per_unit: float, product_unit_price_after_tax: float) -> float:
    """Calculates the profit margin percentage based on the sales price."""
    if sales_price_mrp_per_unit == 0:  # Avoid division by zero
        return 0
    profit_per_unit = sales_price_mrp_per_unit - product_unit_price_after_tax
    margin = (profit_per_unit / sales_price_mrp_per_unit) * 100
    return round(margin, 2)

def calculate_markup_percentage(sales_price_mrp_per_unit: float, product_unit_price_after_tax: float) -> float:
    """Calculates the markup percentage based on the cost (unit price after tax)."""
    if product_unit_price_after_tax == 0:  # Avoid division by zero
        return float('inf') if sales_price_mrp_per_unit > 0 else 0
    profit_per_unit = sales_price_mrp_per_unit - product_unit_price_after_tax
    markup = (profit_per_unit / product_unit_price_after_tax) * 100
    return round(markup, 2)

def perform_product_calculation(request: ProductCalculationRequest) -> ProductCalculationResult:
    """
    Performs all calculations for a single product and returns the result.
    """
    # Convert percentage to decimal
    tax_rate_decimal = request.gst_percentage / 100.0
    tax_name = f"GST {request.gst_percentage}%"
    
    # Perform all calculations
    subtotal_before_tax_val = calculate_subtotal_before_tax(request.quantity, request.unit_price_before_tax)
    unit_price_after_tax_val = calculate_product_unit_price_after_tax(request.unit_price_before_tax, tax_rate_decimal)
    subtotal_after_tax_val = calculate_subtotal_after_tax(request.quantity, unit_price_after_tax_val)
    effective_rate_val = unit_price_after_tax_val  # Same as unit price after tax
    margin_percentage_val = calculate_margin_percentage(request.sales_price_mrp_per_unit, unit_price_after_tax_val)
    markup_percentage_val = calculate_markup_percentage(request.sales_price_mrp_per_unit, unit_price_after_tax_val)
    
    return ProductCalculationResult(
        # Input data
        product_name=request.product_name,
        quantity=request.quantity,
        unit_price_before_tax=request.unit_price_before_tax,
        gst_percentage=request.gst_percentage,
        sales_price_mrp_per_unit=request.sales_price_mrp_per_unit,
        
        # Calculated values
        subtotal_before_tax=round(subtotal_before_tax_val, 2),
        tax_name=tax_name,
        tax_rate_decimal=round(tax_rate_decimal, 4),
        unit_price_after_tax=round(unit_price_after_tax_val, 2),
        subtotal_after_tax=round(subtotal_after_tax_val, 2),
        effective_rate_per_unit=round(effective_rate_val, 2),
        margin_percentage=margin_percentage_val,
        markup_percentage=markup_percentage_val
    )


# API Routes
@api_router.get("/")
async def root():
    return {"message": "Product Pricing Calculator API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.post("/calculate", response_model=ProductCalculationResult)
async def calculate_product(request: ProductCalculationRequest):
    """
    Calculate pricing for a single product.
    """
    try:
        result = perform_product_calculation(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@api_router.post("/calculate-bulk", response_model=BulkCalculationResult)
async def calculate_bulk_products(request: BulkCalculationRequest):
    """
    Calculate pricing for multiple products at once.
    """
    try:
        calculations = []
        for product_request in request.products:
            result = perform_product_calculation(product_request)
            calculations.append(result)
        
        return BulkCalculationResult(
            calculations=calculations,
            total_products=len(calculations)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bulk calculation error: {str(e)}")

@api_router.post("/calculations", response_model=CalculationHistory)
async def save_calculation(calculation_result: ProductCalculationResult):
    """
    Save a calculation result to history.
    """
    try:
        history_entry = CalculationHistory(calculation_result=calculation_result)
        await db.calculation_history.insert_one(history_entry.dict())
        return history_entry
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving calculation: {str(e)}")

@api_router.get("/calculations", response_model=List[CalculationHistory])
async def get_calculation_history(limit: int = 50):
    """
    Get calculation history (latest first).
    """
    try:
        history = await db.calculation_history.find().sort("saved_at", -1).limit(limit).to_list(limit)
        return [CalculationHistory(**entry) for entry in history]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching history: {str(e)}")

@api_router.delete("/calculations/{calculation_id}")
async def delete_calculation(calculation_id: str):
    """
    Delete a specific calculation from history.
    """
    try:
        result = await db.calculation_history.delete_one({"id": calculation_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Calculation not found")
        return {"message": "Calculation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting calculation: {str(e)}")

@api_router.get("/gst-rates")
async def get_common_gst_rates():
    """
    Get common GST rates used in India.
    """
    return {
        "common_rates": [
            {"rate": 0, "description": "Tax Exempt"},
            {"rate": 5, "description": "GST 5%"},
            {"rate": 12, "description": "GST 12%"},
            {"rate": 18, "description": "GST 18%"},
            {"rate": 28, "description": "GST 28% (Luxury)"}
        ],
        "custom_allowed": True,
        "max_rate": 100
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
