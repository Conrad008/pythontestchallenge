# Django Password Reset

A Django password-reset application built as a practical project for learning **Test-Driven Development (TDD)** and automated testing with Python.

The project implements a complete password-reset workflow, including requesting a reset, generating a secure token, sending a reset email, validating the token, handling expiration, validating the new password, and changing the user's password.

The project was developed using a **test-first approach**, with tests driving the implementation.

---


## Project Goals

The main goal of this project was to learn and practice:

* Test-Driven Development (TDD)
* `pytest`
* `pytest-django`
* Factory Boy
* Mocking and patching
* Django forms and validation
* Django authentication
* Password-reset tokens
* Email services
* Database testing
* Testing HTTP requests and responses
* Production deployment with Render

Rather than building the feature first and writing tests afterwards, the project uses the TDD cycle:

```text
RED
 ↓
Write a failing test
 ↓
GREEN
 ↓
Write the minimum code needed to pass
 ↓
REFACTOR
 ↓
Improve the implementation
 ↓
Repeat
```

---

# Password Reset Feature

The application provides a complete password-reset workflow.

### 1. Request a reset

The user enters their email address at:

`/password-reset/`

Django looks for the account and generates a password-reset token for an existing user.

### 2. Generate a token

Django's built-in `default_token_generator` is used to generate a secure, time-sensitive password-reset token.

The reset URL contains:

* `uidb64`
* `token`

For example:

```text
/password-reset/Mg/<token>/
```

### 3. Send the email

The application constructs a password-reset URL and sends an email containing the link.

The email functionality is separated into a service so that it can be tested independently and mocked during tests.

### 4. Redeem the token

The user follows the password-reset link.

Django checks:

* Whether the user exists
* Whether the token is valid
* Whether the token has expired

### 5. Set a new password

The user enters and confirms a new password.

The password is validated before being saved.

---

#  Testing

Testing is the core of this project.

The project uses:

* **pytest** — testing framework
* **pytest-django** — Django integration for pytest
* **Factory Boy** — test data generation
* **pytest-mock / unittest.mock** — mocking and patching

Run the test suite with:

```bash
python -m pytest -v
```

---

## Test Coverage

The password-reset feature includes tests for:

### Existing users

A password-reset request for an existing user should generate a reset URL and send the reset email.

### Unknown users

A request for an unknown email should not reveal whether an account exists.

This prevents users from using the password-reset form to enumerate registered accounts.

### Mocked email service

The email service is mocked so that tests do not actually send emails.

The tests verify that the email service is called with the expected arguments.

For example:

```python
mock_send_email.assert_called_once_with(
    user.email,
    expected_reset_url,
)
```

### Valid token

A valid password-reset token should allow the user to access the password-reset form.

### Invalid token

An invalid or modified token should be rejected.

### Expired token

An expired password-reset token should no longer be usable.

### Password validation

Tests cover the password requirements enforced by the application, including invalid passwords and mismatched password confirmation.

### Successful password change

A valid token combined with a valid new password should successfully change the user's password.

---

# TDD in Practice

One of the main goals of this project was to demonstrate the TDD cycle in practice.

## RED

Start by writing a test describing behaviour that does not exist yet.

For example:

```python
def test_existing_user_receives_reset_email():
    ...
```

Initially, the test fails.

This is the **RED** stage.

```text
Test
 ↓
FAIL
 ↓
RED
```

---

## GREEN

Implement the minimum amount of functionality necessary to make the test pass.

```text
RED
 ↓
Implement
 ↓
PASS
 ↓
GREEN
```

The objective at this stage is not to create perfect code.

The objective is simply to satisfy the behaviour described by the test.

---

## REFACTOR

Once the test passes, improve the implementation without changing its behaviour.

For example, password-reset functionality can be separated into services:

```text
views.py
    ↓
services.py
    ↓
Django authentication / email functionality
```

The tests should continue passing after the refactor.

The overall TDD cycle becomes:

```text
       ┌──────────────┐
       │              ▼
     RED → GREEN → REFACTOR
       ▲              │
       └──────────────┘
```

---

# Factory Boy

Factory Boy is used to create test users without repeatedly writing database setup code such as:

```python
User.objects.create_user(...)
```

Instead, tests can create users through a factory:

```python
user = UserFactory(
    email="test@example.com"
)
```

This makes tests:

* Easier to read
* Less repetitive
* Easier to maintain
* More consistent

Factories also make it easier to create different test scenarios.

For example:

```python
user = UserFactory()
```

or:

```python
user = UserFactory(
    email="existing@example.com"
)
```

---

#  Mocking and Patching

The application sends password-reset emails, but automated tests should not depend on an actual email provider.

Instead, the email service is mocked.

This allows a test to verify:

> Was the email service called correctly?

