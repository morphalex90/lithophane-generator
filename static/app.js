document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("upload_form");
    const fileInput = document.getElementById("file_input");
    const fileSummary = document.getElementById("file_summary");
    const submitBtn = document.getElementById("submit_btn");
    const status = document.getElementById("status");
    const resultSection = document.getElementById("result_section");
    const resultList = document.getElementById("result_list");

    // Reflect the current selection and enable/disable the submit button.
    fileInput.addEventListener("change", () => {
        const count = fileInput.files.length;
        if (count === 0) {
            fileSummary.textContent = "No files selected";
        } else if (count === 1) {
            fileSummary.textContent = fileInput.files[0].name;
        } else {
            fileSummary.textContent = `${count} files selected`;
        }
        submitBtn.disabled = count === 0;
    });

    function setLoading(isLoading) {
        form.classList.toggle("loading", isLoading);
        submitBtn.disabled = isLoading || fileInput.files.length === 0;
        fileInput.disabled = isLoading;
    }

    function showStatus(message, type) {
        status.textContent = message;
        status.className = `status ${type}`;
        status.hidden = false;
    }

    // Build a list of source images, each with download links for its STL(s).
    function renderResults(items) {
        resultList.replaceChildren();

        for (const item of items) {
            const li = document.createElement("li");

            const heading = document.createElement("div");
            heading.className = "result-source";
            heading.textContent = `${item.source} (${formatSize(item.size)})`;
            li.appendChild(heading);

            const links = document.createElement("div");
            links.className = "result-files";
            for (const file of item.files) {
                const a = document.createElement("a");
                a.href = file.url;
                a.textContent = file.name;
                a.setAttribute("download", "");
                links.appendChild(a);
            }
            li.appendChild(links);

            resultList.appendChild(li);
        }
    }

    function formatSize(bytes) {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const files = fileInput.files;
        if (files.length === 0) return;

        const formData = new FormData();
        for (const file of files) {
            formData.append("files", file);
        }

        const shape = form.querySelector('input[name="shape"]:checked').value;
        formData.append("shape", shape);

        setLoading(true);
        showStatus("Generating lithophanes… this may take a moment.", "loading");
        resultSection.hidden = true;

        try {
            const response = await fetch("/process", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }

            const data = await response.json();
            renderResults(data.items || []);
            resultSection.hidden = false;
            showStatus("Done! Your lithophanes are ready.", "success");
        } catch (error) {
            showStatus(`Something went wrong: ${error.message}`, "error");
        } finally {
            setLoading(false);
        }
    });
});
