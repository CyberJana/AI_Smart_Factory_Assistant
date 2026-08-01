from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=12, max_length=128)
    role: str = "operator"


class UserOut(ORMModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_verified: bool


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MachineOut(ORMModel):
    id: str
    code: str
    name: str
    location: str
    status: str
    health_score: float
    utilization: float
    updated_at: datetime


class SensorReadingOut(ORMModel):
    id: str
    machine_id: str
    metric: str
    value: float
    unit: str
    recorded_at: datetime


class MaintenanceOut(ORMModel):
    id: str
    machine_id: str
    title: str
    maintenance_type: str
    priority: str
    status: str
    due_at: datetime
    notes: str | None


class AlertOut(ORMModel):
    id: str
    machine_id: str | None
    title: str
    severity: str
    message: str
    acknowledged: bool
    created_at: datetime


class ProductionOrderOut(ORMModel):
    id: str
    order_number: str
    product_name: str
    target_quantity: int
    actual_quantity: int
    status: str
    due_at: datetime


class InventoryOut(ORMModel):
    id: str
    sku: str
    name: str
    category: str
    quantity: float
    reorder_point: float
    unit: str
    location: str


class ProductOut(ORMModel):
    id: str
    sku: str
    name: str
    category: str
    unit: str


class EnergyOut(ORMModel):
    id: str
    machine_id: str | None
    source: str
    consumption_kwh: float
    carbon_kg: float
    recorded_at: datetime


class InspectionCreate(BaseModel):
    product_code: str = Field(min_length=2, max_length=60)
    image_url: str | None = None


class InspectionOut(ORMModel):
    id: str
    product_code: str
    image_url: str | None
    result: str
    defect_type: str | None
    confidence: float
    bounding_boxes: list
    inspected_at: datetime


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


class ReportRequest(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    report_type: str = "executive"


class ReportOut(ORMModel):
    id: str
    title: str
    report_type: str
    generated_by: str
    created_at: datetime
