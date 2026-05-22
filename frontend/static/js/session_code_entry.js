const submitButton = document.getElementById('submit-button');
const sessionCodeInput = document.getElementById('session-code-input');

submitButton.addEventListener('click', handleCodeInputSubmission);
sessionCodeInput.addEventListener('keypress', handleKeyPresses);

function handleCodeInputSubmission() {
    if (sessionCodeInput.value.trim() === code) {
        window.location.replace(nextUrl);
    } else {
        sessionCodeInput.value = ''
        alert('Please enter a valid session code.')
    }
}

function handleKeyPresses(event) {
    if (event.key === 'Enter') {
        submitButton.click();
    }
}