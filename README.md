
# Task Week 3 

## Overview

This repository contains the solution for Task of Week3

## Running Local Development Server

### Set Up Virtual Environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

## Dependencies

Dependencies are managed inside the `requirement` folder.

### Install Packages and Dependencies:

```bash
pip install -r requirements/dev.txt
```

### Environment Variables:

Copy `sample.env.py` to `env.py` and configure necessary environment variables like database credentials, API keys, etc.

### Initialize Database:

```bash
python manage.py migrate
```

### Run Development Server:

```bash
python manage.py runserver
```

### Access the Development Server:

Open your web browser and go to `http://127.0.0.1:8000/` to see the Django project running.


