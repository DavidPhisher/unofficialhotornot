document.addEventListener("DOMContentLoaded", () => {
    const imagesContainer = document.querySelector(".images-container");

    imagesContainer.addEventListener("click", async (event) => {
        const selectedImage = event.target.closest(".image");
        if (selectedImage) {
            const winnerId = selectedImage.getAttribute("data-id");

            try {
                const response = await fetch("/vote", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ winner_id: winnerId })
                });

                const data = await response.json();
                updateImages(data.images);
            } catch (error) {
                console.error("Error:", error);
            }
        }
    });

    function updateImages(images) {
        imagesContainer.children[0].setAttribute("data-id", images[0][0]);
        imagesContainer.children[0].querySelector("img").src = images[0][1];
        imagesContainer.children[0].querySelector(".vote").textContent = images[0][2];

        imagesContainer.children[1].setAttribute("data-id", images[1][0]);
        imagesContainer.children[1].querySelector("img").src = images[1][1];
        imagesContainer.children[1].querySelector(".vote").textContent = images[1][2];
    }
});
