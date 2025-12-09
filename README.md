# 🎼 AI Music Composition Studio

This repository contains a prototype **AI-assisted music composition & arrangement tool** built with **Python + Streamlit**.  
It is designed as a final project for an "All-in-One Creation" style course, demonstrating:

- Generative structure design (melody, chords, multi-track arrangement)
- Data-driven mapping from mood/style parameters to musical patterns
- Interactive web-based creativity using Streamlit

> Note: The current version uses **simple rule-based and random generation** for music structure.  
> You can later replace these parts with real AI/ML models or more advanced music algorithms.

---

## ✨ Features

- **Composition Settings (Sidebar)**  
  - Mood: `Happy`, `Sad`, `Calm`, `Epic`, `Lo-fi`  
  - Style: `Pop`, `Cinematic`, `Game BGM`, `Lo-fi`, `Jazz`  
  - Tempo (BPM)  
  - Key (e.g., `C major`, `A minor`)  
  - Length in bars  
  - Arrangement template: `Pop Band`, `String Ensemble`, `8-bit Game`

- **AI-ish Music Generation (Prototype)**
  - Main melody generation (as a sequence of bars, beats, degrees, durations)
  - Chord progression per bar based on mood (e.g., I–V–vi–IV for happy pop)
  - Multi-instrument tracks:
    - `Lead` (melody line)
    - `Chords` (block chords per bar)
    - `Bass` (root-note pattern)
    - `Drums` (simple kick & snare pattern)

- **Interactive Visualization**
  - Display of configuration summary
  - Melody & chord progression as tables
  - Per-track data views via expanders:
    - Inspect each instrument’s bars, beats, and patterns

- **Future-ready Design**
  - Clear function boundaries:
    - `generate_melody(config)`
    - `generate_chords(config)`
    - `arrange_tracks(melody_df, chords_df, config)`
  - Easy to upgrade with:
    - AI models
    - MIDI/audio rendering
    - More complex arrangement logic

---

## 🧱 Project Structure

Currently, the project is a single-file Streamlit app:

```text
.
├── app.py           # Main Streamlit application
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
