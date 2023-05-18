
from pathlib import Path

BASE_DIR = Path(__file__).parent
print(BASE_DIR)

class Config:
    SQLALCHEMY_DATABASE_URI: 'postgresql://postgres:password@localhost:5432/example'