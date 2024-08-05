    (function() {
        let seenImages = new Set();
        let stopScrolling = false;
        let scrollDelay = 3000;  // Delay between scrolls in milliseconds
        let scrollAmount = 500; // Amount to scroll each time
        let totalCount = 0;
        let promotedCount = 0;

        function scrollAndCollectImages() {
            if (stopScrolling) {
                console.log("Scrolling stopped.");
                return;
            }

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
                try {
                    // Check if the div has aria-label="promotedby"
                    let promotedLabel = div.querySelector('[aria-label="promotedby"]');
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

            // Continue scrolling after a delay
            setTimeout(scrollAndCollectImages, scrollDelay);
        }

        // Start the scrolling and collecting process
        scrollAndCollectImages();

        // Expose stopScrolling to the global scope so it can be set to true from the console
        window.stopScrolling = function() {
            stopScrolling = true;
        };

        console.log("Script is running. To stop it, type stopScrolling() in the console.");
    })();
