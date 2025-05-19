import streamlit as st
import json
import gspread
from google.oauth2.service_account import Credentials

# 1. 读取本地上传的 JSON 文件
# 假设你在项目根目录放了 your_credentials.json
with open("your_credentials.json") as f:
    creds_dict = json.load(f)

# 2. 创建认证凭证（记得加上所需权限）
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

# 3. 连接 Google Sheets
client = gspread.authorize(creds)
sheet_id = "1ga4yQT0oUc3X1a1kEO6FdP3vzxdTAV3AwxQ4W2jo_-Q"  # 替换成你的表ID
sheet = client.open_by_key(sheet_id).Sound2ColorOutcome

# Streamlit界面
st.title("声音联想颜色实验")

# 播放预制音频（需要提前放置音频文件，streamlit支持wav/mp3）
audio_file = open("audio_sample.mp3", "rb").read()
if st.button("播放音频"):
    st.audio(audio_file, format="audio/mp3")

# 颜色选择
color = st.color_picker("请选择你联想到的颜色")

# 保存按钮
if st.button("保存颜色"):
    # 将颜色转换为RGB
    # st.color_picker返回的是HEX，需要转换成RGB
    hex_color = color.lstrip("#")
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    try:
        # 追加新行到表格
        sheet.append_row([rgb[0], rgb[1], rgb[2]])
        st.success(f"成功保存颜色 RGB: {rgb}")
    except Exception as e:
        st.error(f"❌ 数据保存失败：{e}")
