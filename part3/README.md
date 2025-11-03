part3/
├── app/
│   ├── __init__.py          ← starts the app: loads settings, starts tools, plugs in routes
│   └── extensions.py        ← shared tools: database, migrations, passwords, jwt, restx api
├── presentation/            ← http endpoints (restx namespaces)
│   ├── users.py             ← /users routes
│   ├── places.py            ← /places routes
│   ├── amenities.py         ← /amenities routes
│   ├── reviews.py           ← /reviews routes
│   └── auth.py              ← /auth routes (login, me)
├── business/                ← core rules/helpers (e.g., password check)
│   └── user.py              ← user logic (hash/verify)
├── persistence/             ← data access (in-memory now, db later)
│   ├── repository.py        ← repo class: get/save/update
│   └── user_storage.py      ← one shared repo instance for all routes
├── config.py                ← dev/prod settings (db uri, jwt secret)
├── requirements.txt         ← python packages to install
└── sql/                     ← sql files (schema, seed) coming soon
