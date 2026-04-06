# Feature Proposal: Native Soundpad Integration

## Proposal Overview
The majority of users utilizing the **MyInstants Downloader** (content creators, gamers, and "shitposters") generally download audio files with one ultimate goal in mind: playing them in their voice chats via **Soundpad** (Leppsoft).

This proposal aims to implement a direct, native integration between the downloader and Soundpad. This would entirely remove the friction of the current manual process (Download -> Open Soundpad -> Add File -> Right Click -> Assign Hotkey).

## Key Features

1. **Direct Download Routing:** 
   Users will be able to configure their official Soundpad audio directory. Upon clicking "Download" in the app's interface, the script will automatically bypass the generic `downloads/` folder and send the `.mp3` directly to their Soundpad directory.

2. **Automated Addition to Soundpad List:**
   Through remote communication, the downloader will notify Soundpad that a new file has been acquired. It will automatically add the meme sound to the active Soundpad library list, making it instantly playable without requiring the user to manually import it.

3. **In-App Hotkey Assignment:**
   When downloading a sound, the downloader UI (`components.py`) will display an optional input field: *"Assign Hotkey"*. The user can input their desired shortcut (e.g., `NumPad 4`), and the downloader will send a remote command binding the newly downloaded audio to that hotkey natively in Soundpad.

4. **Collision Warning System:**
   Before binding the audio to the requested hotkey, the script will query Soundpad's database. If the chosen key is already occupied by another sound, the downloader UI will display an alert: *"This hotkey is already assigned to the sound 'X'. Do you want to overwrite it?"*.

## Technical Implementation Suggestions (For Devs)
- **Soundpad Remote Control API:** Soundpad features a native Windows named pipe infrastructure designed specifically for remote commanding (`\\.\pipe\sp_remote_control`). 
- The Python backend of *MyInstants Downloader* can connect directly to this named pipe (or utilize community-made Python wrapper libraries available on GitHub).
- Required Soundpad API remote commands for this integration:
  - `DoAddSound(local_file_path)`
  - `DoGetSoundList()` (Used to check existing macros/hotkeys to validate collision).
  - Hotkey mapping bindings via basic RPC syntax.
