// Initialize the URL for the AJAX requests
document.getElementById("finalize-order-btn").addEventListener("click", () => {
    fetch(finalizeOrderUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest", // Identify as an AJAX request
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                // Remove the finalized order from the list in the UI
                document.getElementById("current-order-list").innerHTML = ""; // Clear the order list
                window.location.href = data.redirect_url; // Redirect to the orders page
            } else {
                alert(data.message); // Display any error messages
            }
        })
        .catch((error) => console.error("Error:", error));
});
