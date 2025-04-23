from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.db.base_class import Base as BaseClass


class PricePrediction(Base, BaseClass):
    """
    PricePrediction model representing predicted prices for products
    at specific future dates.
    """
    
    product_id = Column(String(36), ForeignKey("product.id"), nullable=False, index=True)
    predicted_price = Column(Float, nullable=False)
    prediction_date = Column(DateTime, nullable=False, index=True)  # The date for which the price is predicted
    generated_at = Column(DateTime, nullable=False)  # When the prediction was generated
    confidence_score = Column(Float, nullable=True)  # Optional confidence level (0-1)
    model_version = Column(String(50), nullable=True)  # Version of ML model used
    factors_influence = Column(JSON, nullable=True)  # JSON of factor influences on this prediction
    
    # Relationships
    product = relationship("Product", back_populates="predictions")
    
    def __repr__(self) -> str:
        return f"<PricePrediction(id={self.id}, product_id={self.product_id}, price={self.predicted_price}, date={self.prediction_date})>"


class PredictionModel(Base, BaseClass):
    """
    Model to track information about the prediction models used
    to generate price predictions.
    """
    
    name = Column(String(100), nullable=False)
    version = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    parameters = Column(JSON, nullable=True)  # Model hyperparameters and configuration
    performance_metrics = Column(JSON, nullable=True)  # Validation metrics
    training_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self) -> str:
        return f"<PredictionModel(id={self.id}, name={self.name}, version={self.version})>"


class ModelTrainingLog(Base, BaseClass):
    """
    Log of model training runs to track the history of model development.
    """
    
    model_id = Column(String(36), ForeignKey("predictionmodel.id"), nullable=False)
    training_start = Column(DateTime, nullable=False)
    training_end = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)  # success, failed, etc.
    error_message = Column(String(500), nullable=True)
    training_metrics = Column(JSON, nullable=True)
    
    # Relationships
    model = relationship("PredictionModel")
    
    def __repr__(self) -> str:
        return f"<ModelTrainingLog(id={self.id}, model_id={self.model_id}, status={self.status})>"
