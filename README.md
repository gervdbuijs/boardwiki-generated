# BoardWiki Generated Apps

Deze repository bevat door BoardWiki gegenereerde webapplicaties per tenant.
Code wordt automatisch gegenereerd via AI en beheerd via de BoardWiki API.

## Structuur

```
boardwiki-generated/
├── tenants/
│   └── {tenant-id}/
│       ├── backend/        # Python (FastAPI)
│       ├── frontend/       # Vanilla JavaScript
│       ├── manifest.json   # Tenant metadata
│       └── .env.example    # Benodigde environment variables
├── shared/
│   ├── utils/              # Gedeelde Python utilities
│   └── templates/          # Basis templates voor codegeneratie
└── .github/
    └── workflows/
        └── deploy-tenant.yml   # Parameterized CI/CD workflow
```

## Workflow triggeren (vanuit BoardWiki)

```bash
POST /repos/{owner}/boardwiki-generated/actions/workflows/deploy-tenant.yml/dispatches
{
  "ref": "main",
  "inputs": {
    "tenant_id": "tenant-abc",
    "action": "deploy"
  }
}
```

## Tenant toevoegen

Nieuwe tenants worden automatisch aangemaakt via de BoardWiki API.
Zie `shared/templates/` voor de basisstructuur.
