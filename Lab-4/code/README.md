# Real-Time Simple Platformer Game

This project is a 2D platformer built using **Pygame**. It introduces students to interactive game design using object-oriented principles, real-time graphical rendering, continuous collision detection, physics tuning, and audio synthesis.

---

## What’s Provided & Completed

A fully functional version of the platformer with:

- A player-controlled character with left/right movement (`A`/`D` or Arrow keys), gravity, and jumping (`W`, `Up`, or `Space`)
- Continuous swept vertical collision detection ensuring reliable platform landing at any velocity
- Dynamic hazards, scoring system, and goal checkpoint
- Real-time Game Over overlay screen displaying final score and best score
- Replay option with selectable difficulty modes (**Easy**, **Medium**, **Hard**)
- 8-bit procedural sound effects for jumping, reaching the goal, and game over
- Clean architecture with object-oriented modular design

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

---

## Tasks Completed

### Task 1: Refine Collision Detection (Completed)
- **Problem**: When falling from elevated platforms, high downward velocity caused the player's discrete rectangle step to completely bypass thin 14px platforms between consecutive frames (tunneling).
- **Resolution**:
  - Implemented continuous swept collision detection that tests the full vertical displacement interval `[old_bottom, new_bottom]` against platform top surfaces.
  - Added a terminal velocity cap (12.0 - 16.0 px/frame) to prevent unbounded acceleration.
  - Automatically snaps the player to `platform.y - player.height` with `vy = 0` and sets `on_ground = True`.

### Task 2: Implement Game Over Condition (Completed)
- **Problem**: Dying on hazards or falling off-screen simply printed a line to the terminal while leaving the screen frozen without any UI or response.
- **Resolution**:
  - Added a formal `GAME_OVER` state machine in `GameEngine`.
  - Created an in-game Game Over overlay rendering "GAME OVER", "Final Score", "Best Score", and keyboard prompts.

### Task 3: Add Replay Option & Difficulty Selection (Completed)
- **Problem**: No mechanism existed to restart without restarting the python process.
- **Resolution**:
  - Added replay options directly on the Game Over screen:
    - **[1] Easy**: Gravity `0.45`, Jump `-13.0`, Speed `4.5` (forgiving, floaty jump)
    - **[2] Medium**: Gravity `0.60`, Jump `-12.0`, Speed `4.0` (balanced classic physics)
    - **[3] Hard**: Gravity `0.85`, Jump `-11.5`, Speed `3.8` (heavy gravity, strict timing)
  - Press `[R]` or `[SPACE]` to replay with current difficulty, or `[Q]` / `[ESC]` to exit.

### Task 4: Add Sound Feedback (Completed)
- **Problem**: No audio feedback was present.
- **Resolution**:
  - Created `game/sounds.py` using procedural in-memory audio waveform synthesis (`math` and `struct`).
  - Synthesizes 8-bit square, saw, and sine waveforms for:
    - **Jump**: Rising square wave blip.
    - **Goal**: Melodic ascending sine wave chime.
    - **Death**: Descending sawtooth pitch buzz.
  - Requires **zero external sound asset files** and includes graceful fallbacks if no sound hardware is present.

---

## Folder Structure

```
44_simple-platformer/
├── main.py
├── requirements.txt
├── README.md
└── game/
    ├── __init__.py
    ├── game_engine.py
    ├── player.py
    ├── platform.py
    ├── hazard.py
    └── sounds.py
```

---

## Submission Checklist

- [x] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior (`Lab-4/before.mp4`)
- [x] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working (`Lab-4/after.mp4`)
- [x] The Chat/LLM chat history exported as a PDF and Word document (`Lab-4/Lab4_Chat_History_PES1UG24CS708.pdf` and `.docx`)