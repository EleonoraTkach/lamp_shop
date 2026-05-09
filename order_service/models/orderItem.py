from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base
import uuid


class OrderItem(Base):
    __tablename__ = "order_x_product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)

    quantity = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    is_deleted = Column(Boolean, default=False)

    order = relationship("Order", back_populates="items")

    __table_args__ = (
        CheckConstraint(
            """
            (product_id IS NOT NULL AND image_url IS NULL)
            OR
            (product_id IS NULL AND image_url IS NOT NULL)
            """,
            name="ck_product_or_image_only_one"
        ),
    )