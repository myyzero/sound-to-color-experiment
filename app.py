import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="声音-颜色联想实验", layout="centered")

st.title("🎧 声音与颜色联想实验")

# 播放音频
audio_file = open("your-audio.mp3", "rb")
st.audio(audio_file.read(), format="audio/mp3")

st.markdown("请完整听完音频后，选择你联想到的颜色 👇")

# 颜色选择器
color = st.color_picker("🎨 请选择颜色", "#ffffff")

# 提交按钮
if st.button("✅ 提交你的颜色"):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "hex": color,
        "r": r,
        "g": g,
        "b": b
    }

    try:
        df = pd.read_csv("responses.csv")
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([data])

    df.to_csv("responses.csv", index=False)
    st.success("✅ 你的颜色已保存，感谢参与！")
