from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint,UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, nullable=False, index=True)

    order_number = Column(String, nullable=False, index=True)

    score = Column(Integer, nullable=False)

    description = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    is_deleted = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint("score >= 1 AND score <= 5", name="check_score_range"),
        UniqueConstraint("product_id", "order_number", name="uq_review_product_order"),
    )