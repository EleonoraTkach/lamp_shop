from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base

def generate_order_number():
    return f"d{uuid.uuid4().hex[:10]}"

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    order_number = Column(String, unique=True, nullable=False, default=generate_order_number)
    status = Column(String, nullable=False, default="created")

    phone_number = Column(String, nullable=False)
    user_full_name = Column(String, nullable=False)

    preorder_id = Column(Integer, nullable=True)

    total_cost = Column(Numeric(10, 2), nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    is_deleted = Column(Boolean, default=False)

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )