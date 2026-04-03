const API_PATH = "http://192.168.1.17:8000/";
function getCSRFToken() {
    let cookieValue = null;
    const name = "csrftoken";

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function toggleWishlist(productId, el = null) {

    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    if (!productId) {
        console.error("productId missing");
        return;
    }

    $.ajax({
        url: "/addOrRemoveWishlist",
        type: "POST",
        contentType: "application/json",
        headers: {
            "token": token,
            "X-CSRFToken": getCSRFToken()
        },
        data: JSON.stringify({ productId }),
        success: function () {

            // Called from wishlist page
            if (!el && typeof loadWishlist === "function") {
                loadWishlist();
                return;
            }

            // Called from product card
            $(el).toggleClass("active");
            $(el).find("i").toggleClass(
                "zmdi-favorite zmdi-favorite-outline"
            );
        },
        error: function (xhr) {
            console.error(xhr.responseText);
        }
    });
}
