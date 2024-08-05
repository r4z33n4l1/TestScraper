(function() {
    let seenImages = new Set();
    let stopScrolling = false;
    let scrollAmount = 1000; // Amount to scroll each time
    let totalCount = 0;
    let promotedCount = 0;
    let imageLimit = parseInt(prompt("How many images do you want to collect?"), 10);

    // Function to get a random delay between min and max milliseconds
    function getRandomDelay(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    // Function to stop the scrolling when "Escape" key is pressed
    window.addEventListener("keydown", function(event) {
        if (event.key === "Escape") {
            stopScrolling = true;
            console.log("Scrolling stopped by user.");
        }
    });

    // Function to scroll and collect images
    function scrollAndCollectImages() {
        // if (stopScrolling || (imageLimit && seenImages.size >= imageLimit)) return;
        if (stopScrolling || totalCount > imageLimit) return;
        // Scroll the page
        window.scrollBy(0, scrollAmount);

        // Find the main div
        let mainDiv = document.querySelector("div.vbI.XiG");
        if (!mainDiv) {
            console.log("Main div not found");
            stopScrolling = true;
            return;
        }

        // Find all nested divs
        let nestedDivs = mainDiv.querySelectorAll("div.Yl-.MIw.Hb7");

        nestedDivs.forEach((div, index) => {
            totalCount++;
            if (stopScrolling || totalCount > imageLimit) return;
            try {
                // Check if the div has aria-label="promotedby"
                let promotedLabel = div.querySelector('[aria-label="Promoted by"]');
                if (promotedLabel) {
                    promotedCount++;
                    let img = div.querySelector("img");
                    let imgSrc = img ? img.src : "No image found";
                    let link = div.querySelector("a");
                    let url = link ? link.href : "No URL found";
                    console.log(`Sponsored: ${promotedLabel.textContent}, Image: ${imgSrc}, URL: ${url}`);
                } else {
                    let img = div.querySelector("img");
                    let imgSrc = img.src;
                    if (!seenImages.has(imgSrc)) {
                        seenImages.add(imgSrc);
                        console.log(`Image ${index}: ${imgSrc}`);
                    }
                }
            } catch (e) {
                console.error(`Error extracting data from div at index ${index}: ${e}`);
            }
        });

        console.log(`Total divs processed: ${totalCount}`);
        console.log(`Total promoted divs: ${promotedCount}`);

        // Continue scrolling after a random delay
        let randomDelay = getRandomDelay(1500, 3000); // Delay between 1500ms and 3000ms
        setTimeout(scrollAndCollectImages, randomDelay);
    }

    // Start the scrolling and collecting process
    scrollAndCollectImages();
})();