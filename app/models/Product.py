from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)

    price = Column(Numeric(8,2), nullable=False)
    quantity = Column(Integer, nullable=False,  default=0)

    category_id = Column(Integer, ForeignKey("category.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    is_deleted = Column(Boolean, default=False)

    category = relationship("Category", back_populates="products")