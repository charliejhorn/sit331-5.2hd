class NotFoundException(Exception):
    """exception raised when a resource is not found by its ID"""
    
    def __init__(self, entity_type, id):
        self.entity_type = entity_type
        self.id = id
        super().__init__(f"{entity_type} with id {id} not found")


class DuplicateException(Exception):
    """exception raised when a duplicate value is found for a field"""
    
    def __init__(self, field, value):
        self.field = field
        self.value = value
        super().__init__(f"duplicate value '{value}' found for field '{field}'")