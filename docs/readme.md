This is a project based on Django Rest Framework and React Js named QuickFood which is a online food delivery system.

Project Structure:
QuickFood/
├── backend/
│   ├── apps/
│   │   ├── __init__.py
│   │   ├── accounts/
│   │   ├── restaurants/
│   │   ├── orders/
│   │   ├── payments/
│   │   ├── ratings/
│   │   └── common/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   │   └── testing.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/ #react client site 
├── docs/
│   ├── api-documentation.md
│   ├── features-list.md
│   ├── role-based-permissions.md
│   ├── database-erd.md
│   └── readme.md
├── .env.example
└── .gitignore