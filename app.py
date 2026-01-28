import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- ページ設定 (タイトルやアイコン) ---
st.set_page_config(
    page_title="Life Mapping - 人生の羅針盤",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSSで見た目をリッチに調整 ---
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        font-size: 1.2rem;
        border-radius: 10px;
        padding: 0.5em 2em;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #2563EB;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- タイトル表示 ---
st.markdown('<div class="main-header">Life Mapping Diagnosis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">あなたの人生の現在地を測り、次の一歩を見つける羅針盤</div>', unsafe_allow_html=True)

# --- サイドバー：ユーザー情報 ---
with st.sidebar:
    st.header("👤 プロフィール")
    name = st.text_input("お名前 (Name)", placeholder="例: 望 太郎")
    st.markdown("---")
    st.info("💡 スライダーを動かして、直感的に今の状態を入力してください。")

# --- メインエリア：入力フォーム (2カラムレイアウト) ---
col1, col2 = st.columns([1, 1])

# 入力値を格納する辞書
scores = {}

# 左カラム：内面的要素
with col1:
    st.subheader("Inner World (内面)")
    scores['哲学'] = st.slider("Q1. 哲学 (Philosophy) - 自分軸・価値観", 1.0, 5.0, 3.0, 0.1)
    scores['才能'] = st.slider("Q2. 才能 (Talent) - 強み・ギフト", 1.0, 5.0, 3.0, 0.1)
    scores['構想'] = st.slider("Q3. 構想 (Vision) - 未来・理想", 1.0, 5.0, 3.0, 0.1)

# 右カラム：外面的要素
with col2:
    st.subheader("Outer World (外面)")
    scores['環境'] = st.slider("Q4. 環境 (Environment) - 居場所・資産", 1.0, 5.0, 3.0, 0.1)
    scores['健康'] = st.slider("Q5. 健康 (Vitality) - 身体・メンタル", 1.0, 5.0, 3.0, 0.1)
    scores['繋がり'] = st.slider("Q6. 繋がり (Connection) - 愛・人間関係", 1.0, 5.0, 3.0, 0.1)

# --- 診断ロジック (Analysis Logic) ---
def analyze_archetype(s):
    # 値の取得（短縮形）
    phi, env, tal, des, vit, con = s['哲学'], s['環境'], s['才能'], s['構想'], s['健康'], s['繋がり']
    min_score = min(s.values())
    
    # ロジック判定 (優先順位順)
    
    # 1. Type 5: 統合された統治者 (The Integrated Sovereign)
    # 条件: 全てが4.0以上 (厳格な基準)
    if min_score >= 4.0:
        return "Type 5: 統合された統治者 (The Integrated Sovereign)", \
               "人生のあらゆる要素が調和し、あなたは自分の王国をしっかりと治めています。", \
               "👑"

    # 2. Type 9: 求心力あるリーダー (The Charismatic Leader)
    # 条件: 繋がり>=4.0, 構想>=4.0, かつ 健康>=3.5 (無理していないこと)
    if con >= 4.0 and des >= 4.0 and vit >= 3.5:
        return "Type 9: 求心力あるリーダー (The Charismatic Leader)", \
               "人々を惹きつける魅力とビジョンを持っています。ですが、自分のための『遊び』を忘れていませんか？", \
               "🌞"

    # 3. Type 1: 傷ついた戦士 (The Burnout Warrior)
    # 条件: 健康が極端に低い、または全体的に疲弊している
    if vit < 3.0:
        return "Type 1: 傷ついた戦士 (The Burnout Warrior)", \
               "誰よりも戦い続けてきましたね。今は重い鎧を脱いで、休むことが最大の勇気です。", \
               "🛡️"

    # 4. その他 (簡易ロジック)
    if tal >= 4.0:
        return "Type 13: 構想する建築家 (The Architect)", "才能とビジョンが光っています。あとは現実化への『環境』作りが鍵です。", "🏗️"
    
    if phi >= 4.0:
        return "Type 4: 哲学する賢者 (The Philosopher)", "確固たる自分軸を持っています。その知恵を外の世界へ届ける時が来ました。", "🦉"

    # デフォルト
    return "Type 0: 旅の途中 (The Traveler)", "あなたは今、自分だけの地図を描いている最中です。どの方向へも進めます。", "🚶"

# --- 診断ボタン ---
st.markdown("---")
if st.button("診断結果を表示する (Show Result)"):
    if not name:
        st.warning("お名前を入力してください！")
    else:
        # 結果の計算
        archetype_name, description, icon = analyze_archetype(scores)
        
        # --- 結果表示エリア ---
        st.success(f"診断完了！ {name} さんの現在地が見つかりました。")
        
        # 2カラムで結果表示
        res_col1, res_col2 = st.columns([1, 1.5])
        
        with res_col1:
            # プロット作成 (Plotly)
            categories = list(scores.keys())
            values = list(scores.values())
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=name,
                line_color='#1E3A8A',
                fillcolor='rgba(30, 58, 138, 0.2)'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )),
                showlegend=False,
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

        with res_col2:
            st.markdown(f"### {icon} {archetype_name}")
            st.info(description)
            
            # 詳細スコア表示
            st.markdown("#### Life Elements Analysis")
            for key, value in scores.items():
                bar_color = "green" if value >= 4.0 else "orange" if value >= 2.5 else "red"
                st.write(f"**{key}:** {value}")
                st.progress(value / 5.0)

        # --- Next Action ---
        st.markdown("---")
        st.markdown("### 🎁 Next Step")
        st.write("この結果を保存し、より詳細な解説（note）を読みましょう。")
        st.write("※ ここにGoogle Sheetsへの保存機能や、noteへのリンクボタンを配置します。")