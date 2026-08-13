"""Unit tests for the maintained animal rescue data layer."""

import unittest
from unittest.mock import MagicMock

from animal_shelter import AnimalShelter


class AnimalShelterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = MagicMock()
        self.database = MagicMock()
        self.collection = MagicMock()
        self.client.__getitem__.return_value = self.database
        self.database.__getitem__.return_value = self.collection
        self.shelter = AnimalShelter(client=self.client)

    def test_create_inserts_into_configured_collection(self) -> None:
        self.collection.insert_one.return_value.inserted_id = "animal-123"

        inserted_id = self.shelter.create({"name": "Milo", "type": "Dog"})

        self.collection.insert_one.assert_called_once_with(
            {"name": "Milo", "type": "Dog"}
        )
        self.assertEqual("animal-123", inserted_id)

    def test_read_returns_matching_documents(self) -> None:
        cursor = MagicMock()
        cursor.__iter__.return_value = iter([{"name": "Milo"}])
        self.collection.find.return_value = cursor

        result = self.shelter.read({"type": "Dog"})

        self.collection.find.assert_called_once_with({"type": "Dog"})
        self.assertEqual([{"name": "Milo"}], result)

    def test_read_applies_limit(self) -> None:
        cursor = MagicMock()
        limited_cursor = MagicMock()
        limited_cursor.__iter__.return_value = iter([{"name": "Milo"}])
        cursor.limit.return_value = limited_cursor
        self.collection.find.return_value = cursor

        result = self.shelter.read(limit=1)

        cursor.limit.assert_called_once_with(1)
        self.assertEqual([{"name": "Milo"}], result)

    def test_update_sets_fields_on_one_matching_document(self) -> None:
        self.collection.update_one.return_value.modified_count = 1

        modified = self.shelter.update(
            {"name": "Milo"},
            {"status": "trained"},
        )

        self.collection.update_one.assert_called_once_with(
            {"name": "Milo"},
            {"$set": {"status": "trained"}},
        )
        self.assertEqual(1, modified)

    def test_delete_removes_one_matching_document(self) -> None:
        self.collection.delete_one.return_value.deleted_count = 1

        deleted = self.shelter.delete({"name": "Milo"})

        self.collection.delete_one.assert_called_once_with({"name": "Milo"})
        self.assertEqual(1, deleted)

    def test_empty_write_filters_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.shelter.create({})
        with self.assertRaises(ValueError):
            self.shelter.update({}, {"status": "trained"})
        with self.assertRaises(ValueError):
            self.shelter.delete({})


if __name__ == "__main__":
    unittest.main()
