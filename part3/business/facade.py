from app.repositories.sqlalchemy_repository import SQLAlchemyRepository

def get_repository(model):
    
    return SQLAlchemyRepository(model)
