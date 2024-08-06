
## What is Poetry?

[Poetry](https://python-poetry.org/docs/pyproject/) is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

## Why Use Poetry?

- **Simplifies Dependency Management**: Poetry provides a simple and easy-to-use interface for managing dependencies, ensuring that your project has the correct versions of libraries it needs.
- **Handles Package Publishing**: Poetry helps in building and publishing your packages to PyPI or any other repository.
- **Environment Isolation**: Poetry uses virtual environments to isolate dependencies for each project, avoiding conflicts.
- **Consistency**: Ensures that everyone working on the project uses the same dependency versions.
- **Better Metadata Management**: Uses `pyproject.toml` which is a standardized file format for specifying project requirements and build configuration.

## Poetry vs Pip Requirements

| Feature               | Poetry                                                   | Pip Requirements                                         |
|-----------------------|----------------------------------------------------------|----------------------------------------------------------|
| Dependency Management | Uses `pyproject.toml` and `poetry.lock` for dependencies | Uses `requirements.txt`                                  |
| Virtual Environments  | Automatically creates and manages virtual environments   | Requires manual creation and management of virtual environments |
| Version Constraints   | Allows flexible version constraints with better resolution| Limited to version pinning                                |
| Project Publishing    | Built-in support for publishing packages to PyPI         | Requires additional tools (like `twine`) for publishing   |
| Development Workflow  | Provides commands for testing, building, and publishing  | Requires separate tools and commands for these tasks      |

## Installing Poetry

To install Poetry, you can use the following command:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Alternatively, you can install Poetry using pip:

```sh
pip install poetry
```

After installation, you can verify it by running:

```sh
poetry --version
```

## Setting Up a Django Project with Poetry

1. **Create a New Project Directory**:
   ```sh
   mkdir my_django_project
   cd my_django_project
   ```

2. **Initialize a New Poetry Project**:
   ```sh
   poetry init
   ```
   Follow the prompts to set up your project details.

3. **Add Django as a Dependency**:
   ```sh
   poetry add django
   ```

4. **Install Dependencies**:
   ```sh
   poetry install
   ```

5. **Create a Django Project**:
   ```sh
   poetry run django-admin startproject myproject .
   ```

6. **Run Migrations and Start the Development Server**:
   ```sh
   poetry run python manage.py migrate
   poetry run python manage.py runserver
   ```

7. **Access Your Django Application**:
   Open your web browser and navigate to `http://127.0.0.1:8000/` to see your Django application running.

