# GitHub Setup – Stap voor stap

## 1. Repo aanmaken

Ga naar github.com → New repository
- **Naam:** `boardwiki-generated`
- **Visibility:** Private (aanbevolen)
- **Initialize:** leeg laten (we pushen zelf)

```bash
git init
git remote add origin https://github.com/<jouw-org>/boardwiki-generated.git
git add .
git commit -m "Initial BoardWiki repo setup"
git push -u origin main
```

---

## 2. GitHub Pages inschakelen

Ga naar: `Settings → Pages`
- **Source:** `Deploy from a branch`
- **Branch:** `gh-pages` / `/ (root)`

Elke tenant krijgt zijn eigen URL:
`https://<org>.github.io/boardwiki-generated/tenants/<tenant-id>/`

---

## 3. GitHub Secrets instellen

Ga naar: `Settings → Secrets and variables → Actions`

Voeg toe:

| Secret naam              | Waarde                                      |
|--------------------------|---------------------------------------------|
| `MONGODB_URI`            | MongoDB Atlas connection string             |
| `RAILWAY_TOKEN`          | Token uit Railway dashboard                 |
| `BOARDWIKI_WEBHOOK_URL`  | URL van jouw BoardWiki webhook endpoint     |
| `BOARDWIKI_WEBHOOK_SECRET` | Willekeurige geheime string voor verificatie |

---

## 4. Personal Access Token (PAT) voor BoardWiki

BoardWiki heeft een token nodig om de GitHub API te kunnen aanroepen.

Ga naar: `github.com → Settings → Developer settings → Personal access tokens → Fine-grained tokens`

Stel in:
- **Repository access:** Alleen `boardwiki-generated`
- **Permissions:**
  - `Contents`: Read & Write (bestanden aanmaken/updaten)
  - `Actions`: Read & Write (workflows triggeren)
  - `Pages`: Read & Write (GitHub Pages)

Sla het token op als omgevingsvariabele in BoardWiki:
```
GITHUB_TOKEN=github_pat_...
GITHUB_OWNER=<jouw-org>
GITHUB_REPO=boardwiki-generated
```

---

## 5. Railway instellen voor backends

1. Ga naar [railway.app](https://railway.app) → New Project
2. Kies **Empty project**
3. Maak per tenant een service aan met naam `<tenant-id>-backend`
4. Koppel aan GitHub repo (automatische deploy uitschakelen – wij triggeren zelf)
5. Voeg environment variables toe per service (zie `.env.example`)

---

## 6. Testen

Trigger de workflow handmatig via GitHub UI:
`Actions → Build, Test & Deploy Tenant → Run workflow`

Vul in:
- `tenant_id`: `tenant-example`
- `action`: `build`

Of via de API (zie `shared/utils/github_api.py`).
