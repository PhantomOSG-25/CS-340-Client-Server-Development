"""MongoDB data-access layer for animal rescue records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import quote_plus


class AnimalShelter:
    """Provide validated CRUD operations for one MongoDB collection."""

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        *,
        host: str = "localhost",
        port: int = 27017,
        database_name: str = "aac",
        collection_name: str = "animals",
        auth_source: str | None = None,
        client: Any | None = None,
    ) -> None:
        """Configure the data layer or use an injected MongoDB client."""
        if client is None:
            from pymongo import MongoClient

            uri = self._build_uri(
                username=username,
                password=password,
                host=host,
                port=port,
                auth_source=auth_source or database_name,
            )
            self.client = MongoClient(uri)
            self._owns_client = True
        else:
            self.client = client
            self._owns_client = False

        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    @staticmethod
    def _build_uri(
        *,
        username: str | None,
        password: str | None,
        host: str,
        port: int,
        auth_source: str,
    ) -> str:
        if bool(username) != bool(password):
            raise ValueError("username and password must be supplied together")

        if username and password:
            user = quote_plus(username)
            secret = quote_plus(password)
            source = quote_plus(auth_source)
            return f"mongodb://{user}:{secret}@{host}:{port}/?authSource={source}"

        return f"mongodb://{host}:{port}"

    @staticmethod
    def _require_document(value: Mapping[str, Any] | None, name: str) -> dict[str, Any]:
        if not isinstance(value, Mapping) or not value:
            raise ValueError(f"{name} must be a non-empty mapping")
        return dict(value)

    def create(self, document: Mapping[str, Any]) -> Any:
        """Insert one animal record and return its generated identifier."""
        result = self.collection.insert_one(
            self._require_document(document, "document")
        )
        return result.inserted_id

    def read(
        self,
        query: Mapping[str, Any] | None = None,
        *,
        limit: int = 0,
    ) -> list[dict[str, Any]]:
        """Return records matching a query, optionally limited in count."""
        if limit < 0:
            raise ValueError("limit cannot be negative")

        cursor = self.collection.find(dict(query or {}))
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    def update(
        self,
        query: Mapping[str, Any],
        changes: Mapping[str, Any],
    ) -> int:
        """Update one matching record and return the modified count."""
        result = self.collection.update_one(
            self._require_document(query, "query"),
            {"$set": self._require_document(changes, "changes")},
        )
        return result.modified_count

    def delete(self, query: Mapping[str, Any]) -> int:
        """Delete one matching record and return the deleted count."""
        result = self.collection.delete_one(
            self._require_document(query, "query")
        )
        return result.deleted_count

    def close(self) -> None:
        """Close a client created by this data layer."""
        if self._owns_client:
            self.client.close()

    def __enter__(self) -> "AnimalShelter":
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()
