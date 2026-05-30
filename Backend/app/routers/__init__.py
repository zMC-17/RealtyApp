"""Роутеры API приложения."""

from app.routers import auth, contracts, payments, properties, requests

__all__ = [
	"auth",
	"contracts",
	"payments",
	"properties",
	"requests",
]
