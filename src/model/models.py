"""Clases Model del ORM (Peewee)."""
from datetime import datetime

from peewee import (CharField, DateTimeField, DecimalField, ForeignKeyField,
                    Model)

from src.model.database import db


class BaseModel(Model):
    class Meta:
        database = db


class Categoria(BaseModel):
    """Categoría de producto (tabla fija que se llena al crear las tablas)."""
    clave = CharField(unique=True)
    nombre = CharField()
    formula = CharField()


class Calculo(BaseModel):
    """Un cálculo de impuesto guardado por el usuario."""
    categoria = ForeignKeyField(Categoria, backref="calculos")
    valor = DecimalField(max_digits=18, decimal_places=2)       # valor o cantidad
    mililitros = DecimalField(max_digits=18, decimal_places=2, default=0)
    impuesto = DecimalField(max_digits=18, decimal_places=2)
    creado = DateTimeField(default=datetime.now)
