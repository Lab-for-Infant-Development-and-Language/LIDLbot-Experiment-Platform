let timers = [];
let clearable = false;
let numMessages = 0;

let fullTranscript = [];

addChatBubble('Ready!', false);

const msgBox = document.getElementById("msgbox");
const nextBtn = document.getElementById("next");

msgBox.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        submitMsg(true);
    }
});

function addChatBubble(msg, user) {
    numMessages += 1;

    fullTranscript.push({
        trial: trialIndex,
        role: user ? "user" : "bot",
        text: msg
    });

    const containerDiv = document.createElement("div");
    const msgDiv = document.createElement("div");
    const msgP = document.createElement("p");
    msgP.textContent = msg;
    msgP.className = "small mb-0";
    msgDiv.appendChild(msgP);

    const img = document.createElement("img");
    let imgSrc = user ? "/static/assets/images/avatar-user.webp" : "/static/assets/images/avatar-ai.webp";

    if (user) {
        containerDiv.className = "d-flex flex-row justify-content-end mb-4";
        msgDiv.className = "p-3 me-3 border";
        containerDiv.appendChild(msgDiv);
        containerDiv.appendChild(img);
    } else {
        containerDiv.className = "d-flex flex-row justify-content-start mb-4";
        msgDiv.className = "p-3 ms-3 border";
        containerDiv.appendChild(img);
        containerDiv.appendChild(msgDiv);
    }

    msgDiv.style.cssText = "border-radius:15px;background-color:#fbfbfb;";
    img.style.cssText = "width:45px; height:100%;";
    img.src = imgSrc;
    document.getElementById("chat").appendChild(containerDiv);
}

function showTyping(user) {
    const containerDiv = document.createElement("div");
    const msgDiv = document.createElement("div");
    const bubbles = document.createElement("div");
    bubbles.className = "dot-flashing small";
    msgDiv.appendChild(bubbles);

    const img = document.createElement("img");
    let imgSrc = user ? "/static/assets/images/avatar-user.webp" : "/static/assets/images/avatar-ai.webp";

    if (user) {
        containerDiv.className = "d-flex flex-row justify-content-end mb-4";
        msgDiv.className = "p-3 me-3 border stage";
        containerDiv.appendChild(msgDiv);
        containerDiv.appendChild(img);
    } else {
        containerDiv.className = "d-flex flex-row justify-content-start mb-4";
        msgDiv.className = "p-4 ms-3 border";
        containerDiv.appendChild(img);
        containerDiv.appendChild(msgDiv);
    }

    containerDiv.id = "typing";
    msgDiv.style.cssText = "border-radius:15px;background-color:#fbfbfb;";
    img.style.cssText = "width:45px; height:100%;";
    img.src = imgSrc;
    document.getElementById("chat").appendChild(containerDiv);
}

function lockInput() {
    msgBox.disabled = true;
    document.getElementById("submit").disabled = true;
}
function unlockInput() {
    msgBox.disabled = false;
    document.getElementById("submit").disabled = false;
}

function removeLastMsg() {
    const chat = document.getElementById("chat");
    if (chat.lastChild) chat.removeChild(chat.lastChild);
}

async function submitMsg(buttonPressed) {
    const msg = msgBox.value.trim();
    if (!msg) return;
    if (!buttonPressed && window.event?.key !== "Enter") return;
    if (msgBox.disabled) return;

    const words = msg.split(/\s+/).length;
    if (words < minWords) {
        msgBox.value = "";
        alert(`Please type at least ${minWords} word(s)!`);
        return;
    }

    lockInput();
    addChatBubble(msg, true);
    msgBox.value = "";
    msgBox.placeholder = "Processing…";

    showTyping(false);

    const responseText = trials[trialIndex]?.responses?.value || "Sorry, I didn't understand that.";
    const processingTime = (3 + Math.min(words, 13)) * 400;

    timers.push(setTimeout(() => {
        const typing = document.getElementById("typing");
        if (typing) typing.remove();

        addChatBubble(responseText, false);
        trialIndex++;

        if (trialIndex >= trials.length) {
            lockInput();
            msgBox.placeholder = "Chat complete. Click Next to continue.";
            uploadFullTranscript();
            nextBtn.classList.remove("hidden");
        } else {
            let countdown = 3;
            const countdownInterval = setInterval(() => {
                msgBox.placeholder = `Clearing in ${countdown}...`;
                if (--countdown < 0) {
                    clearInterval(countdownInterval);
                    clearChatAndReset();
                }
            }, 1000);
        }
    }, processingTime));
}

function clearChatAndReset() {
    for (let i = 0; i < numMessages; i++) removeLastMsg();
    numMessages = 0;
    unlockInput();
    msgBox.placeholder = "Send message";
    addChatBubble('Ready!', false);
}

nextBtn.addEventListener('click', () => {
    window.location.replace(nextUrl);
});

function buildFullTranscriptFile() {
    let output = "";

    let currentTrial = null;
    for (const entry of fullTranscript) {
        if (entry.trial !== currentTrial) {
            currentTrial = entry.trial;
            output += `\n=== TRIAL ${currentTrial} ===\n`;
        }
        output += `${entry.role.toUpperCase()}: ${entry.text}\n`;
    }
    return output.trim();
}

async function uploadFullTranscript() {
    const text = buildFullTranscriptFile();

    const blob = new Blob([text], { type: "text/plain" });

    const formData = new FormData();

    formData.append(
        "file",
        blob,
        `${Date.now()}.txt`
    );

    await fetch("/session/responses/save_transcript", {
        method: "POST",
        body: formData
    });
}