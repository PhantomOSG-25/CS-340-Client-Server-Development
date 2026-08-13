"""Rescue-category rules shared by the dashboard and tests."""

from __future__ import annotations

from typing import Any


WATER_BREEDS = [
    "Labrador Retriever Mix",
    "Chesapeake Bay Retriever",
    "Newfoundland",
]

MOUNTAIN_BREEDS = [
    "German Shepherd",
    "Alaskan Malamute",
    "Old English Sheepdog",
    "Siberian Husky",
    "Rottweiler",
]

DISASTER_BREEDS = [
    "Doberman Pinscher",
    "German Shepherd",
    "Golden Retriever",
    "Bloodhound",
    "Rottweiler",
]


def classify_rescue_type(breed: str) -> str:
    """Return the primary rescue category associated with a breed."""
    if breed in WATER_BREEDS:
        return "Water Rescue"
    if breed in MOUNTAIN_BREEDS:
        return "Mountain Rescue"
    if breed in DISASTER_BREEDS:
        return "Disaster or Individual Tracking"
    return "Other"


def build_rescue_query(rescue_type: str | None) -> dict[str, Any]:
    """Translate a dashboard selection into a MongoDB query."""
    if rescue_type == "Water":
        return {
            "breed": {"$in": WATER_BREEDS},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156},
        }
    if rescue_type == "Mountain":
        return {
            "breed": {"$in": MOUNTAIN_BREEDS},
            "sex_upon_outcome": "Intact Male",
        }
    if rescue_type == "Disaster":
        return {
            "breed": {"$in": DISASTER_BREEDS},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300},
        }
    return {}
