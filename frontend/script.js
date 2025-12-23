const BASE = "http://localhost:8000/";

// =========================================
// 1. PREVIEW BEFORE UPLOAD
// =========================================
function previewImages() {
    const preview = document.getElementById("preview");
    preview.innerHTML = "";

    const files = document.getElementById("images").files;

    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = document.createElement("img");
            img.src = e.target.result;
            img.className = "preview-img";
            preview.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
}


// =========================================
// 2. UPLOAD + LOADING ANIMATION
// =========================================
async function uploadImages() {
    const files = document.getElementById("images").files;

    if (files.length < 3) {
        alert("Please upload at least 3 images!");
        return;
    }

    const formData = new FormData();
    for (let f of files) formData.append("files", f);

    // SHOW LOADING ANIMATION
    document.getElementById("loading").style.display = "block";
    document.getElementById("result-section").classList.add("d-none");

    const res = await fetch(BASE + "api/hdr", {
        method: "POST",
        body: formData,
    });

    const data = await res.json();

    // HIDE LOADING AFTER DONE
    document.getElementById("loading").style.display = "none";
    document.getElementById("result-section").classList.remove("d-none");

    // SET RESULT IMAGES
    document.getElementById("hdr-img").src = BASE + data.hdr_result;
    document.getElementById("compare-img").src = BASE + data.compare;
    document.getElementById("hist-img").src = BASE + data.histogram;

    document.getElementById("download-link").href = BASE + data.hdr_result;
}
