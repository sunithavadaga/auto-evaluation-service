from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from services.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    assignment_id = Column(Integer, nullable=False)
    submission_link = Column(String(500), nullable=False)
    score = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String(50), default="submitted")
    created_at = Column(DateTime(timezone=True), server_default=func.now())