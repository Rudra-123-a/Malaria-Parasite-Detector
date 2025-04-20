function uploadImage() {
    let fileInput = document.getElementById("fileInput");
    let resultText = document.getElementById("result-text");
    let previewImg = document.getElementById("preview-img");

    if (!fileInput.files.length) {
        alert("Please select an image first.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultText.innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
        } else {
            resultText.innerHTML = `<strong>Result:</strong> ${data.result}`;
            previewImg.src = URL.createObjectURL(fileInput.files[0]);
            previewImg.style.display = "block";
        }
    })
    .catch(error => {
        resultText.innerHTML = `<span style="color: red;">Error: ${error}</span>`;
    });
}
