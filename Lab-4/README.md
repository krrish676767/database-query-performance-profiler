# Lab 4: VibeCoding & LLM-Driven Game Engineering

## Student Information
- **Name:** Krrish P Raju
- **SRN:** PES1UG24CS708
- **Course:** UE23CS352B - Software Engineering Lab
- **Assigned Problem:** #44 Simple Platformer (`SETAPESU26/44_simple-platformer`)
- **Pair-Programming Tool:** AI Assistant (Gemini / Claude Vibe Coding Session)

---

## Deliverables in this Directory

| Deliverable File | Description | Verification / Status |
| :--- | :--- | :--- |
| 🎥 [`before.mp4`](./before.mp4) | **10-Second Pre-Fix Gameplay Video** | Captures the original broken collision behavior (player falling through platform after elevated drop) and the frozen game state on death. (600 frames, 60.0 fps, 10.00s) |
| 🎥 [`after.mp4`](./after.mp4) | **10-Second Post-Fix Gameplay Video** | Demonstrates rock-solid continuous collision landing, goal scoring, death sequence, the Game Over UI, and replaying on Easy difficulty mode. (600 frames, 60.0 fps, 10.00s) |
| 📄 [`Lab4_Chat_History_PES1UG24CS708.pdf`](./Lab4_Chat_History_PES1UG24CS708.pdf) | **Exported Chat History (PDF)** | Professional 2-page document containing the prompt-driven vibe coding dialogue, defect isolation steps, and deliverables verification matrix. |
| 📝 [`Lab4_Chat_History_PES1UG24CS708.docx`](./Lab4_Chat_History_PES1UG24CS708.docx) | **Exported Chat History (Word DOCX)** | Complete editable Word document of the prompt-driven debugging transcript. |
| 💻 [`code/`](./code) | **Updated Platformer Codebase** | Contains the complete Python/Pygame source code with all 4 tasks implemented. |

---

## Bugs Identified and Resolved

### 1. Bug 1: Platform Tunneling / Discrete Collision Failure (Task 1)
- **Problem**: When falling from the elevated platform (`y = 400`), vertical acceleration grew unbounded under gravity (`vy > 16 px/frame`). Because platforms are only 14 pixels thick and the engine evaluated collisions discretely *after* applying `player.y += player.vy`, the player completely skipped past the platform's bounding box between consecutive frames without overlapping.
- **Solution**:
  - Implemented **Continuous Swept Collision Detection**: The engine evaluates whether the vertical displacement interval `[old_bottom, new_bottom]` intersected the platform surface `platform.y` while horizontally aligned.
  - Implemented **Terminal Velocity Capping** (12.0 - 16.0 px/frame depending on difficulty) to stabilize kinematics.
  - Corrected landing snap logic to position `player.y = platform.y - player.height` with `vy = 0` and `on_ground = True`.

### 2. Bug 2: Unhandled Game Over State & Permanent Window Freeze (Task 2)
- **Problem**: When falling into the void or touching the red hazard, the engine set `game_over = True`, printed a single line to stdout (`Game over! Final score: X`), and halted `update()`. The window froze on the death frame with no visual indicator or restart functionality.
- **Solution**:
  - Implemented an explicit state machine: `self.state = "PLAYING" | "GAME_OVER"`.
  - Created a real-time Game Over overlay with a dark semi-transparent backdrop, dialogue panel, final score display, high score tracking, and keyboard prompts.

---

## Features Implemented

### Task 3: Replay Option & Dynamic Difficulty Selection
- Implemented `DIFFICULTIES` configuration presets:
  - **Easy**: Gravity `0.45`, Jump `-13.0`, Speed `4.5` (forgiving, floaty jump)
  - **Medium**: Gravity `0.60`, Jump `-12.0`, Speed `4.0` (balanced classic physics)
  - **Hard**: Gravity `0.85`, Jump `-11.5`, Speed `3.8` (heavy gravity, strict timing)
- Interactive keyboard shortcuts during Game Over:
  - Press `[1]` / `[E]` for Easy mode
  - Press `[2]` / `[M]` for Medium mode
  - Press `[3]` / `[H]` for Hard mode
  - Press `[R]` or `[SPACE]` to replay current difficulty
  - Press `[Q]` or `[ESC]` to exit

### Task 4: In-Memory Procedural Sound Feedback
- Created `game/sounds.py` using pure mathematical waveform synthesis (`math` and `struct` modules) to produce 16-bit PCM RIFF WAV audio directly in memory:
  - **Jump**: Rising square wave sweep (260 Hz → 640 Hz) with sharp exponential decay.
  - **Goal Reached**: Melodic ascending sine wave arpeggio (480 Hz → 960 Hz).
  - **Death / Game Over**: Descending sawtooth pitch drop (340 Hz → 75 Hz).
- Zero external audio files required, ensuring guaranteed cross-platform compatibility and zero missing asset crashes.

---

## How to Run the Updated Game

```bash
cd code
pip install -r requirements.txt
python main.py
```

### Controls:
- **Move:** `A` / `D` or `Left` / `Right` Arrow keys
- **Jump:** `W`, `Up` Arrow, or `Spacebar`
- **Replay / Select Difficulty (on Game Over):** `1` (Easy), `2` (Medium), `3` (Hard), `R` (Replay), `Q` (Quit)
