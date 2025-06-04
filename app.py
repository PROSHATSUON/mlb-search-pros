import streamlit as st
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import os

# YouTube APIキーをSecretsから取得
API_KEY = st.secrets["YOUTUBE_API_KEY"]

st.title("MLB YouTube 検索ツール")
keyword = st.text_input("検索ワードを入力してください")

if keyword:
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": keyword,
        "key": API_KEY,
        "type": "video",
        "maxResults": 5
    }

    res = requests.get(search_url, params=params)
    result = res.json()
    items = result.get("items", [])

    if not items:
        st.info("動画が見つかりませんでした。キーワードを変えて再検索してみてください。")

    for item in items:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]

        st.markdown(f"### [{title}](https://www.youtube.com/watch?v={video_id})")
        st.video(f"https://www.youtube.com/watch?v={video_id}")

        # 字幕の中でキーワードにマッチする部分だけ表示
        def show_matched_captions(video_id, keyword):
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                matched = [entry for entry in transcript if keyword.lower() in entry['text'].lower()]

                if matched:
                    st.markdown("### ✨ キーワードにマッチした字幕")
                    for entry in matched:
                        start = int(entry['start'])
                        text = entry['text']
                        url = f"https://www.youtube.com/watch?v={video_id}&t={start}s"
                        st.markdown(f"- [{text}]({url}) （{start}秒から）")
                else:
                    st.info("字幕の中にキーワードは見つかりませんでした。")

            except TranscriptsDisabled:
                st.info("この動画には字幕が無効になっています。")
            except NoTranscriptFound:
                st.info("字幕が見つかりませんでした。")
            except Exception as e:
                st.warning(f"字幕取得時にエラーが発生しました：{e}")

        show_matched_captions(video_id, keyword)
