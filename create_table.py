# Crie um script separado, por exemplo: create_tables.py

from sqlalchemy import create_engine

from fastapi_zero.models import table_registry
from fastapi_zero.settings import Settings

db_url = Settings().DATABASE_URL.replace('sqlite+aiosqlite://', 'sqlite:///')  # type: ignore
print('URL usada:', db_url)  # Adicione este print

engine = create_engine(db_url)


def create_table():
    table_registry.metadata.create_all(engine)
    print('Tabelas criadas com sucesso!')
