Pen Bill of Materials API
===

This repository has the code to run a server that hosts an API for bills of materials for pens! This document discusses some design considerations (**Assumptions**, **Design Decisions**, **Extension**), explains the repository on a high-level (**Design Decisions**, **Key Files**), provides instructions for testing the code (**Startup Guide**), and provides documentation for API methods (**API Documentation**).

### Assumptions

*  Component (part or assembly) names are URL-friendly.
*  A component is considered the same no matter what color its constituent part(s) is/are.
*  The name of a component uniquely identifies it against all other assemblies, subassemblies, and parts.
*  An assembly also used in a different model of pen is also an assembly in that pen, and same with a subassembly.
*  **Add Children Parts to Parent** only accepts parts, which means pens are "constructed" top-down rather than bottom-up.
*  Component names don't contain commas.
*  **Remove Parts From Assembly** only looks at the parts directly used to make that assembly, and does not work for subassemblies.
*  Duplicates of parts in the same assembly are not allowed.
*  Whether or not a part is the same color as the pen is a universal property of the part, so that specifying the pen's color specifies each constituent part's color.

### Design Decisions

  * The URL scheme is clearly orgnized according to the best practices of API design, and is meant to be self-descriptive. See **API Documentation** below.
  * The code is organized as a Django project, which separates URL dispatch, function definition, unit tests, models, and settings into different files.
  * All data structures are held in-memory, since this particular application has modest capacity demands. This simplifies the design and improves performance.
  * All pen-related data is primarily referenced via JSON-like Python dictionaries, one containing assemblies and one containing parts. This is because most of the requests make clear distinctions between parts and assemblies, with the exception of requests like **List Children**.
  * Parts and assemblies can also be referenced in relation to each other through the members of the Component class, which all components belong to. A Component lists all of its parents and children (if they exist) in a tree-like fashion, and has a name and component type. Requests like **List Children** take advantage of this tree-like organization, and the `POST` and `DELETE` features are able to efficiently and concisely keep parent and child lists up-to-date.

### Extension

In addition to the required methods, there are two related methods which output the full hierarchy of each bill of materials--one method is JSON-encoded and the other method is a multi-level, human-readable bullet point list. Search below for the following:

  * **Display Hierarchy Text**
  * **Display Hierarchy JSON**

This feature might be a useful way for the user to visualize their database of bills of materials or visualize the construction of a particular pen. Additionally, the JSON option allows any client to define their own preferred `GET` functionality for front-end apps, like visualization tools, more advanced logical queries, and typeaheads / information retrieval purposes.

Each time a change is made (i.e., a `POST` or `DELETE` request is made), both the plain text and JSON hierarchy representations are recompiled. This is because with this particular application, we can expect queries to be predominantly `GET`s, and it would be wasteful to recompile the hierarchies every time someone requests to see them. Even though we can expect relatively few `POST` and `DELETE` requests, this functionality is made to have a minimal impact on the performance of these requests with the use of multi-threading. Each time the database is updated, a new thread is spun off which asynchronously recompiles the hierarchies after the request returns, and any existing threads are killed to avoid race conditions. This means any subsequent calls to Display Hierarchy Text/JSON might not be completely up-to-date, but should work for all intents and purposes.

### Key Files

  * `pens_api/views.py`: Defines all API methods, as well as some helper functions
  * `pens_api/urls.py`: URL dispatcher which connects URLs in requests to the relevant API methods
  * `pens_api/models.py`: Holds all pen-related data in memory
  * `demo.py`: Independently runnable code that demonstrates the API's functionality

## Startup Guide

In order to test this API on your local machine, you need to have an environment with Python 3 and `pip` installed.

