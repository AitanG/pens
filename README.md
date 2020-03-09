Pen Bill of Materials API
===

TODO: add a complete description of the project and how to use it here.

### Assumptions

*  Component (part or assembly) names are URL-friendly.
*  A component is considered the same no matter what color its constituent part(s) is/are.
*  The name of a component uniquely identifies it against all other assemblies, subassemblies, and parts.
*  An assembly also used in a different model of pen is also an assembly in that pen, and same with a subassembly.
*  **Add Children Parts to Parent** only accepts parts, which means pens are "constructed" top-down rather than bottom-up.
*  Component names don't contain commas.
*  **Remove Parts From Assembly** only looks at the parts directly used to make that assembly, and does not work for subassemblies.

### Design Decisions

### Key Files

  * `pens_api/views.py`: Defines all API methods, as well as some helper functions
  * `pens_api/urls.py`: URL dispatcher which connects URLs in requests to the relevant API methods
  * `pens_api/models.py`: Holds all pen-related data in memory
  * `demo.py`: Independently runnable code that demonstrates the API's functionality

## Startup Guide

In order to test this API on your local machine, you need to have an environment with Python 3 and `pip` installed.

First, download or clone this repository from GitHub. Next, navigate to the root directory of this repository using the command line and run the following commands:

```
python -m pip install Django
python manage.py runserver
```

The first command installs the Python library Django, which provides all the dependencies needed for the code to execute. The second command spins up a server on your machine using the default port 8000 that is now capable of handling API requests.

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