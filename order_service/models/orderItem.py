from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base
import uuid


class OrderItem(Base):
    __tablename__ = "order_x_product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, nullable=False)

    quantity = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    is_deleted = Column(Boolean, default=False)

    order = relationship("Order", back_populates="items")