First, download or clone this repository from GitHub. Next, navigate to the root directory of this repository using the command line and run the following commands (assuming you don't already have Django installed):

```
python -m pip install Django
python manage.py runserver
```

The first command installs the Python library Django, which provides all the dependencies needed for the code to execute. The second command spins up a server on your machine using the default port 8000 that is now capable of handling API requests. Python may prompt you to install libraries like `threading` and `json` if you haven't already installed them--if so, install them and try the `runserver` command again.

To test the API functionality, use the client of your choice using the domain `http://localhost:8000`. Browsers automatically send requests with the `GET` method, but for `POST` and `DELETE` requests, you have to use a different type of client, like Postman. As an example, to list all known parts, make the following `GET` request:

```
`http://localhost:8000/part/
```

The Python script named `demo.py` demonstrates the API's functionality by creating two different models of pen and two colors of each model, and performing a series of `GET` queries on the bills of materials. In order to run the script, you must have the Python library `requests` installed.

Any changes you make through the API will *not* persist through server restarts.

The file `pens/pens_api/tests.py` in this repository contains some basic unit tests that can be run via the command:

```
python manage.py test
```

## API Documentation

### List Parts

List all known parts.

**URL:** `part/`

**Method:** `GET`

### Create Part

Make a new part known to the API and available to add to bills of materials.

**URL:** `part/<name>`

**Method:** `POST`

**Conditions for** `400 Bad Request`**:**

  * The requested part already exists.

### Delete Part

Delete a part API-wide, also removing it from any bills of materials.

**URL:** `part/<name>`

**Method:** `DELETE`

**Conditions for** `400 Bad Request`**:**

  * The requested part does not exist.

### Add Children Parts to Parent

Indicate a list of parts as "children" of a "parent" part, which then becomes an assembly.

**URL:** `part/<parentName>/child/part/<childrenNames>`

**Method:** `POST`

**Conditions for** `400 Bad Request`**:**

  * The parent part does not exist.
  * The parent part is an assembly.
  * A specified child part does not exist.
  * A specified child part is an assembly.
  * A specified child part is the same as the parent part.

### List Component Parts

List all parts used in any bills of materials.

**URL:** `part/component/`

**Method:** `GET`

### List Orphan Parts

List all known parts *not* used in any bills of materials.

**URL:** `part/orphan/`

**Method:** `GET`

### List Assemblies Containing Part

List all known assemblies containing the specified part.

**URL:** `part/<name>/assembly/`

**Method:** `GET`

**Conditions for** `400 Bad Request`**:**

  * The part does not exist.

### List Assemblies

List all known assemblies.

**URL:** `assembly/`

**Method:** `GET`

### List Top-Level Assemblies

List all assemblies that are never used in any other assemblies.

**URL:** `assembly/top/`

**Method:** `GET`

### List Subassemblies

List all assemblies that are used in other assemblies.

**URL:** `assembly/subassembly/`

**Method:** `GET`

### List Children

List all components (parts or subassemblies) used in the specified assembly.

**URL:** `assembly/<parentName>/child/`

**Method:** `GET`

**Conditions for** `400 Bad Request`**:**

  * The parent assembly does not exist.

### List First-Level Children

List all components (parts or subassemblies) used in the specified assembly, not through a subassembly of the specified assembly.

**URL:** `assembly/<parentName>/child/first/`

**Method:** `GET`

**Conditions for** `400 Bad Request`**:**

  * The parent assembly does not exist.

### List Parts In Assembly

List all parts used in the specified assembly.

**URL:** `assembly/<parentName>/child/part/`

**Method:** `GET`

**Conditions for** `400 Bad Request`**:**

  * The parent assembly does not exist.

### Remove Parts From Assembly

Remove a list of parts from the specified assembly.

**URL:** `assembly/<parentName>/child/part/<childrenNames>`

**Method:** `DELETE`

**Conditions for** `400 Bad Request`**:**

  * The parent assembly does not exist.
  * The parent assembly is a part.
  * A specified part is an assembly.
  * A specified part does not exist.
  * A specified part was not found in the first level of the assembly.

### Display Hierarchy Text

Display a text rendering of the full hierarchy of each top-level assembly

**URL:** `hierarchy-text`

**Method:** `GET`

### Display Hierarchy JSON

Display a JSON object representing full hierarchy of each top-level assembly

**URL:** `hierarchy-json`

**Method:** `GET`
