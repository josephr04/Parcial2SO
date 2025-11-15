
"""Controlador ligero para el módulo de categorías.

Este archivo expone funciones que la vista puede usar. Internamente
llama a `model.py`.
"""
from . import model


def crear_categoria(nombre, ruta_imagen=None):
	return model.crear_categoria(nombre, ruta_imagen)


def obtener_categorias():
	return model.obtener_categorias()


def obtener_categoria(id_):
	return model.obtener_categoria(id_)


def actualizar_categoria(id_, nombre, ruta_imagen=None):
	return model.actualizar_categoria(id_, nombre, ruta_imagen)


def eliminar_categoria(id_):
	return model.eliminar_categoria(id_)
