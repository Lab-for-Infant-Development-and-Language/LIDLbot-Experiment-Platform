let mediaRecorder; 
let audioChunks = []; 
let mediaStream;
let recordedAudioBlob = null;
let uploadCancelled = false;

initAudioRecording();

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.grammars = new (window.SpeechGrammarList || window.webkitSpeechGrammarList)();
recognition.lang = 'en-CA';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

const loader = document.getElementById('loader');
const micText = document.getElementById('mic-text');
const micIcon = document.getElementById('mic-icon');
const tutorial = document.getElementById('tutorial');
const tutorialText = document.getElementById('tutorial-text');
const spaceIcon = document.getElementById('space-icon');

document.addEventListener('keydown', handleKeyDown);
document.addEventListener('keyup', handleKeyUp);

const VoicebotStates = {
  START: start,
  LISTENING: listening,
  PROCESSING: processing,
  TALKING: talking,
  WAITING: waiting
}
let blockLength = trials.length;
let spokenWordsList = [];
let preloadedTrials = [];
let timers = [];
let VoicebotState;
let isSpaceKeyDown = false;
let isSoundDetected = false;

loadTrial(trialIndex);
setState(VoicebotStates.START);
recognition.start();

recognition.onstart = function (event) {
}

recognition.onend = function (event) {
  micIcon.classList.remove('mic-icon-pulse');
  recognition.start();
}

recognition.onsoundstart = function (event) {
  isSoundDetected = true;
  if (VoicebotState === VoicebotStates.LISTENING && isSoundDetected) {
    micIcon.classList.add('mic-icon-pulse');
  }
}

recognition.onsoundend = function (event) {
  isSoundDetected = false;
  micIcon.classList.remove('mic-icon-pulse');
}

recognition.onspeechstart = function (event) {
}

recognition.onresult = function (event) {
  const results = event.results;
  for (let i = 0; i < results.length; i++) {
    if (results[i].isFinal) {
      const transcript = results[i][0].transcript.trim();
      const words = transcript.split(/\s+/);
      spokenWordsList.push(...words);
    }
  }
}

function setState(state, ...args) {
  VoicebotState = state;
  VoicebotState(...args);
}

function start(micTextMessage, tutorialTextMessage) {
  if (trialIndex >= blockLength) {
    document.location.replace(nextUrl);
    return;
  }

  loader.classList.add('loader-hidden');
  micText.innerHTML = micTextMessage ? micTextMessage : 'Ready!';
  micText.classList.remove('loader-hidden');
  micIcon.classList.remove('mic-icon-on');
  micIcon.classList.remove('mic-icon-pulse');
  tutorial.classList.remove('tutorial-hidden');
  tutorialText.innerHTML = tutorialTextMessage ? tutorialTextMessage : 'Press and hold SPACE to activate voicebot.';
  spaceIcon.classList.remove('space-icon-hidden');
}

function listening() {
  loader.classList.add('loader-hidden');
  micText.classList.add('loader-hidden');
  micIcon.classList.add('mic-icon-on');
  tutorial.classList.add('tutorial-hidden');
  if (VoicebotState === VoicebotStates.LISTENING && isSoundDetected) {
    micIcon.classList.add('mic-icon-pulse');
  }
}

function processing() {
  loader.classList.remove('loader-hidden');
  micText.classList.add('loader-hidden');
  micIcon.classList.remove('mic-icon-on');
  micIcon.classList.remove('mic-icon-pulse');
  tutorial.classList.remove('tutorial-hidden');
  tutorialText.innerHTML = 'If you made a mistake, press ESC to cancel now.';

  let processingTime = (3 + Math.min(spokenWordsList.length, 20)) * 350;
  timers.push(setTimeout(() => {
    if (verifiedNotTrolling()) {
      setState(VoicebotStates.TALKING);
    } else {
      setState(VoicebotStates.START, '', 'Voice not detected, please try again.');
    }
  }, processingTime));
}

