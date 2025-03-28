document.addEventListener("DOMContentLoaded", function() {
    const messageBox = document.getElementById("text");

    messageBox.addEventListener("focus", function() {
        this.dataset.placeholder = this.placeholder; // Store the placeholder text
        this.placeholder = ""; // Remove placeholder on focus
    });

    messageBox.addEventListener("blur", function() {
        if (this.value.trim() === "") {
            this.placeholder = this.dataset.placeholder; // Restore placeholder if empty
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const resultBox = document.getElementById("result");
    resultBox.style.height = "auto";  // Reset height to auto
    resultBox.style.height = resultBox.scrollHeight + "px";  // Set height based on content
});

document.addEventListener("DOMContentLoaded", function() {
    const messageBox = document.getElementById("text");
    const predictButton = document.getElementById("predictButton");

    const activeColor = "#a5dca5";

    predictButton.disabled = true;
    predictButton.style.backgroundColor = "#cacaca";
    predictButton.style.cursor = "not-allowed";

    function updateState() {
        let textLength = messageBox.value.length;
        charCount.textContent = `${textLength}/500`; // Update character count
    
        if (textLength > 0) {
            predictButton.style.backgroundColor = activeColor;
            predictButton.disabled = false;
            predictButton.style.cursor = "pointer";
        } else {
            predictButton.style.backgroundColor = "#cacaca"; // Gray when empty
            predictButton.disabled = true;
            predictButton.style.cursor = "not-allowed";
        }
    }

    // Attach event listener to track input changes
    messageBox.addEventListener("input", updateState);
});


const prediction = document.body.getAttribute("data-prediction").trim();
const body = document.getElementById("background");

if (prediction === "Spam") {
    body.style.backgroundImage = "url('static/img/spam_bg.jpg')"; // Replace with correct path
} else {
    body.style.backgroundImage = "url('static/img/ham_bg.jpg')"; // Replace with correct path
}
