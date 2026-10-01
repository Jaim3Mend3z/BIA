from logging.config import fileConfig
from pathlib import Path
import os

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv

from app.db.base import Base
from app import models


# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]


# ============================================================
# VARIABLES DE ENTORNO
# ============================================================

load_dotenv(BASE_DIR / ".env")


# ============================================================
# CONFIGURACIÓN DE ALEMBIC
# ============================================================

config = context.config


# ============================================================
# LOGGING
# ============================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ============================================================
# CONEXIÓN A POSTGRESQL
# ============================================================

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError(
        "DATABASE_URL no está configurada en el archivo .env"
    )

config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%")
)


# ============================================================
# METADATA DE LOS MODELOS
# ============================================================

target_metadata = Base.metadata


# ============================================================
# FILTRO DE OBJETOS
# ============================================================

def include_object(
    object,
    name,
    type_,
    reflected,
    compare_to,
):
    """
    Evita que Alembic intente eliminar estructuras que
    ya existen en PostgreSQL pero que no pertenecen a BIA.

    Esto es especialmente importante con PostGIS, que
    incorpora sus propias tablas y estructuras.
    """

    if type_ == "table":
        if reflected and compare_to is None:
            return False

    return True


# ============================================================
# MIGRACIONES OFFLINE
# ============================================================

def run_migrations_offline() -> None:
    """
    Ejecuta migraciones sin conexión directa a PostgreSQL.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# MIGRACIONES ONLINE
# ============================================================

def run_migrations_online() -> None:
    """
    Ejecuta migraciones mediante conexión directa
    a PostgreSQL.
    """

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
