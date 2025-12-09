import streamlit as st
import pandas as pd
import random

# --------------------------------------
# 基础工具函数
# --------------------------------------

def build_scale(key: str, mode: str = "major"):
    """根据调性生成一个简单音阶（用数字代替音高，方便后续扩展成 MIDI）"""
    # 这里用相对音级 1-7 表示，真正实现时可以换成 MIDI 音高
    if mode == "major":
        scale_degrees = [1, 2, 3, 4, 5, 6, 7]
    else:
        scale_degrees = [1, 2, 3, 4, 5, 6, 7]  # 你可以自己根据小调调整

    return scale_degrees


def choose_chord_progression(mood: str):
    """根据情绪选择一个简单和弦进行（用 I, V, vi, IV 等罗马数字代替）"""
    progressions = {
        "Happy": [["I", "V", "vi", "IV"]],
        "Sad": [["vi", "IV", "I", "V"]],
        "Calm": [["I", "IV", "ii", "V"]],
        "Epic": [["i", "VI", "III", "VII"]],
        "Lo-fi": [["I", "iii", "vi", "IV"]],
    }
    # 如果没有匹配 mood，就用默认流行和弦
    return random.choice(progressions.get(mood, [["I", "V", "vi", "IV"]]))


def generate_melody(config):
    """
    生成主旋律（简单规则版）
    输出：一个 DataFrame，包含：bar, beat, degree, duration
    """
    num_bars = config["num_bars"]
    mood = config["mood"]
    key = config["key"]
    mode = "major" if "major" in key else "minor"

    scale = build_scale(key, mode)
    rows = []

    # 简单规则：每小节 4 个八分音符（总共 2 拍），仅作为示例
    note_per_bar = 4
    for bar in range(1, num_bars + 1):
        for i in range(note_per_bar):
            degree = random.choice(scale)
            duration = 0.5  # 0.5 拍，八分音符
            beat = i * duration
            rows.append({
                "bar": bar,
                "beat": beat,
                "degree": degree,
                "duration": duration,
            })

    melody_df = pd.DataFrame(rows)
    return melody_df


def generate_chords(config):
    """
    生成和弦走向（按小节）
    输出：一个 DataFrame，包含：bar, chord
    """
    num_bars = config["num_bars"]
    progression = choose_chord_progression(config["mood"])
    rows = []

    for bar in range(1, num_bars + 1):
        chord_symbol = progression[(bar - 1) % len(progression)]
        rows.append({
            "bar": bar,
            "chord": chord_symbol,
        })

    chords_df = pd.DataFrame(rows)
    return chords_df


def arrange_tracks(melody_df, chords_df, config):
    """
    根据编曲模板，把旋律和和弦分配给不同乐器轨道。
    输出：一个 dict，每个 key 是乐器名，对应一个 DataFrame。
    """
    arrangement = config["arrangement"]

    tracks = {}

    # Lead：直接用 melody
    lead_df = melody_df.copy()
    lead_df["instrument"] = "Lead"
    tracks["Lead"] = lead_df

    # Chords：按和弦生成简单的“块状”伴奏（每小节 1 个和弦）
    chord_rows = []
    for _, row in chords_df.iterrows():
        bar = int(row["bar"])
        chord = row["chord"]
        chord_rows.append({
            "bar": bar,
            "beat": 0.0,
            "symbol": chord,
            "duration": 4.0,  # 这里假定一小节 4 拍
        })
    chord_track = pd.DataFrame(chord_rows)
    chord_track["instrument"] = "Chords"
    tracks["Chords"] = chord_track

    # Bass：使用和弦根音的简化表示（这里直接用 bar 号替代，实际可映射到低音音高）
    bass_rows = []
    for _, row in chords_df.iterrows():
        bar = int(row["bar"])
        chord = row["chord"]
        bass_rows.append({
            "bar": bar,
            "beat": 0.0,
            "pattern": f"{chord}_root",
            "duration": 4.0,
        })
    bass_track = pd.DataFrame(bass_rows)
    bass_track["instrument"] = "Bass"
    tracks["Bass"] = bass_track

    # Drums：简单节奏 pattern
    drum_rows = []
    for bar in range(1, config["num_bars"] + 1):
        # 4/4：在 0, 1, 2, 3 拍放一个简单鼓点
        for beat in [0.0, 1.0, 2.0, 3.0]:
            drum_rows.append({
                "bar": bar,
                "beat": beat,
                "hit": "kick" if beat in [0.0, 2.0] else "snare",
            })
    drums_track = pd.DataFrame(drum_rows)
    drums_track["instrument"] = "Drums"
    tracks["Drums"] = drums_track

    # 未来可以根据 arrangement 模板，对不同风格做不一样的 pattern
    # 例如：Pop Band / Strings / 8-bit Game 等

    return tracks


