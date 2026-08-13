# Animal Rescue CRUD and Dashboard Project

[![Python tests](https://github.com/PhantomOSG-25/animal-rescue-dashboard/actions/workflows/test.yml/badge.svg)](https://github.com/PhantomOSG-25/animal-rescue-dashboard/actions/workflows/test.yml)

**CS-340 Client-Server Development | Python, MongoDB, PyMongo**

This project was developed for a client scenario involving Grazioso Salvare, an organization that identifies and trains rescue animals. The goal was to make animal records easier to store, search, update, and use through a data-driven dashboard.

My work focused on separating database operations from the user interface so the same Python data-access module could support a dashboard or another application without duplicating database logic.

The maintained version exposes both layers directly: a testable MongoDB data-access class and a standalone Dash application with table filtering, rescue-category visualization, and record mapping.

## Project Goals

- Connect a Python application to MongoDB.
- Implement create, read, update, and delete operations.
- Return query results in a format that a dashboard can use.
- Keep database responsibilities separate from interface logic.
- Translate client requirements into useful filters and visual information.

## Maintained CRUD Module

The maintained [`animal_shelter.py`](animal_shelter.py) module defines an `AnimalShelter` class that centralizes the application's MongoDB connection and data operations. It operates directly on the configured collection, validates write inputs, escapes credentials in connection strings, supports dependency injection for tests, and closes client resources it creates.

| Operation | Purpose |
| --- | --- |
| Create | Add a new animal record |
| Read | Find records matching a supplied query |
| Update | Modify fields in a matching record |
| Delete | Remove a matching record |

Credentials are supplied to the class constructor instead of being written directly into the source code. Host, port, database, collection, and authentication source are configurable, while safe local defaults keep the basic setup concise.

## Quick Start

1. Create a virtual environment and install the runtime dependency:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

2. Supply credentials through your environment or another secret-management method, then create the data layer:

   ```python
   import os

   from animal_shelter import AnimalShelter

   shelter = AnimalShelter(
       username=os.environ["MONGODB_USERNAME"],
       password=os.environ["MONGODB_PASSWORD"],
   )

   dogs = shelter.read({"animal_type": "Dog"}, limit=25)
   shelter.close()
   ```

Do not commit database passwords or local `.env` files.

## Tests

The unit tests inject a mock MongoDB client, so CRUD behavior can be checked without a running database:

```bash
python -m unittest discover -s tests -v
```

The suite covers collection selection, create/read/update/delete behavior, result handling, limits, rescue-category queries, and validation that prevents empty write operations.

## Run the Dashboard

Copy [`.env.example`](.env.example) to your preferred local secret-management setup and provide the MongoDB connection values as environment variables. Never commit the populated values.

```bash
export MONGODB_USERNAME="your_username"
export MONGODB_PASSWORD="your_password"
python dashboard.py
```

The dashboard provides:

- water, mountain, and disaster/tracking rescue filters
- a sortable and filterable animal-record table
- a rescue-category pie chart derived from the visible records
- a map for the selected animal when location data is available
- clear empty-data and missing-location states

## Design Approach

I treated the project as a client problem instead of only a programming exercise. That meant considering how the organization would search records, interpret results, and reuse the database layer as the dashboard changed.

Separating the CRUD module from the dashboard improved:

- **Maintainability:** database changes are isolated from interface code.
- **Reusability:** the module can support other administrative tools or services.
- **Troubleshooting:** connection, query, and display problems can be investigated separately.
- **Adaptability:** new filters or interface features do not require rewriting the basic data operations.

## Repository Contents

- [`animal_shelter.py`](animal_shelter.py) - maintained, testable MongoDB data-access class
- [`dashboard.py`](dashboard.py) - standalone Dash application
- [`rescue_filters.py`](rescue_filters.py) - tested rescue classification and MongoDB query rules
- [`tests/test_animal_shelter.py`](tests/test_animal_shelter.py) - dependency-injected unit tests
- [`tests/test_rescue_filters.py`](tests/test_rescue_filters.py) - rescue classification and query tests
- [`CRUD_Python_Module.py`](CRUD_Python_Module.py) - original course implementation retained for comparison
- [`requirements.txt`](requirements.txt) - runtime dependency manifest
- Project milestones and reports - supporting design and implementation documentation

## Skills Demonstrated

Python, MongoDB, PyMongo, CRUD operations, client-server design, database integration, modular development, requirements analysis, debugging, and client-centered problem solving.

## Project Status

The core data-access layer and dashboard are visible and configurable, and the logic that can run without MongoDB or Dash is unit tested. Credential-bearing course archives were removed after the maintained, sanitized source was published.

## Author

Michael B. Wood  
Bachelor of Science in Computer Science, Software Engineering concentration  
Southern New Hampshire University | Coursework completing August 2026
