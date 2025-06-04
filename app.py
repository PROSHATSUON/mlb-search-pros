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
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# 動画IDごとに字幕を取得して表示する関数
def show_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        st.markdown("### 📘 英語字幕（自動生成含む）")
        for entry in transcript:
            st.markdown(f"- {entry['text']}")
    except TranscriptsDisabled:
        st.info("この動画には字幕が無効になっています。")
    except NoTranscriptFound:
        st.info("字幕が見つかりませんでした。")
    except Exception as e:
        st.warning(f"字幕取得時にエラーが発生しました：{e}")
show_captions(video_id)
st.markdown(f"### [{title}](https://www.youtube.com/watch?v={video_id})")
st.video(f"https://www.youtube.com/watch?v={video_id}")
show_captions(video_id)  # ← 字幕を表示