# --------------------------------------
# Streamlit App 主体
# --------------------------------------

def main():
    st.set_page_config(
        page_title="AI Music Composition Studio",
        layout="wide",
    )

    st.title("🎼 AI Music Composition Studio")
    st.markdown(
        """
        This app is a **prototype framework** for your final project:
        an AI-assisted music composition & arrangement tool.
        
        - Set mood, style, tempo, and key on the left.
        - Click **Generate Composition** to create:
          - a main melody  
          - a chord progression  
          - multi-instrument tracks (Lead, Chords, Bass, Drums)  
        - Later you can replace the simple rule-based logic with real AI / ML models.
        """
    )

    # 侧边栏：参数设置
    st.sidebar.header("🎛 Composition Settings")

    mood = st.sidebar.selectbox(
        "Mood",
        ["Happy", "Sad", "Calm", "Epic", "Lo-fi"],
        index=0
    )

    style = st.sidebar.selectbox(
        "Style",
        ["Pop", "Cinematic", "Game BGM", "Lo-fi", "Jazz"],
        index=0
    )

    bpm = st.sidebar.slider("Tempo (BPM)", 60, 180, 100, step=5)

    key = st.sidebar.selectbox(
        "Key",
        ["C major", "G major", "A minor", "E minor", "D major"],
        index=0
    )

    num_bars = st.sidebar.slider("Length (bars)", 4, 32, 8, step=4)

    arrangement = st.sidebar.selectbox(
        "Arrangement Template",
        ["Pop Band", "String Ensemble", "8-bit Game"],
        index=0
    )

    if "composition" not in st.session_state:
        st.session_state["composition"] = None

    if st.sidebar.button("🎹 Generate Composition"):
        config = {
            "mood": mood,
            "style": style,
            "bpm": bpm,
            "key": key,
            "num_bars": num_bars,
            "arrangement": arrangement,
        }

        melody_df = generate_melody(config)
        chords_df = generate_chords(config)
        tracks = arrange_tracks(melody_df, chords_df, config)

        st.session_state["composition"] = {
            "config": config,
            "melody": melody_df,
            "chords": chords_df,
            "tracks": tracks,
        }

    # 显示生成结果
    comp = st.session_state["composition"]
    if comp is None:
        st.info("👉 Set parameters on the left and click **Generate Composition** to start.")
        return

    config = comp["config"]
    melody_df = comp["melody"]
    chords_df = comp["chords"]
    tracks = comp["tracks"]

    # 上半部分：配置 & 总览
    st.subheader("🎯 Composition Overview")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Configuration**")
        st.write(
            {
                "Mood": config["mood"],
                "Style": config["style"],
                "BPM": config["bpm"],
                "Key": config["key"],
                "Bars": config["num_bars"],
                "Arrangement": config["arrangement"],
            }
        )

    with col2:
        st.markdown("**High-level Description (for your report / slides)**")
        st.write(
            f"This piece is a **{config['style']}** style track in **{config['key']}** "
            f"with a **{config['mood']}** mood, at **{config['bpm']} BPM**, "
            f"arranged as **{config['arrangement']}** over **{config['num_bars']} bars**."
        )

    # 中间部分：Melody & Chords
    st.subheader("🎵 Melody & Chord Progression")

    mc_col1, mc_col2 = st.columns(2)

    with mc_col1:
        st.markdown("**Main Melody (simplified)**")
        st.dataframe(melody_df, use_container_width=True)

    with mc_col2:
        st.markdown("**Chord Progression (per bar)**")
        st.dataframe(chords_df, use_container_width=True)

    # 下半部分：多乐器轨道
    st.subheader("🎻 Multi-instrument Tracks")

    for name, df in tracks.items():
        with st.expander(f"Track: {name}", expanded=(name == "Lead")):
            st.dataframe(df, use_container_width=True)
            # 未来可以在这里添加可视化（piano-roll / bar chart）或音频播放

    st.markdown("---")
    st.markdown(
        """
        ✅ **Next Steps / TODO (for your final project):**  
        - Replace the random & rule-based generation with more advanced music algorithms or AI models.  
        - Add real MIDI / audio rendering and playback.  
        - Add user controls for regenerating only one track (e.g., bass line).  
        - Export compositions (JSON, MIDI, MusicXML, etc.).
        """
    )


if __name__ == "__main__":
    main()
