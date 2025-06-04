import streamlit as st

st.title("MLB YouTube 検索ツール")
keyword = st.text_input("検索キーワードを入力してください")

if keyword:
    st.write(f"あなたが検索したのは：{keyword}")
