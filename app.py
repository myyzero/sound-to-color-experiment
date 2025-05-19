import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# ---------- Google Sheet 授权部分 ----------
# 从 Streamlit secrets 中加载 JSON 凭据
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

# 定义授权范围
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# 授权并连接到 Google Sheets
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["SHEET_ID"]).worksheet("Sound2Color Outcome")

# ---------- 页面内容 ----------
st.title("🎧 声音感知颜色实验")

st.write("点击下方按钮播放音频，然后根据你联想到的颜色在调色盘中进行选择，最后点击提交按钮。")

# 播放音频
audio_file = open("your_audio.mp3", "rb")  # 将音频文件与你的 app.py 放在同一个目录下
audio_bytes = audio_file.read()
st.audio(audio_bytes, format="audio/mp3")

# 颜色选择器
color = st.color_picker("🎨 请选择你联想到的颜色", "#ffffff")

# 提交按钮
if st.button("提交"):
    # 获取当前时间
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 拆分 RGB
    hex_color = color.lstrip('#')
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # 写入 Google Sheet
    sheet.append_row([timestamp, color, rgb[0], rgb[1], rgb[2]])

    st.success("✅ 提交成功！感谢你的参与。")

# 显示当前表格记录数（可选）
records = sheet.get_all_values()
st.write(f"目前已有 {len(records) - 1} 位参与者提交。")
