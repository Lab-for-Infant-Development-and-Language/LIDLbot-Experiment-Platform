const textDisplay = document.getElementById('text-display');
const imageDisplay = document.getElementById('image-display');
const nextButton = document.getElementById('next-button');

nextButton.addEventListener('click', handleNextButtonClicked);
document.addEventListener('keydown', handleKeyPresses);

const PromptTypes = {
  TEXT: 'text',
  IMAGE: 'image',
  SURVEY: 'survey'
}

const blockLength = trials.length;

updatePrompt(trialIndex);
disableNextButtonTemporarily(2000);

function updatePrompt(index) {
  if (index >= blockLength) return;

  const prompt = trials[index].prompter;
  switch (prompt.type) {
    case PromptTypes.TEXT:
      textDisplay.textContent = prompt.value;
      textDisplay.classList.remove('hidden');
      imageDisplay.classList.add('hidden');
      break;
    case PromptTypes.IMAGE:
      imageDisplay.src = prompt.value;
      textDisplay.classList.add('hidden');
      imageDisplay.classList.remove('hidden');
      break;
    case PromptTypes.SURVEY:
      const currentUrl = new URL(window.location.href);
      const urlParts = currentUrl.pathname.split("/");
      const urlModuleIndex = parseInt(urlParts[3]);
      const urlTrialIndex = parseInt(urlParts[4]);
      const urlNextTrialIndex = urlTrialIndex + 1;
      const redirectUrl = encodeURIComponent(
        `${currentUrl.origin}/experiment/page/${urlModuleIndex}/${urlNextTrialIndex}`
      );
      window.location.href = `${prompt.value}?redirect_url=${redirectUrl}&sona_id=${sonaId}&participant_id=${participantId}`;
  }
}

function disableNextButtonTemporarily(duration) {
  nextButton.disabled = true;
  setTimeout(() => {
    nextButton.disabled = false;
  }, duration);
}

function handleNextButtonClicked() {
  if (nextButton.disabled) return;

  trialIndex++;

  if (trialIndex < blockLength) {
    updatePrompt(trialIndex);
    disableNextButtonTemporarily(2000);
  } else if (trialIndex === blockLength) {
    textDisplay.textContent = 'Finished! Click button to continue...';
    textDisplay.classList.remove('hidden');
    imageDisplay.classList.add('hidden');
    let audio = new Audio("/static/assets/audio/success.mp3");
    audio.play();
  } else {
    window.location.replace(nextUrl);
  }
}

function handleKeyPresses(event) {
  if (['ArrowRight', 'Enter'].includes(event.key)) {
    nextButton.click();
  }
}