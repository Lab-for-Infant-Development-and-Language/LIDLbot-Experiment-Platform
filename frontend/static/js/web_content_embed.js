document.addEventListener('DOMContentLoaded', () => {
  const nextButton = document.getElementById('next-button');
  const timerEl = document.getElementById('timer');
  const msgEl = document.getElementById('msg');

  nextButton.classList.add('hidden');
  timerEl.classList.add('hidden');
  msgEl.classList.add('hidden');

  function showControls() {
    nextButton.classList.remove('hidden');
    timerEl.classList.remove('hidden');
    msgEl.classList.remove('hidden');
  }

  function enableNextButton() {
    nextButton.addEventListener('click', () => {
      window.location.replace(nextUrl);
    });
  }

  function setupAutoAdvance() {
    if (autoAdvanceTimeout !== null) {
      setTimeout(() => {
        window.location.replace(nextUrl);
      }, autoAdvanceTimeout * 1000);
    }
  }

  function startFlow() {
    showControls();
    enableNextButton();
    setupAutoAdvance();
  }

  if (buttonRevealTimeout !== null) {
    setTimeout(startFlow, buttonRevealTimeout * 1000);
  } else {
    startFlow();
  }
});