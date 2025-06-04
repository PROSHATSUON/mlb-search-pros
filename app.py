import streamlit as st
import requests

st.title("MLB YouTube 検索ツール")
keyword = st.text_input("検索ワードを入力してください")

if keyword:
    st.write(f"🔍「{keyword}」で検索中...")

    # ↓↓↓ エラーチェック用に APIキーと検索結果の中身も表示する
    try:
        API_KEY = st.secrets["YOUTUBE_API_KEY"]
    except Exception as e:
        st.error("APIキーが見つかりません。StreamlitのSecretsを確認してください。")
        st.stop()

    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": keyword,
        "key": API_KEY,
        "type": "video",
        "maxResults": 5
        # "channelId": "UCBVY2e4zZxtDGA8-B1Dm0nQ"  ← 今はコメントアウト
    }

    res = requests.get(SEARCH_URL, params=params)
    result = res.json()

    st.write(result)  # ← APIの生データを表示してチェック

    items = result.get("items", [])
    if not items:
        st.warning("動画が見つかりませんでした。キーワードやAPIキーを確認してください。")
    else:
        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            st.markdown(f"### [{title}](https://www.youtube.com/watch?v={video_id})")
            st.video(f"https://www.youtube.com/watch?v={video_id}")
