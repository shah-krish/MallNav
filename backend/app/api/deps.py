from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

# Annotated[Type, extra_info] means "This value has this type, and here's some additional information about it. 
# No need to repeatedly write "db: Session = Depends(get_db)".With Annotated, you define the dependency once and reuse it
SessionDep = Annotated[Session, Depends(get_db)]