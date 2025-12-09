# streamlit_app.py - 极简音乐可视化工作室
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64
import io
from PIL import Image
import random
import math

# 页面配置
st.set_page_config(
    page_title="Music Art Visualizer",
    page_icon="🎵",
    layout="wide"
)

# 应用标题
st.title("🎵 Music Art Visualizer")
st.markdown("**Transform your music into visual art with one click!**")

# 生成简单的音乐模拟数据
def generate_music_data(music_type="electronic"):
    """生成模拟的音乐数据"""
    np.random.seed(42)
    
    if music_type == "electronic":
        beats = 120  # BPM
        frequencies = np.linspace(80, 2000, 1000)
        amplitudes = np.random.exponential(0.5, 1000) * np.sin(frequencies/100)
        
    elif music_type == "classical":
        beats = 72
        frequencies = np.linspace(50, 1000, 1000)
        amplitudes = np.random.normal(0.5, 0.2, 1000) * np.sin(frequencies/50)
        
    elif music_type == "jazz":
        beats = 100
        frequencies = np.linspace(60, 1500, 1000)
        amplitudes = np.random.uniform(0.3, 0.8, 1000) * np.sin(frequencies/80)
    
    else:  # pop
        beats = 128
        frequencies = np.linspace(100, 2500, 1000)
        amplitudes = np.random.random(1000) * np.sin(frequencies/120)
    
    return {
        "frequencies": frequencies,
        "amplitudes": amplitudes,
        "beats": beats,
        "music_type": music_type
    }

# 3种简单的可视化风格
def create_waveform_art(music_data):
    """风格1：波形艺术"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 基于音乐类型选择颜色
    colors = {
        "electronic": ["#FF006E", "#8338EC", "#3A86FF"],
        "classical": ["#FF9E00", "#FF5400", "#FF006E"],
        "jazz": ["#38B000", "#70E000", "#CCFF33"],
        "pop": ["#7209B7", "#F72585", "#4361EE"]
    }
    
    color = colors.get(music_data["music_type"], ["#FF006E", "#8338EC"])
    
    # 创建波形
    x = music_data["frequencies"]
    y = music_data["amplitudes"]
    
    # 添加一些噪声和效果
    for i in range(3):
        ax.plot(x, y + i*0.2, 
                color=color[i % len(color)], 
                alpha=0.7,
                linewidth=2)
    
    ax.fill_between(x, -0.5, 0.5, alpha=0.1, color=color[0])
    ax.axis('off')
    ax.set_facecolor('#111111')
    fig.patch.set_facecolor('#111111')
    
    plt.tight_layout()
    return fig

def create_circular_art(music_data):
    """风格2：圆形艺术"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 音乐数据映射到圆形
    angles = np.linspace(0, 2 * np.pi, 1000)
    radii = 0.5 + music_data["amplitudes"][:1000] * 0.3
    
    # 创建多个同心圆
    for i in range(5):
        r = radii * (1 + i * 0.1)
        x = r * np.cos(angles + i * 0.5)
        y = r * np.sin(angles + i * 0.5)
        
        ax.plot(x, y, 
                color=plt.cm.plasma(i/5), 
                alpha=0.7,
                linewidth=1.5)
    
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#000000')
    fig.patch.set_facecolor('#000000')
    
    plt.tight_layout()
    return fig

