function handleStartButtonClick(event) {
    // Verify required fields
    let form = document.getElementById('experiment-settings-form');
    let formData = new FormData(form);

    let allRequiredFieldsFilled = true;
    let requiredFields = document.querySelectorAll('[data-required]');
    requiredFields.forEach(field => {
        let requiredAsterisk = field.querySelector('.required-asterisk');
        let formValue = formData.get(field.getAttribute('for'));
        if (formValue === '' || formValue === null) {
            requiredAsterisk.dataset.display = 'true';
            allRequiredFieldsFilled = false;
        } else {
            requiredAsterisk.dataset.display = 'false';
        }
    });
    
    if (!allRequiredFieldsFilled) {
        alert('Please fill out all required fields.');
        event.preventDefault();
        return false;
    }

    confirmSettings(event);
}

function confirmSettings(event) {
    let participantId = document.getElementById('participant-id').value;
    let participantIdWarning = document.getElementById('participant-id-warning');
    let nextParticipantId = document.getElementById('next-participant-id').textContent;
    let dryRun = document.getElementById('dry-run').checked;
    let bypassIdRestrictions = document.getElementById('bypass-id-restrictions').checked;

    participantIdWarning.dataset.display = 'false';
    // CAUTION: nextParticipantId is empty
    if (!bypassIdRestrictions && parseInt(participantId) !== parseInt(nextParticipantId)) {
        if (parseInt(participantId) < parseInt(nextParticipantId)) {
            // Show warning dialog for overwriting data
            if (!confirm("WARNING: You have entered a participant ID that has already been used. Continuing with this Participant ID will overwrite that participant's data files with this new one.")) {
                event.preventDefault();
                return false;
            }
        } else {
            // Show flag and message for invalid Participant ID
            participantIdWarning.dataset.display = 'true';
            alert("Invalid Participant ID. Check the Next Participant ID field, and try again.");
            event.preventDefault();
            return false;
        }
    }

    let sonaId = document.getElementById('sona-paid-id')?.value;
    let source = document.querySelector('input[name="source"]:checked').value;
    let condition = document.querySelector('input[name="condition"]:checked').value;
    let screen = document.querySelector('input[name="screen-selection"]:checked').value;
    let order = document.getElementById('counterbalance-order').value;

    // Create a div element
    let text = `
      Now Running:

      Participant ID: ${participantId}
      SONA/Paid ID: ${sonaId}
      Set: ${order}
      Source: ${source}
      Condition: ${condition}
      
      Screen: ${screen}
      Dry Run: ${dryRun}
      Bypass ID Restrictions: ${bypassIdRestrictions}

      Remember to fullscreen the app before starting!
      
      Proceed?
    `;

    // Pass the content of the div to the confirm dialog
    if (confirm(text)) {
        return true;
    } else {
        event.preventDefault();
        return false;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Fetch participant data from CSV
    fetch('/session/stats')
        .then(response => {
            return response.text();
        })
        .then(data => {
            // Parse CSV data
            Papa.parse(data, {
                header: true,
                dynamicTyping: true,
                complete: function (results) {
                    // Calculate required values
                    calculateValues(results.data);
                }
            });
        })
        .catch(error => console.error('Error fetching participant data:', error));

    function calculateValues(participantData) {
        const clean = (v) => (v === null || v === undefined) ? '' : String(v).trim();

        const lastRow = participantData[participantData.length - 2];
        const rawLastParticipantID = clean(lastRow?.participant_id);

        const parsedID = Number(rawLastParticipantID);
        const isValidLastParticipantID =
            rawLastParticipantID !== '' &&
            Number.isFinite(parsedID) &&
            parsedID >= 0;

        const lastParticipantID = isValidLastParticipantID ? parsedID : 0;
        const nextParticipantID = lastParticipantID + 1;
        const displayLastParticipantID = isValidLastParticipantID ? parsedID : '---';

        document.getElementById('last-used-participant-id').textContent = displayLastParticipantID;
        document.getElementById('next-participant-id').textContent = nextParticipantID;
    }
});
