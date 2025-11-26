"""
Request validation utilities
"""
from pydantic import BaseModel, ValidationError

def validate_request(schema: BaseModel, data: dict):
    """
    Validate request data against Pydantic schema
    
    Args:
        schema: Pydantic model class
        data: Request data dictionary
        
    Returns:
        Validated model instance
        
    Raises:
        ValidationError: If validation fails
    """
    try:
        return schema(**data)
    except ValidationError as e:
        raise e
