(function () {
    const BLOCK_ID = "O638e52097da7d6e6867d7974_eI7d50e0ecffb64633aeb1d730f0cbd529";

    function createLayout() {
        const container = document.createElement("div");
        container.id = "boardwiki-welcome-container";
        container.style.maxWidth = "700px";
        container.style.margin = "40px auto";
        container.style.padding = "24px";
        container.style.fontFamily = "Arial, Helvetica, sans-serif";
        container.style.borderRadius = "8px";
        container.style.boxShadow = "0 2px 8px rgba(0,0,0,0.1)";
        container.style.backgroundColor = "#ffffff";

        const title = document.createElement("h1");
        title.textContent = "BoardWiki Client Web Function Page";
        title.style.textAlign = "center";
        title.style.color = "#2c3e50";
        title.style.fontSize = "1.6em";

        const message = document.createElement("p");
        message.id = "boardwiki-welcome-message";
        message.style.fontSize = "1.05em";
        message.style.lineHeight = "1.5";
        message.style.color = "#333333";
        message.style.textAlign = "center";
        message.textContent = "Loading welcome message...";

        const linksHeading = document.createElement("h2");
        linksHeading.textContent = "Available Functions";
        linksHeading.style.fontSize = "1.1em";
        linksHeading.style.color = "#2c3e50";
        linksHeading.style.marginTop = "24px";

        const linksList = document.createElement("ul");
        linksList.id = "boardwiki-function-links";
        linksList.style.listStyle = "none";
        linksList.style.padding = "0";
        linksList.style.textAlign = "center";

        const emptyItem = document.createElement("li");
        emptyItem.textContent = "No functions available yet.";
        emptyItem.style.color = "#777777";
        linksList.appendChild(emptyItem);

        container.appendChild(title);
        container.appendChild(message);
        container.appendChild(linksHeading);
        container.appendChild(linksList);

        return { container, message };
    }

    function fetchWelcomeMessage(messageEl) {
        fetch("/" + BLOCK_ID + "/message")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                messageEl.textContent = data.message;
            })
            .catch(() => {
                messageEl.textContent =
                    "Welcome at the BoardWiki Client Web function page. " +
                    "You will find links (buttons) to the functions that have been generated for you by BoardWiki.";
            });
    }

    function init() {
        const target = document.getElementById("boardwiki-app") || document.body;
        const { container, message } = createLayout();
        target.appendChild(container);
        fetchWelcomeMessage(message);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();