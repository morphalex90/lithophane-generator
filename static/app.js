function uploadFiles() {
    const files = document.getElementById("file_input").files;

    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    fetch("/process", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = data.result;
    });
}
