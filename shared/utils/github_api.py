"""
BoardWiki → GitHub API helper
Gebruik dit vanuit BoardWiki om:
  1. Tenant-bestanden aan te maken / bij te werken
  2. De deploy-workflow te triggeren
  3. De workflow-status op te vragen
"""

import base64
import httpx
from typing import Literal

GITHUB_API = "https://api.github.com"


class GitHubClient:
    def __init__(self, token: str, owner: str, repo: str):
        self.owner = owner
        self.repo  = repo
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    # ── Bestanden ──────────────────────────────────────────────────────

    async def upsert_file(self, path: str, content: str, message: str) -> dict:
        """Maak een bestand aan of update het (base64-encoded)."""
        url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/contents/{path}"

        # Haal huidige SHA op als het bestand al bestaat (vereist door GitHub)
        sha = None
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=self.headers)
            if r.status_code == 200:
                sha = r.json()["sha"]

        payload = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
        }
        if sha:
            payload["sha"] = sha

        async with httpx.AsyncClient() as client:
            r = await client.put(url, headers=self.headers, json=payload)
            r.raise_for_status()
            return r.json()

    async def upsert_tenant_files(self, tenant_id: str, files: list[dict]) -> list:
        """
        Verwerk meerdere bestanden voor een tenant in één aanroep.
        `files` is een lijst van {"path": "backend/app.py", "content": "..."}
        """
        results = []
        for f in files:
            full_path = f"tenants/{tenant_id}/{f['path']}"
            result = await self.upsert_file(
                path=full_path,
                content=f["content"],
                message=f"BoardWiki: update {f['path']} voor {tenant_id}",
            )
            results.append({"path": full_path, "status": "ok", "sha": result["content"]["sha"]})
        return results

    # ── Workflow ───────────────────────────────────────────────────────

    async def trigger_workflow(
        self,
        tenant_id: str,
        action: Literal["build", "test", "deploy", "build-test-deploy"] = "build-test-deploy",
        ref: str = "main",
    ) -> dict:
        """Trigger de deploy-workflow voor een specifieke tenant."""
        url = (
            f"{GITHUB_API}/repos/{self.owner}/{self.repo}"
            f"/actions/workflows/deploy-tenant.yml/dispatches"
        )
        payload = {
            "ref": ref,
            "inputs": {
                "tenant_id": tenant_id,
                "action": action,
            },
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(url, headers=self.headers, json=payload)
            r.raise_for_status()
        return {"triggered": True, "tenant_id": tenant_id, "action": action}

    async def get_latest_run(self, tenant_id: str) -> dict | None:
        """Haal de meest recente workflow-run op voor een tenant."""
        url = (
            f"{GITHUB_API}/repos/{self.owner}/{self.repo}"
            f"/actions/workflows/deploy-tenant.yml/runs"
        )
        params = {"per_page": 10}
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=self.headers, params=params)
            r.raise_for_status()
            runs = r.json().get("workflow_runs", [])

        # Filter op tenant_id in de inputs
        for run in runs:
            if run.get("inputs", {}).get("tenant_id") == tenant_id:
                return {
                    "run_id": run["id"],
                    "status": run["status"],        # queued | in_progress | completed
                    "conclusion": run["conclusion"], # success | failure | null
                    "url": run["html_url"],
                    "created_at": run["created_at"],
                }
        return None


# ── Gebruiksvoorbeeld ──────────────────────────────────────────────────
# from shared.utils.github_api import GitHubClient
#
# client = GitHubClient(
#     token="ghp_...",
#     owner="jouw-org",
#     repo="boardwiki-generated",
# )
#
# # 1. Bestanden uploaden
# await client.upsert_tenant_files("tenant-abc", [
#     {"path": "backend/app.py",          "content": "...gegenereerde code..."},
#     {"path": "backend/requirements.txt", "content": "..."},
#     {"path": "frontend/index.html",      "content": "..."},
#     {"path": "frontend/app.js",          "content": "..."},
#     {"path": "manifest.json",            "content": "..."},
# ])
#
# # 2. Workflow triggeren
# await client.trigger_workflow("tenant-abc", action="build-test-deploy")
#
# # 3. Status opvragen
# run = await client.get_latest_run("tenant-abc")
# print(run["status"], run["conclusion"])
