# Anti-AFK Tool

A Python tool that prevents your computer from going to sleep by automatically moving the mouse when you've been inactive for more than 3 minutes.

## Features

- Monitors keyboard and mouse activity
- Detects when you've been away for 3+ minutes
- Automatically moves the mouse slightly to prevent sleep mode
- Moves mouse back to original position to avoid disruption
- Clean shutdown with Ctrl+C

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the tool:
```bash
python anti_afk.py
```

The tool will:
1. Start monitoring your keyboard and mouse activity
2. If you're inactive for 3 minutes, it will move your mouse slightly
3. Continue running until you press Ctrl+C to stop it

## How It Works

- The tool uses the `pynput` library to monitor mouse movements, clicks, scrolls, and keyboard presses
- When any activity is detected, it updates the "last activity" timestamp
- Every 30 seconds, it checks if you've been inactive for 3+ minutes
- If you have been inactive, it moves the mouse by 1-3 pixels and then moves it back
- This prevents your computer from entering sleep mode without disrupting your work

## Requirements

- Python 3.6+
- pynput library

## Notes

- On macOS, you may need to grant accessibility permissions to your terminal or Python
- The tool runs continuously until stopped with Ctrl+C
- Mouse movements are minimal and designed to be non-disruptive 