def create_particle_art(music_data):
    """风格3：粒子艺术"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 基于音乐振幅创建粒子
    n_particles = 500
    amplitudes = music_data["amplitudes"]
    
    # 生成随机粒子位置
    x = np.random.randn(n_particles) * 2
    y = np.random.randn(n_particles) * 2
    
    # 粒子大小基于音乐振幅
    sizes = np.abs(amplitudes[:n_particles]) * 100 + 10
    colors = amplitudes[:n_particles]
    
    # 散点图
    scatter = ax.scatter(x, y, 
                         s=sizes, 
                         c=colors, 
                         cmap='viridis',
                         alpha=0.6,
                         edgecolors='white',
                         linewidth=0.5)
    
    # 添加一些连接线
    for i in range(0, n_particles, 50):
        for j in range(i+1, min(i+3, n_particles)):
            ax.plot([x[i], x[j]], [y[i], y[j]], 
                    'w-', alpha=0.1, linewidth=0.5)
    
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')
    
    plt.tight_layout()
    return fig

# 侧边栏控制
st.sidebar.header("🎛️ Control Panel")

# 1. 音乐类型选择
music_type = st.sidebar.selectbox(
    "Select Music Type",
    ["electronic", "pop", "classical", "jazz"],
    index=0
)

# 2. 可视化风格选择
art_style = st.sidebar.radio(
    "Art Style",
    ["Waveform Art", "Circular Art", "Particle Art"],
    index=0
)

# 3. 颜色调整
brightness = st.sidebar.slider("Brightness", 0.5, 1.5, 1.0, 0.1)
art_size = st.sidebar.slider("Art Size", 0.5, 2.0, 1.0, 0.1)

# 4. 生成按钮
if st.sidebar.button("🎨 Generate Art", type="primary", use_container_width=True):
    # 生成音乐数据
    music_data = generate_music_data(music_type)
    
    # 创建可视化
    with st.spinner("Creating your music art..."):
        if art_style == "Waveform Art":
            fig = create_waveform_art(music_data)
        elif art_style == "Circular Art":
            fig = create_circular_art(music_data)
        else:  # Particle Art
            fig = create_particle_art(music_data)
        
        # 显示图表
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.pyplot(fig)
            
            # 下载按钮
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, facecolor=fig.get_facecolor())
            buf.seek(0)
            
            st.download_button(
                label="📥 Download Artwork",
                data=buf,
                file_name=f"music_art_{music_type}.png",
                mime="image/png",
                use_container_width=True
            )
        
        with col2:
            # 音乐信息显示
            st.subheader("🎵 Music Info")
            st.metric("BPM", music_data["beats"])
            st.metric("Type", music_data["music_type"].title())
            st.metric("Art Style", art_style)
            
            # 艺术信息
            st.subheader("🎨 Art Info")
            st.write(f"**Colors:** Based on {music_type} palette")
            st.write(f"**Pattern:** Generated from {len(music_data['amplitudes'])} data points")
            st.write(f"**Brightness:** {brightness}x")
            
            # 简单的频率可视化
            st.subheader("📊 Frequency Spectrum")
            freq_chart = np.abs(music_data["amplitudes"][:100])
            st.line_chart(freq_chart)

# 如果没有生成艺术，显示示例
else:
    st.info("👈 Select music type and art style, then click 'Generate Art'")
    
    # 显示示例图片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400", 
                caption="Waveform Art Example")
    
    with col2:
        st.image("https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400", 
                caption="Circular Art Example")
    
    with col3:
        st.image("https://images.unsplash.com/photo-1519681393784-d120267933ba?w-400", 
                caption="Particle Art Example")

# 使用说明
with st.expander("📖 How to Use"):
    st.markdown("""
    ### Simple Steps:
    1. **Select Music Type** - Choose from electronic, pop, classical, or jazz
    2. **Choose Art Style** - Pick one of 3 visualization styles
    3. **Adjust Settings** - Fine-tune brightness and size
    4. **Generate & Download** - Click the button and save your artwork
    
    ### What's Happening Behind the Scenes:
    - Simulated music data is generated based on your selection
    - Mathematical algorithms transform frequencies into visual patterns
    - Colors are automatically selected based on music genre
    - You get a unique artwork every time!
    
    ### Tech Used:
    - **Streamlit** - Web interface
    - **Matplotlib** - Art generation
    - **NumPy** - Data processing
    - No external APIs or complex dependencies!
    """)

# 项目信息
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎓 Final Project")
st.sidebar.markdown("**Arts & Advanced Big Data**")
st.sidebar.markdown("Sungkyunkwan University")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>Music Art Visualizer | Final Project | Arts & Advanced Big Data</p>
    <p>Sungkyunkwan University | Fall 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)