without actually sending an email.

For example:

```python
mocker.patch(
    "my_tdd.views.send_reset_email"
)
```

The test can then verify:

```python
mock_send_reset_email.assert_called_once()
```

This demonstrates an important testing principle:

> External dependencies should generally be isolated from automated tests.

Mocking is particularly useful for:

* Email services
* APIs
* External services
* Payment providers
* Notifications
* Other side effects

---

#  Project Structure

The project is organized approximately as follows:

```text
TDDproject/
│
├── manage.py
├── requirements.txt
├── build.sh
├── .python-version
├── pytest.ini
├── .gitignore
│
├── tdd_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
└── my_tdd/
    ├── __init__.py
    ├── views.py
    ├── forms.py
    ├── services.py
    ├── urls.py
    │
    ├── templates/
    │   └── ...
    │
    └── tests/
        ├── ...
        └── ...
```

---

#  Technologies

| Technology    | Purpose                    |
| ------------- | -------------------------- |
| Python        | Programming language       |
| Django        | Web framework              |
| PostgreSQL    | Production database        |
| pytest        | Testing framework          |
| pytest-django | Django testing integration |
| Factory Boy   | Test data factories        |
| pytest-mock   | Mocking and patching       |
| WhiteNoise    | Static file serving        |
| Gunicorn      | Production WSGI server     |
| Render        | Deployment platform        |
| Git           | Version control            |
| GitHub        | Source code hosting        |

---

# 💻 Running Locally

## Prerequisites

* Python 3.14.6
* Git

---

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY
cd YOUR_PROJECT_DIRECTORY
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 4. Run migrations

```bash
python manage.py migrate
```

---

## 5. Run the tests

```bash
python -m pytest -v
```

---

## 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

The root URL redirects to:

```text
/password-reset/
```

---

# Email in Development

During development, the project can use Django's console email backend.

Instead of sending an actual email, Django prints the email contents to the terminal.

This makes it possible to test the password-reset flow locally without configuring an external email provider.

For example, Django may output something similar to:

```text
Use the following link to reset your password:

http://127.0.0.1:8000/password-reset/Mg/<token>/
```

In production, a real email provider should be configured.

---

#  Deployment

The application is deployed using **Render**.

The production architecture is:

```text
GitHub
   │
   ▼
Render Web Service
   │
   ├── Django
   ├── Gunicorn
   └── WhiteNoise
   │
   ▼
PostgreSQL
```

The deployment uses a `build.sh` script.

The build process is:

```bash
pip install -r requirements.txt
./build.sh
```

The build script runs:

```bash
python manage.py collectstatic --no-input
python manage.py migrate
```

The application is started using:

```bash
gunicorn tdd_project.wsgi:application
```

---

#  Production Database

SQLite is used for local development.

Production uses PostgreSQL.

The application reads the production database configuration from:

```text
DATABASE_URL
```

This allows the same Django application to use different databases depending on the environment.

Conceptually:

```text
Local
 ↓
SQLite

Production
 ↓
PostgreSQL
```

---

#  Environment Variables

Production secrets should never be committed to GitHub.

The application uses environment variables for production configuration.

Important variables include:

```text
SECRET_KEY
DEBUG
DATABASE_URL
```

### SECRET_KEY

The production Django secret key is stored in Render's environment variables rather than in source control.

### DEBUG

Production should run with:

```text
DEBUG=False
```

### DATABASE_URL

Render provides the PostgreSQL connection URL through:

```text
DATABASE_URL
```

---

#  Python Version

The project uses:

```text
Python 3.14.6
```

The version is pinned using:

```text
.python-version
```

containing:

```text
3.14.6
```

Pinning the Python version helps keep the local development environment and production environment consistent.

---

#  Security Considerations

The password-reset workflow uses several security practices.

## Password-reset tokens

Django's built-in token generator is used rather than implementing a custom token system.

## Account enumeration

The application does not reveal whether an email address belongs to a registered account.

This prevents attackers from using the password-reset form to discover registered email addresses.

## Password validation

New passwords are validated before being saved.

## Secrets

Production secrets are stored as environment variables rather than committed to GitHub.

## HTTPS

The deployed application should be accessed over HTTPS in production.

---

## Deployment

The project also provided practical experience taking a Django application from:

```text
Local development
       ↓
Automated tests
       ↓
GitHub
       ↓
Render
       ↓
PostgreSQL
       ↓
Production
```
---

#  Key Commands

Run the development server:

```bash
python manage.py runserver
```

Run all tests:

```bash
python -m pytest -v
```

Run Django system checks:

```bash
python manage.py check
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Collect static files:

```bash
python manage.py collectstatic --no-input
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Update dependencies:

```bash
python -m pip freeze > requirements.txt
```

---
