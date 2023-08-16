from datetime import datetime

import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON

metadata = MetaData()

# именовать таблицы стоит в единственном числе

# таблица role
role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

# таблица user
user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

# Не забываем реренести созданные таблицы в базу данных с помощью миграций(Alembic)
