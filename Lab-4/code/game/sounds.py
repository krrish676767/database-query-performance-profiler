"""
Sound manager module for Simple Platformer.
Generates procedural 8-bit retro sound effects dynamically using in-memory WAV synthesis.
Requires zero external asset files and gracefully falls back if audio devices are unavailable.
"""

import math
import struct
import io
import pygame

def _generate_wav_sound(freq_start, freq_end, duration, wave_type="square", decay=8.0, volume=12000):
    """Generates an in-memory pygame.mixer.Sound object using mathematical wave synthesis."""
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    raw_data = bytearray()
    phase = 0.0

    for i in range(n_samples):
        t = i / n_samples
        # Linear frequency modulation
        freq = freq_start + (freq_end - freq_start) * t
        phase += 2.0 * math.pi * freq / sample_rate

        if wave_type == "square":
            val = 1.0 if math.sin(phase) >= 0 else -1.0
        elif wave_type == "saw":
            val = 2.0 * (phase / (2.0 * math.pi) % 1.0) - 1.0
        elif wave_type == "triangle":
            val = 2.0 * abs(2.0 * (phase / (2.0 * math.pi) % 1.0) - 1.0) - 1.0
        else: # sine
            val = math.sin(phase)

        envelope = math.exp(-t * decay)
        sample = int(val * envelope * volume)
        clamped = max(-32767, min(32767, sample))
        raw_data.extend(struct.pack("<h", clamped))

    bio = io.BytesIO()
    # RIFF WAV header
    bio.write(b"RIFF")
    bio.write(struct.pack("<I", 36 + len(raw_data)))
    bio.write(b"WAVEfmt ")
    bio.write(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
    bio.write(b"data")
    bio.write(struct.pack("<I", len(raw_data)))
    bio.write(raw_data)
    bio.seek(0)

    try:
        return pygame.mixer.Sound(bio)
    except Exception:
        return None

class SoundManager:
    """Manages sound effects for player actions (jump, goal, death)."""
    def __init__(self):
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
        except Exception:
            self.enabled = False

        if self.enabled:
            # Task 4 sound effects
            self.jump_sound = _generate_wav_sound(freq_start=260, freq_end=640, duration=0.14, wave_type="square", decay=9.0)
            self.goal_sound = _generate_wav_sound(freq_start=480, freq_end=960, duration=0.35, wave_type="sine", decay=4.0, volume=15000)
            self.death_sound = _generate_wav_sound(freq_start=340, freq_end=75, duration=0.45, wave_type="saw", decay=5.0, volume=16000)
        else:
            self.jump_sound = None
            self.goal_sound = None
            self.death_sound = None

    def play_jump(self):
        if self.enabled and self.jump_sound:
            try:
                self.jump_sound.play()
            except Exception:
                pass

    def play_goal(self):
        if self.enabled and self.goal_sound:
            try:
                self.goal_sound.play()
            except Exception:
                pass

    def play_death(self):
        if self.enabled and self.death_sound:
            try:
                self.death_sound.play()
            except Exception:
                pass
