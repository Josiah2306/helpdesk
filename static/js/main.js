// Auto scroll comments to latest
$(document).ready(function () {
    let comments = document.getElementById("comment-section");
    if (comments) {
        comments.scrollTop = comments.scrollHeight;
    }
});

// Confirmation dialog on logout
$(document).on("click", ".logout-btn", function (e) {
    if (!confirm("Are you sure you want to log out?")) {
        e.preventDefault();
    }
});
