import streamlit as st
from bs4 import BeautifulSoup
import re

st.title("person要素の抽出ツール")

with st.expander("🔰 このツールの使い方ガイド"):
    st.markdown("""
### 🧾 ツールの概要
このツールは、アップロードした XML ファイル内から `<person>〜</person>` タグで囲まれた人物情報を、キーワードで検索して抽出するものです。

---

### 🔍 使い方
1. **XMLファイルをアップロード**
    - 複数ファイル同時にアップロード可能です。
2. **検索キーワードを入力**
    - 例： `天智天皇, 持統天皇` のように、カンマ区切りで複数入力可能です。
3. **一致するデータが表示されます**
    - `<person>〜</person>` タグで囲まれた文字列が表示されます。
    - 出典ファイルも展開することで確認できます。

---

### 💡 注意点
- XMLはUTF-8形式で保存されている必要があります。
- `<person>` タグが適切に閉じられていないと、正しく抽出できない場合があります。
- 検索はタグの中身すべてに対して行われます（作者名、職業なども対象）。

---
""")

uploaded_files = st.file_uploader(
    "参照したいXMLファイル（person情報があるもの）をアップロードしてください", type="xml", accept_multiple_files=True)

keywords_input = st.text_input("検索キーワード（人名など）複数ある場合はカンマで区切る", "")

if uploaded_files and keywords_input:
    keywords = [kw.strip() for kw in keywords_input.split(",")]
    matches = []

    # 各ファイルを処理
    for uploaded_file in uploaded_files:
        content = uploaded_file.read().decode("utf-8")
        soup = BeautifulSoup(content, "xml")

        person_tags = soup.find_all("person")
        for tag in person_tags:
            tag_str = str(tag)
            if any(keyword in tag_str for keyword in keywords):
                matches.append({
                    "text": tag_str,
                    "filename": uploaded_file.name
                })

    # 抽出結果の表示
    if matches:
        st.success(f"{len(matches)} 件見つかりました。")

        for match in matches:
            st.code(match["text"], language="xml")
            with st.expander("どのファイルから見つかったかを見る"):
                st.markdown(f"この情報は **{match['filename']}** から抽出されました。")
    else:
        st.warning("一致するキーワードが見つかりませんでした。")