async function talking() {
  loader.classList.add('loader-hidden');
  micText.classList.add('loader-hidden');
  micIcon.classList.remove('mic-icon-on');
  micIcon.classList.add('mic-icon-orange');
  micIcon.classList.remove('mic-icon-pulse');
  tutorial.classList.add('tutorial-hidden');

  const trialResponseAudio = await preloadedTrials.shift();
  trialResponseAudio.play();
}

function waiting(micTextMessage) {
  loader.classList.add('loader-hidden');
  micText.innerHTML = micTextMessage ? micTextMessage : 'Please click "Next" on your prompts screen now.';
  micText.classList.remove('loader-hidden');
  micIcon.classList.remove('mic-icon-on');
  micIcon.classList.remove('mic-icon-orange');
  micIcon.classList.remove('mic-icon-pulse');
  tutorial.classList.remove('tutorial-hidden');
  tutorialText.innerHTML = '';
  spaceIcon.classList.add('space-icon-hidden');

  let seconds = 3;
  const countdownInterval = setInterval(() => {
    tutorialText.innerHTML = `${seconds}...`;
    if (--seconds < 0) {
      clearInterval(countdownInterval);
      loadTrial(++trialIndex);
      setState(VoicebotStates.START);
    }
  }, 1000);
}

function verifiedNotTrolling() {
  return spokenWordsList.length >= minWords;
}

function loadTrial(index) {
  if (0 <= index && index < blockLength) {
    const response = trials[index].responses.value
    let audio = new Audio(response);
    audio.addEventListener('ended', () => {
      setState(VoicebotStates.WAITING);
    });
    preloadedTrials.push(audio);
  }
}

function handleKeyDown(event) {
  if ([' '].includes(event.key) && !isSpaceKeyDown) {
    isSpaceKeyDown = true;
    startRecording();
    if (VoicebotState === VoicebotStates.START) {
      spokenWordsList = [];
      setState(VoicebotStates.LISTENING);
    }
  } else if (['Escape'].includes(event.key) && VoicebotState === VoicebotStates.PROCESSING) {
    cancelProcessing();
    for (let timer of timers) {
      clearTimeout(timer);
    }
    setState(VoicebotStates.START);
  }
}

function handleKeyUp(event) {
  if ([' '].includes(event.key)) {
    stopRecording();
    if (VoicebotState === VoicebotStates.START) {
      isSpaceKeyDown = false;
      setState(VoicebotStates.START, '', 'Press and <b>hold</b> SPACE to activate voicebot.');
    } else if (VoicebotState === VoicebotStates.LISTENING) {
      stopRecognitionTimer = setTimeout(() => {
        setState(VoicebotStates.PROCESSING);
        isSpaceKeyDown = false;
      }, 1000);
    }
  }
}

async function initAudioRecording() { 
  mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true }); 
  mediaRecorder = new MediaRecorder(mediaStream); 
  mediaRecorder.ondataavailable = (event) => { 
    if (event.data.size > 0) { audioChunks.push(event.data); } 
  }; 
  mediaRecorder.onstop = async () => { 
    recordedAudioBlob = new Blob(audioChunks, { type: 'audio/webm' }); 
    audioChunks = []; 
    if (uploadCancelled) {
      recordedAudioBlob = null;
      uploadCancelled = false;
      return;
    }
    await uploadRecording()
  }; 
}

function startRecording() { 
  recordedAudioBlob = null; 
  audioChunks = []; 
  if (mediaRecorder.state === 'inactive') { 
    mediaRecorder.start(); 
  } 
}

function stopRecording() { 
  if (mediaRecorder.state === 'recording') { 
    mediaRecorder.stop(); 
  } 
}

function cancelProcessing() {
  uploadCancelled = true;
  recordedAudioBlob = null;
  audioChunks = [];
}

async function uploadRecording() { 
  if (!recordedAudioBlob) { 
    console.warn('No recording available'); 
    return; 
  } 
  const formData = new FormData(); 
  formData.append('file', recordedAudioBlob, `${trialIndex}_${Date.now()}.webm`); 
  try { 
    const response = await fetch('/session/responses/save_audio', { method: 'POST', body: formData }); 
    const result = await response.json(); 
    console.log('Upload success:', result); 
  } catch (err) { 
    console.error('Upload failed:', err); 
  } 
}