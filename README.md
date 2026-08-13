# Animal Rescue CRUD and Dashboard Project

**CS-340 Client-Server Development | Python, MongoDB, PyMongo**

This project was developed for a client scenario involving Grazioso Salvare, an organization that identifies and trains rescue animals. The goal was to make animal records easier to store, search, update, and use through a data-driven dashboard.

My work focused on separating database operations from the user interface so the same Python data-access module could support a dashboard or another application without duplicating database logic.

## Project Goals

- Connect a Python application to MongoDB.
- Implement create, read, update, and delete operations.
- Return query results in a format that a dashboard can use.
- Keep database responsibilities separate from interface logic.
- Translate client requirements into useful filters and visual information.

## CRUD Module

The reusable [`CRUD_Python_Module.py`](CRUD_Python_Module.py) defines an `AnimalShelter` class that centralizes the application's MongoDB connection and data operations.

| Operation | Purpose |
| --- | --- |
| Create | Add a new animal record |
| Read | Find records matching a supplied query |
| Update | Modify fields in a matching record |
| Delete | Remove a matching record |

Credentials are supplied to the class constructor instead of being written directly into the source code. The database, collection, host, and port are defined in one place to make the connection behavior easier to understand and maintain.

## Design Approach

I treated the project as a client problem instead of only a programming exercise. That meant considering how the organization would search records, interpret results, and reuse the database layer as the dashboard changed.

Separating the CRUD module from the dashboard improved:

- **Maintainability:** database changes are isolated from interface code.
- **Reusability:** the module can support other administrative tools or services.
- **Troubleshooting:** connection, query, and display problems can be investigated separately.
- **Adaptability:** new filters or interface features do not require rewriting the basic data operations.

## Repository Contents

- [`CRUD_Python_Module.py`](CRUD_Python_Module.py) - reusable MongoDB data-access class
- Project milestones and reports - supporting design and implementation documentation
- Project packages - dashboard and course-delivery artifacts retained from the original coursework

## Skills Demonstrated

Python, MongoDB, PyMongo, CRUD operations, client-server design, database integration, modular development, requirements analysis, debugging, and client-centered problem solving.

## Portfolio Note

This repository preserves the original course deliverables. A future cleanup can move the dashboard source out of the packaged archives, add automated tests, and use environment-based configuration for easier local setup.

## Author

Michael B. Wood  
Bachelor of Science in Computer Science, Software Engineering concentration  
Southern New Hampshire University | Coursework completing August 2026
