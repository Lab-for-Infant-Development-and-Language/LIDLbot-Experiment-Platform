document.getElementById('next-button').addEventListener('click', handleNextButton);

setTimeout(unhideAll, 5000);

function unhideAll() {
    const hiddenElements = document.getElementsByClassName('hidden');
    for (let i = 0; i < hiddenElements.length; i++) {
        hiddenElements[i].classList.remove('hidden');
    }
}

function handleNextButton() {
    window.location.replace(nextUrl);
}