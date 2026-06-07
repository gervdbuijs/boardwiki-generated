// BoardWiki gegenereerde frontend voor: tenant-example
// Backend URL wordt ingesteld via config.js (gegenereerd bij deployment)
const API_BASE = window.BOARDWIKI_CONFIG?.apiUrl ?? "http://localhost:8000";

async function fetchItems() {
  const list = document.getElementById("items-list");
  try {
    const res = await fetch(`${API_BASE}/items`);
    const items = await res.json();

    if (items.length === 0) {
      list.innerHTML = "<p>Nog geen items.</p>";
      return;
    }

    list.innerHTML = items
      .map(item => `
        <div class="item" data-id="${item._id}">
          <strong>${item.name}</strong>
          ${item.description ? `<span>${item.description}</span>` : ""}
          <button onclick="deleteItem('${item._id}')">✕</button>
        </div>`)
      .join("");
  } catch (err) {
    list.innerHTML = `<p class="error">Kon items niet laden: ${err.message}</p>`;
  }
}

async function deleteItem(id) {
  await fetch(`${API_BASE}/items/${id}`, { method: "DELETE" });
  fetchItems();
}

document.getElementById("add-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("item-name").value.trim();
  const description = document.getElementById("item-desc").value.trim();

  await fetch(`${API_BASE}/items`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, description }),
  });

  e.target.reset();
  fetchItems();
});

// Initieel laden
fetchItems();
