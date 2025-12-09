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
                    "beat": beat,
                    "hit": "kick" if beat in [0.0, 2.0] else "snare",
                }
            )
    drums_track = pd.DataFrame(drum_rows)
    drums_track["instrument"] = "Drums"
    tracks["Drums"] = drums_track

    return tracks

# --------------------------------------
# 五线谱（音名）与简谱表示
# --------------------------------------

SCALE_NOTE_MAP = {
    "C major": ["C4", "D4", "E4", "F4", "G4", "A4", "B4"],
    "G major": ["G3", "A3", "B3", "C4", "D4", "E4", "F#4"],
    "D major": ["D3", "E3", "F#3", "G3", "A3", "B3", "C#4"],
    "A minor": ["A3", "B3", "C4", "D4", "E4", "F4", "G4"],
    "E minor": ["E3", "F#3", "G3", "A3", "B3", "C4", "D4"],
}


def degree_to_note_name(degree: int, key: str) -> str:
    """把音级（1-7）映射成一个简单的音名（近似五线谱信息）"""
    scale = SCALE_NOTE_MAP.get(key, SCALE_NOTE_MAP["C major"])
    idx = int(degree) - 1
    idx = max(0, min(idx, 6))
    return scale[idx]


def build_jianpu_string(melody_df: pd.DataFrame, num_bars: int) -> str:
    """把旋律转换成按小节分组的简谱字符串，例如：1 2 3 5 | 5 5 3 2"""
    bars = []
    for bar in range(1, num_bars + 1):
        sub = melody_df[melody_df["bar"] == bar]
        if sub.empty:
            continue
        nums = [str(int(d)) for d in sub["degree"].tolist()]
        bars.append(" ".join(nums))
    return " | ".join(bars)


def build_staff_string(melody_df: pd.DataFrame, key: str, num_bars: int) -> str:
    """
    用音名列表的方式表示“接近五线谱”的信息。
    示例：
    Bar 1: C4 D4 E4 G4
    Bar 2: E4 D4 C4 D4
    """
    lines = []
    for bar in range(1, num_bars + 1):
        sub = melody_df[melody_df["bar"] == bar]
        if sub.empty:
            continue
        notes = [degree_to_note_name(deg, key) for deg in sub["degree"].tolist()]
        line = f"Bar {bar}: " + " ".join(notes)
        lines.append(line)
    return "\n".join(lines)

# --------------------------------------
# PDF 导出
# --------------------------------------

def generate_pdf_report(composition):
    """
    根据当前 composition 生成一份简单 PDF 报告（包含配置、和弦、简谱、音名）。
    返回 bytes，给 st.download_button 使用。
    """
    config = composition["config"]
    melody_df = composition["melody"]
    chords_df = composition["chords"]
    tracks = composition["tracks"]

    num_bars = config["num_bars"]
    key = config["key"]

    jianpu_str = build_jianpu_string(melody_df, num_bars)
    staff_str = build_staff_string(melody_df, key, num_bars)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 第 1 页：基本信息
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Music Composition Report", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(4)
    pdf.cell(0, 8, "Configuration:", ln=True)

    cfg_lines = {
        "Mood": config["mood"],
        "Style": config["style"],
        "BPM": config["bpm"],
        "Key": config["key"],
        "Bars": config["num_bars"],
        "Arrangement": config["arrangement"],
    }
    for k, v in cfg_lines.items():
        pdf.cell(0, 6, f"- {k}: {v}", ln=True)

    # 和弦
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Chord Progression (per bar):", ln=True)
    pdf.set_font("Arial", size=11)
    for _, row in chords_df.iterrows():
        pdf.cell(0, 6, f"Bar {int(row['bar'])}: {row['chord']}", ln=True)

    # 第 2 页：简谱 & 音名
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Melody - Jianpu (Simplified Numeric Notation):", ln=True)
    pdf.set_font("Arial", size=11)
    for line in jianpu_str.split("|"):
        pdf.cell(0, 6, line.strip(), ln=True)

    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Melody - Staff-like Note Names:", ln=True)
    pdf.set_font("Arial", size=11)
    for line in staff_str.split("\n"):
        pdf.cell(0, 6, line, ln=True)

    # 轨道概要
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Tracks Summary:", ln=True)
    pdf.set_font("Arial", size=11)
    for name, df in tracks.items():
        pdf.cell(0, 6, f"- {name}: {len(df)} events", ln=True)

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return pdf_bytes

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
        这是一个用于期末项目的 **AI 音乐作曲与编曲原型**：

        - 左侧设置情绪、风格、速度、调性和长度  
        - 点击 **Generate Composition** 生成：主旋律、和弦走向、多乐器轨道  
        - 旋律会以 **五线谱信息（音名）+ 简谱（数字谱）** 的形式展示，并可导出 PDF 报告
        """
    )

    # 侧边栏：参数设置
    st.sidebar.header("🎛 Composition Settings")

    mood = st.sidebar.selectbox(
        "Mood",
        ["Happy", "Sad", "Calm", "Epic", "Lo-fi"],
        index=0,
    )

    style = st.sidebar.selectbox(
        "Style",
        ["Pop", "Cinematic", "Game BGM", "Lo-fi", "Jazz"],
        index=0,
    )

    bpm = st.sidebar.slider("Tempo (BPM)", 60, 180, 100, step=5)

    key = st.sidebar.selectbox(
        "Key",
        ["C major", "G major", "A minor", "E minor", "D major"],
        index=0,
    )

    num_bars = st.sidebar.slider("Length (bars)", 4, 32, 8, step=4)

    arrangement = st.sidebar.selectbox(
        "Arrangement Template",
        ["Pop Band", "String Ensemble", "8-bit Game"],
        index=0,
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

    comp = st.session_state["composition"]
    if comp is None:
        st.info("👉 在左侧设置参数，然后点击 **Generate Composition** 开始生成。")
        return

    config = comp["config"]
    melody_df = comp["melody"]
    chords_df = comp["chords"]
    tracks = comp["tracks"]

    # 配置概览
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
        st.markdown("**High-level Description (for report/presentation)**")
        st.write(
            f"This piece is a **{config['style']}** style track in **{config['key']}** "
            f"with a **{config['mood']}** mood, at **{config['bpm']} BPM**, "
            f"arranged as **{config['arrangement']}** over **{config['num_bars']} bars**."
        )

    # 旋律 + 谱表示
    st.subheader("🎵 Melody & Notation")

    jianpu_str = build_jianpu_string(melody_df, config["num_bars"])
    staff_str = build_staff_string(melody_df, config["key"], config["num_bars"])

    mcol1, mcol2 = st.columns(2)

    with mcol1:
        st.markdown("**Melody Data (for debugging / analysis)**")
        st.dataframe(melody_df, use_container_width=True)

    with mcol2:
        st.markdown("**Chord Progression (per bar)**")
        st.dataframe(chords_df, use_container_width=True)

    st.markdown("**简谱（Numeric Notation）**")
    st.code(jianpu_str, language="text")

    st.markdown("**五线谱信息（以音名表示，非真实乐谱图像）**")
    st.code(staff_str, language="text")

    # 多乐器轨道
    st.subheader("🎻 Multi-instrument Tracks")

    for name, df in tracks.items():
        with st.expander(f"Track: {name}", expanded=(name == "Lead")):
            st.dataframe(df, use_container_width=True)

    # 导出 PDF
    st.subheader("📥 Export PDF Report")

    pdf_bytes = generate_pdf_report(comp)
    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name="ai_music_composition_report.pdf",
        mime="application/pdf",
    )


if __name__ == "__main__":
    main()
