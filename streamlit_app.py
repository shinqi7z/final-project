import streamlit as st
import pandas as pd
import random
import io
from fpdf import FPDF

# --------------------------------------
# 基础工具函数
# --------------------------------------

def build_scale(key: str, mode: str = "major"):
    """根据调性生成一个简单音阶（用数字 1-7 表示音级）"""
    # 这里只用 1–7，真正音高在后面用映射表决定
    if mode == "major":
        scale_degrees = [1, 2, 3, 4, 5, 6, 7]
    else:
        scale_degrees = [1, 2, 3, 4, 5, 6, 7]
    return scale_degrees


def choose_chord_progression(mood: str):
    """根据情绪选择一个简单和弦进行（用 I、V、vi 等罗马数字表示）"""
    progressions = {
        "Happy": [["I", "V", "vi", "IV"]],
        "Sad": [["vi", "IV", "I", "V"]],
        "Calm": [["I", "IV", "ii", "V"]],
        "Epic": [["i", "VI", "III", "VII"]],
        "Lo-fi": [["I", "iii", "vi", "IV"]],
    }
    return random.choice(progressions.get(mood, [["I", "V", "vi", "IV"]]))


def generate_melody(config):
    """
    生成主旋律（简单规则版）
    输出：DataFrame: bar, beat, degree, duration
    """
    num_bars = config["num_bars"]
    key = config["key"]
    mode = "major" if "major" in key else "minor"

    scale = build_scale(key, mode)
    rows = []

    # 简单规则：每小节 4 个八分音符（每个 0.5 拍）
    note_per_bar = 4
    for bar in range(1, num_bars + 1):
        for i in range(note_per_bar):
            degree = random.choice(scale)
            duration = 0.5
            beat = i * duration
            rows.append(
                {
                    "bar": bar,
                    "beat": beat,
                    "degree": int(degree),
                    "duration": duration,
                }
            )

    melody_df = pd.DataFrame(rows)
    return melody_df


def generate_chords(config):
    """
    生成和弦走向（按小节）
    输出：DataFrame: bar, chord
    """
    num_bars = config["num_bars"]
    progression = choose_chord_progression(config["mood"])
    rows = []

    for bar in range(1, num_bars + 1):
        chord_symbol = progression[(bar - 1) % len(progression)]
        rows.append({"bar": bar, "chord": chord_symbol})

    chords_df = pd.DataFrame(rows)
    return chords_df


def arrange_tracks(melody_df, chords_df, config):
    """
    根据编曲模板，把旋律和和弦分配给不同乐器轨道。
    输出：dict[str, DataFrame]
    """
    tracks = {}

    # Lead：直接用 melody
    lead_df = melody_df.copy()
    lead_df["instrument"] = "Lead"
    tracks["Lead"] = lead_df

    # Chords：每小节 1 个和弦
    chord_rows = []
    for _, row in chords_df.iterrows():
        bar = int(row["bar"])
        chord = row["chord"]
        chord_rows.append(
            {
                "bar": bar,
                "beat": 0.0,
                "symbol": chord,
                "duration": 4.0,  # 假设一小节 4 拍
            }
        )
    chord_track = pd.DataFrame(chord_rows)
    chord_track["instrument"] = "Chords"
    tracks["Chords"] = chord_track

    # Bass：根音占一小节
    bass_rows = []
    for _, row in chords_df.iterrows():
        bar = int(row["bar"])
        chord = row["chord"]
        bass_rows.append(
            {
                "bar": bar,
                "beat": 0.0,
                "pattern": f"{chord}_root",
                "duration": 4.0,
            }
        )
    bass_track = pd.DataFrame(bass_rows)
    bass_track["instrument"] = "Bass"
    tracks["Bass"] = bass_track

    # Drums：简单 4/4 鼓点
    drum_rows = []
    for bar in range(1, config["num_bars"] + 1):
        for beat in [0.0, 1.0, 2.0, 3.0]:
            drum_rows.append(
                {
                    "bar": bar,
