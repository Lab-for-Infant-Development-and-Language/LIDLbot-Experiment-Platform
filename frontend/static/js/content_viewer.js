const textDisplay = document.getElementById('text-display');
const imageDisplay = document.getElementById('image-display');
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');

let contentIndex = 0;
updateContent(contentIndex);
preloadImage(contentIndex + 1);

prevButton.addEventListener('click', decrementcontentIndex);
nextButton.addEventListener('click', incrementcontentIndex);
document.addEventListener('keydown', handleKeyPresses);


function updateContent(index) {
    if (contents.length === 0) {
        textDisplay.classList.add('hidden');
        imageDisplay.classList.add('hidden');
    } else if (0 <= index && index < contents.length) {
        switch (contents[index]["type"]) {
            case "image":
                imageDisplay.src = contents[index]["value"];
                textDisplay.classList.add('hidden');
                imageDisplay.classList.remove('hidden');
                break;
            case "text":
                textDisplay.textContent = contents[index]["value"];
                textDisplay.classList.remove('hidden');
                imageDisplay.classList.add('hidden');
        }
    }
}


function preloadImage(index) {
    if (0 <= index && index < contents.length) {
        if (contents[index]["type"] !== "image") return;
        const preloadedImage = new Image();
        preloadedImage.src = contents[index]["value"];
    }
}


function decrementcontentIndex() {
    contentIndex = Math.max(0, contentIndex - 1);
    if (contentIndex === 0) {
        prevButton.disabled = true;
    }
    updateContent(contentIndex);
    preloadImage(contentIndex - 1);
    preloadImage(contentIndex + 1);
}


function incrementcontentIndex() {
    contentIndex++;
    if (contentIndex >= contents.length) {
        nextButton.disabled = true;
        window.location.replace(nextUrl);
        return;
    }
    prevButton.disabled = false;
    updateContent(contentIndex);
    preloadImage(contentIndex - 1);
    preloadImage(contentIndex + 1);
}


function handleKeyPresses(event) {
    if (['ArrowLeft', 'Backspace'].includes(event.key)) prevButton.click();
    else if (['ArrowRight', 'Enter'].includes(event.key)) nextButton.click();
}