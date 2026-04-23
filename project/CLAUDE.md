# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run development server
python manage.py runserver

# Run Tailwind CSS watcher (required for styling changes)
python manage.py tailwind start

# Apply migrations
python manage.py migrate

# Create new migrations
python manage.py makemigrations

# Run tests
python manage.py test

# Run a single test
python manage.py test apps.users.tests

# Install dependencies (uses uv)
uv sync
```

**Environment setup**: Copy `.env.example` to `.env` and configure. The app defaults to SQLite; set `DB_ENGINE=postgres` and PostgreSQL credentials to use Postgres.

## Architecture

### Project Layout

```
config/          # Django settings, URLs, WSGI/ASGI
apps/            # Django applications (users, core, notifications, advanced_form)
templates/       # Global base template + reusable components
theme/           # django-tailwind app (Tailwind CSS build)
```

### Settings

`config/settings/` uses a split layout. `__init__.py` imports from `base.py`. Custom user model: `AUTH_USER_MODEL = 'users.User'`.

### Apps

- **users** — Custom `AbstractUser` model, registration/login/logout views
- **core** — Home page + `Service` abstract base class (`apps/core/interfaces.py`) used across apps
- **notifications** — Demonstrates Strategy + Factory patterns: `NotificationService` accepts a `Sender` (SMS or Email), selected via `get_sender(sender_type)` factory in `senders/__init__.py`
- **advanced_form** — `Product`, `ProductVolume` (OneToOne), `ProductInfo` (FK) models with a product listing page

### Templates

Global components live in `templates/components/` (alert, card_header, form_field, btn_submit, form_footer, nav_tab). App-specific templates live in `apps/<app>/templates/<app>/`. App-level components can override global ones.

Base template (`templates/base.html`) provides nav, auth links, and the `{% tailwind_css %}` tag.

### Design Patterns

The `Service` ABC in `apps/core/interfaces.py` defines an `execute()` method and `__call__` delegate — new business logic services should extend it. The notifications app shows the intended pattern: service + strategy + factory.
