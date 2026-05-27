# LIDLbot

LIDLbot is an all-in-one experiment platform designed for psychological or linguistic experiments on conversational user interface interactions that require per-trial manipulations or measurements. LIDLbot features customizable modules and built-in voice agent and chatbot simulators to help researchers build streamlined experiments quickly. It offers benefits similar to Wizard-of-Oz setups, while not requiring live researcher administration of stimuli or responses.

# Table of Contents
- [Environment Setup](#Environment-Setup)
  - [Hardware Prerequisites](#Hardware-Prerequisites)
  - [Software Prerequisites](#Software-Prerequisites)
  - [Initialize Back-end Environment](#Initialize-Back-end-Environment)

- [Configuration](#Configuration)
  - [Experiment Configuration](#Experiment-Configuration)
  - [Set and Sequence Configuration](#Set-and-Sequence-Configuration)
  - [Module Configuration](#Module-Configuration)
  - [Block Configuration](#Block-Configuration)
  - [Trial Configuration](#Trial-Configuration)

- [Startup](#Startup)
    - [Session Setup](#Session-Setup)
      - [Participant Stats](#Participant-Stats)
      - [Participant Info](#Participant-Info)
      - [App Settings](#App-Settings)
      - [Launch Procedure](#Launch-Procedure)
 

# Environment Setup
The following section describes the necessary steps to set up the program source code.

## Hardware Prerequisites

- Two independent computers, minimum 4 GB of RAM, and 500 MB of free storage.

## Software Prerequisites

- Windows or MacOS
- Google Chrome
- Python (3.11 or later)
- Python Poetry (https://python-poetry.org/docs/)

## Initialize Back-end Environment

1. Open a terminal in the project root folder.
2. `cd backend` 
3. `poetry env activate`
<<<<<<< HEAD
4. `poetry install` (Note that `poetry install` is only required for the first time to install dependencies.)
=======
4. `poetry install`

Notes: 
- `poetry install` is only required for the first time to install dependencies.)
- If `poetry env activate` does not work, you will need to update poetry with `poetry self update`.
>>>>>>> a4e1f174a77f879927ecea7b2a63ecdac7b8256e


# Experiment Configuration

In LIDLbot, experiments are configured via an experiment folder. On program launch, researchers will be prompted to select a folder on their device, the contents of which define the experiment's flow and materials. For general use, no modifications to the source code are required.

The expected structure of the configuration folder is described below.

```
experiment_root/
├── participant_data/
│   ├── responses/
│   │   ├── voice/
│   │   └── chat/
│   ├── data.csv
│   └── participant.csv
├── resources/
│   ├── assets/
│   └── configuration/
│       ├── experiment_config.json
│       ├── sets_sequences_config.json
│       ├── modules_config.json
│       ├── blocks_config.json
│       └── trials_config/
```



| Name | Description |
|------|-------------|
| `experiment_root` | This is the root of the configuration folder. There are no restrictions on the folder name. |
| `participant_data` | Storage for experiment results. If not present, this folder will be created automatically (along with its contents). |
| `voice` | Storage for Participant responses to Voicebot Trials (audio recordings). |
| `chat` | Storage for Participant responses to Chatbot Trials (text files). |
| `data.csv` | A record of Trial orders and responses chosen by the system (main or alternative), on a per Participant basis. |
| `participant.csv` | A record of each Participant’s startup settings (Participant ID, set, chosen screen, etc.) as well as start and end timestamps. |
| `resources` | Storage for experiment resources. |
| `assets` | Storage for images and audio files. Although images and audio files may be placed anywhere within the configuration folder, a dedicated `assets` folder is recommended. |
| `configuration` | Storage for configuration files. |
| `experiment_config.json` | General experiment configuration. |
| `sets_sequences_config.json` | Definition of Sets and Sequences. |
| `modules_config.json` | Definition of Modules. |
| `blocks_config.json` | Definition of Blocks. |
| `trials_config` | A folder containing (potentially multiple) Trial configuration files. |


LIDLbot provides validation for the selected configuration folder and its files. It will ensure that the required files are present and that the configuration files follow the structure as described below. Detected errors will be logged in the program terminal output.


## experiment_config.json

In `experiment_config.json`, the experiment name is defined. For future iterations of the program, additional settings may also be described here.

A sample `experiment_config.json` entry is provided:

```json
{ "experiment_name": "Sample Experiment" }
```

## sequence_config.json

*Sets* are defined in `sets_sequences_config.json`. Each *Set* defines a *Sequence* for the *Assistant* screen and another Sequence for the *Study* screen.

A *Sequence is an ordered and non-empty list of custom *Modules* that determines the flow of the experiment.

A sample entry is provided:

```json
{
    "sample_set_1": {
        "assistant": [
            "sample_session_code_entry",
            "sample_voicebot_block_1"
        ],
        "study": [
            "sample_web_link",
            "sample_content_viewer",
            "sample_session_code_display",
            "sample_prompter_block_1",
            "sample_web_content_embed"
        ]
    },
}
```


## modules_config.json

In `modules_config.json`, custom modules are defined. 

Each Module must specify a valid template. 

| **Module Type** | **Module Name** | **Template Label** | **Description** |
| --- | --- | --- | --- |
| Static Modules | Content Viewer | `content_viewer` | Displays content such as images or text. Content will be displayed one at a time, and advanced with a Next button. Content displays sequentially in list order. |
|  | Web Survey | `web_link` | Displays a webpage in full screen, intended to be used for external survey hosting sites such as Qualtrics, Gorilla, or SurveyMonkey. Module will be advanced automatically after detecting the survey has been completed using page redirect logic (must also be configured on the survey website). |
|  | Web Embeds | `web_content_embed` | Displays embedded content from external web sources in a smaller window, such as videos, widgets, and/or games. Content can be advanced with a Next button or an automatic timer. |
| Gating Modules | Session Code Entry | `session_code_entry` | Gates Participant progression in the study by requiring a text string (Researcher-specified) acting as a password to proceed. |
|  | Session Code Display | `session_code_display` | Displays the text string required to proceed. |
| Block Modules | Prompter | `prompter` | Displays text, images, or survey URLs by Trials, defined by the Researcher in a Trials config `.json`. |
|  | Voicebot | `voicebot` | Built-in voice agent interface. The CUI accepts Participant voice input, which then triggers a premade audio response as specified by the Researcher in `trials_config.json`. |
|  | Chatbot | `chatbot` | Built-in chatbot interface. The CUI accepts Participant voice input, which then triggers a premade audio response as specified by the Researcher in `trials_config.json`. |

### Static Modules

Static Modules are different kinds of content displays. Broadly, they all involve specifying filepaths or URLs to be displayed. 

**Content Viewer**

A Content Viewer displays a series of text or images, primarily to be used for instructions for the Participant. The content displays sequentially as listed, requiring only a list of relative paths to the image files or the text string to be displayed. The Content Viewer comes with a `NEXT` and `PREVIOUS` button to allow the Participant to navigate between images/text. 

A sample entry is provided:
```json
"sample_content_viewer": {
    "template": "content_viewer",
    "contents": [
        { "type": "image", "value": "resources/assets/images/sample_cv/sample_cv_1.png" },
        { "type": "image", "value": "resources/assets/images/sample_cv/sample_cv_2.png" },
        { "type": "text", "value": "sample text instruction." }
    ]
}
```

![image.png](attachment:fe584bee-35a5-4be3-a0bf-7ade260c8ade:image.png)

**Web Survey**

A Web Survey is used to redirect users to an external webpage (e.g., Qualtrics). This can be used for surveys, questionnaires, and consent forms. To ensure the experiment can continue, the external page *must* be able to redirect users back to the program. 

To configure this, the Researcher specifies the URL of the external webpage. In the backend, LIDLbot will automatically append a query parameter `redirect_url` to the end of the specified one. The linked external web page should then use this parameter to redirect the user back after completion.

For example, in Qualtrics, first, add an `Embedded Data`Element (in the `Survey Flow`) with the parameter name `redirect_url` with a blank value. Then, add an `End of Survey` Element. Set it to use the `Redirect to URL` option, and then set the value to `${e://Field/redirect_url}`.

![image.png](attachment:204f6052-dd55-44dc-9644-b1ea91c7c5fe:image.png)

**Web Embed**

A Web Content Embed displays as an embedded view within the program. This is useful when additional control is needed, such as enforcing a timer. The `NEXT` button can be set to appear after a specified amount of time has passed. It can also be set to auto-advance to the next Module after a certain amount of time. 

From a configuration standpoint, a `web_content_embed` requires a URL. (Note that certain pages are not compatible with web embeds for security reasons. These sites can detect if they are in an embed and will not not allow it.)

To set the behaviour for the `NEXT` button, a value can be specified under `button_reveal_timeout`. The button will be revealed after the specified amount of seconds. If the value is `0`, then the button will immediately be revealed.

Similarly, `auto_advance_timeout` will set a countdown to auto-advance after the `NEXT` button appears. The Module will advance after the specified amount of seconds relative to the `NEXT` button appearance. However, if set to `null`, then it will not auto-advance at all.

![image.png](attachment:0cad9759-70bf-42f9-a674-06634a8a7f86:image.png)

### Block Modules

Block Modules are used for customizing the content and stimuli displayed during experimental blocks. Block Modules rely on specific logic to determine the count, selection, and randomization of Trials, which are specified by a Block. Block Modules follow a relationship of Block > Block Modules > Trial.

**Prompter**

A prompter displays text and/or image prompts. Configuration requires only the name of the trial block.

**Voicebot**

Voicebot receives audio input and replies with audio responses. Configuration requires only the name of the trial block.

**Chatbot**

Chatbot receives text input and replies with text output. Once again, configuration requires only the name of the trial block.

![image.png](attachment:e1fc8d0d-2535-435b-a5b4-d227391391d9:image.png)

Notice that the same Block should be specified for corresponding Prompter and Bot modules.

### Gating Modules

Gating Modules are used to “gate” a Participant’s progression. They prevent a Participant from initiating the Voicebot or Chatbot Modules before having reached the Prompter by requiring a passcode to continue. 

**Session Code Entry**

To be used on the Assistant Instance. A session code entry prompts the participant to enter a session code, and will only allow them to proceed if the code is correct. Configuration requires providing the expected session code.

**Session Code Display**

To be used on the Study Instance to display a session code. Configuration requires providing the code to display.

![image.png](attachment:35be6497-8bff-45f4-86c3-21a97db82c59:image.png)

## blocks_config.json

In `blocks_config.json`, Trial Blocks are defined. This determines how many Trials will be in a Block, of those, how many should present an alternative response as opposed to the main response, and whether or not the trials should be randomized. A Block draws its Trials from a pool. A pool is referenced by its name.

![image.png](attachment:9d0a98c0-06be-4edb-ba82-32417312087a:image.png)

## Trials .json

`trial_config` files may have any name and can be anywhere in the config folder (although keeping them with the rest of the configs (inside `resources/configuration`

Trial pools config is where individual trials are defined. For easier handling, trials are organized into groups, referred to as pools. In this example, we have two pools (though any number of pools is permitted).

Each trial must define a prompt (which may either be text or an image). This is determined by the “type” field as shown.

For a text prompt, the value is simply the desired text. For an image prompt, the value must be the relative file path to the image file (that is to say, relative to the configuration root folder).

Each trial must also define a response, the “type” may either be text or audio. A value must be provided for both the main response as well as the alternative response. Like image prompts, audio responses must be given as relative file paths to the audio file.

![image.png](attachment:9d2d0fc2-5b4c-4b3e-a8cd-58e17b73b6cc:image.png)


# Session Setup
 
## Startup

1. Open a terminal in the project root folder.
2. `cd backend` 
3. `poetry env activate`
<<<<<<< HEAD
4. `poetry run python run.py`
=======
4. `poetry run python app.py`
>>>>>>> a4e1f174a77f879927ecea7b2a63ecdac7b8256e
5. A file selection dialog will open. Select the experiment configuration folder. A successful validation looksl ike the code below.
    - The contents of the folder (configuration files and assets) will be validated. Validation logs are available in the console.
    - Should validation fail or should the user fail to select a folder, LIDLbot will terminate.

```
[INFO]: Starting LIDLbot...

=== Setup ===
[ACTN]: Please select the experiment configuration folder in the file dialog window.
[PASS]: Folder selected: C:\Users\---\sample-experiment.

[INFO]: Loading configuration files...
[PASS]: Configuration files loaded successfully.

[INFO]: Validating 'experiment_config.json'...
[PASS]: 'experiment_config.json' validated successfully.

[INFO]: Validating 'trial_pools_config.json'...
[PASS]: 'trial_pools_config.json' validated successfully.

[INFO]: Validating 'blocks_config.json'...
[PASS]: 'blocks_config.json' validated successfully.

[INFO]: Validating 'modules_config.json'...
[PASS]: 'modules_config.json' validated successfully.

[INFO]: Validating 'orders_config.json'...
[PASS]: 'orders_config.json' validated successfully.

=== Experiment ===
[INFO]: Initializing experiment...

[INFO]: Server running on http://127.0.0.1:56314.
[INFO]: Opened browser at http://127.0.0.1:56314/experiment/page/0.
```

1. On successful validation, LIDLbot will automatically launch in the default browser. Please ensure that Google Chrome is used; other browsers, like Firefox, may not support the required speech recognition module.
    1. The terminal output also provides the URL. If the browser fails to automatically open, or the default browser is not Google Chrome, copy and paste this URL into a Google Chrome tab.

## Session Setup

Once launched, LIDLbot begins at the Session Setup screen. 

![setup.png](attachment:ff518b02-1325-47e1-ade6-d7c4e9e74fd8:setup.png)

### Participant Stats

| **Label** | **Description** |
| --- | --- |
| Last Used Participant ID | Displays the Participant ID of the most recent previously recorded session. |
| Next Participant ID  | Displays the next Participant ID. By default, the Researcher should enter this value should into the Participant ID box unless they wish to test or overwrite the previously recorded entry. |
| Total Participant Counts | The total number of participants logged in the experiment. |

### Participant Info

| **Label** | **Description** |
| --- | --- |
| Participant ID | Participant ID. This is used to track participant sessions in recorids, and most importantly, determines the seed that generates the order of Trials. **This ID must match between both Instances, or else the Trials will not be synchronized.** |
| Secondary ID | This field is to be used for any secondary ID numbers that the Researcher may use, such as those from participant management systems like SONA. (Currently, this field is still required to launch a session, so if the Researcher does not need it, they can just enter a random number to continue.) |
| Set | The **Set** to be used for the session. (See Section 1.2 in paper.)  |

Info entered here is logged in a `participants.csv` file to as a record of past sessions. Future development is planned to enable customizability for adding extra participant info to be entered this section to be logged in `participant.csv`, such as Participant Group/Conditions. 

### App Settings

| **Label** | **Description** |
| --- | --- |
| Screen Selection | Used to select the Instance that will be displayed on the device. In typical usage, only one computer should display the Assistant Instance, and the other displays the Study Instance.  |
| Testing Modes (Dry Run) | Used for debugging and testing purposes. Allows the Researcher to run through a whole session without saving any participant data or input.  |
| Testing Modes (Bypass ID Restrictions) | Used for debugging and testing purposes. By default, the platform will not launch a session if the `Participant ID` field does not match the value provided by `Next Participant ID`.  Selecting this option overrides that behaviour. |

### Launch

The Researcher enters the Participant’s info. Then, the set may be selected, as well as the desired screen (either Assistant or Study). When ready, the Researcher clicks `Start`.

At this time, it is recommended to fullscreen the app to prevent distractions and improve immersion. Do this by pressing F11 (Windows) or clicking the Green window button (MacOS).

After clicking `Start`, an alert dialog will appear that lists the Participant ID number and other entered Participant Info. This appears so the Researcher can quickly check that information is entered correctly and matches between both Instances. Again, this is especially for the Participant ID and the Set, as mismatched entries will result in desynchronization.

Once the Researcher has verified the entries do match, clicking `OK` starts the experiment session.
