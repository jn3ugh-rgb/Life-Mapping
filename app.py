import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import statistics

# ▼ 3つのモジュールからそれぞれデータをインポート
from questions import questions_data
from feedback import definitions
from archetypes import calculate_archetype

# --- ページ設定 ---
st.set_page_config(
    page_title="Life Mapping Diagnosis",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- セッションステート初期化 (名前同期用) ---
if "shared_name" not in st.session_state:
    st.session_state["shared_name"] = ""

# --- コールバック関数 (同期ロジック) ---
def sync_name_from_top():
    """上の入力欄が変更されたら、共有変数に反映"""
    st.session_state["shared_name"] = st.session_state.name_top

def sync_name_from_bottom():
    """下の入力欄が変更されたら、共有変数に反映"""
    st.session_state["shared_name"] = st.session_state.name_bottom

# --- CSS (デザイン調整) ---
st.markdown("""
<style>
    .main-header {font-size: 3.0rem; color: #1E3A8A; text-align: center; font-weight: 700; margin-bottom: 1rem;}
    .sub-header {font-size: 1.2rem; color: #4B5563; text-align: center; margin-bottom: 2rem;}
    .category-header {color: #1E3A8A; border-bottom: 2px solid #1E3A8A; padding-bottom: 5px; margin-top: 20px; font-weight: bold;}
    
    /* ▼ iPhoneダークモード対策: 文字色を濃い色(#334155)に固定 */
    .feedback-box {
        background-color: #f8fafc; 
        border-left: 5px solid #1E3A8A; 
        padding: 15px; 
        border-radius: 5px; 
        margin-top: 10px; 
        margin-bottom: 20px;
        color: #334155; 
    }
    
    .tag-blue {color: #1d4ed8; font-weight: bold;} 
    .tag-green {color: #15803d; font-weight: bold;}
    .tag-red {color: #b91c1c; font-weight: bold;}
    div.stButton > button:first-child {background-color: #1E3A8A; color: white; border-radius: 8px; font-size: 1.2rem; width: 100%; padding: 0.5rem;}
    div.stButton > button:hover {background-color: #2563EB; border: none;}
</style>
""", unsafe_allow_html=True)

# --- UI構築 ---

st.markdown('<div class="main-header">Life Mapping Diagnosis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">人生の現在地を測る 48の問い</div>', unsafe_allow_html=True)

# 導入メッセージエリア
st.markdown("""
<div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid #1E3A8A; color: #334155;">
    <p style="margin:0; line-height: 1.8;">
        ようこそ、Life Mapping診断へ。<br>
        この診断は、あなたの人生を構成する<b>6つの要素（哲学・環境・才能・構想・健康・繋がり）</b>の状態を可視化し、
        今あなたがどのような<b>「アーキタイプ（冒険の原型）」</b>を生きているのかを紐解きます。<br><br>
        <b>所要時間は約3分です。</b><br>
        あまり深く考えすぎず、今の感覚に一番近いものを直感的に選んでください。<br>
        あなたの現在地を知ることが、理想の未来へ進むための最初の一歩になります。
    </p>
</div>
""", unsafe_allow_html=True)

# ▼ 【上部】お名前入力欄 (Top)
st.text_input(
    "お名前 (Name)", 
    key="name_top",
    value=st.session_state["shared_name"], # 共有変数の値を表示
    on_change=sync_name_from_top,          # 変更時に同期関数を実行
    placeholder="例: 山田 太郎"
)

st.markdown("---")
user_scores = {}

# 選択肢の定義
options = {
    1: "全く当てはまらない", 
    2: "あまり当てはまらない", 
    3: "どちらとも言えない", 
    4: "やや当てはまる", 
    5: "非常に当てはまる"
}

# カテゴリごとにループ
for category, q_list in questions_data.items():
    st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
    
    cat_answers = []
    for i, q_text in enumerate(q_list):
        # 1. 質問文
        st.markdown(f"**Q.{i+1} {q_text}**")
        
        # スライダーのキーを定義
        slider_key = f"{category}_{i}"
        
        # 現在の値を取得（セッションステートにあればそれを、なければデフォルト3）
        if slider_key in st.session_state:
            current_val = st.session_state[slider_key]
        else:
            current_val = 3
        
        # 2. 全選択肢をスライダーの上に表示 (選択中のみハイライト)
        legend_html = ""
        for k, v in options.items():
            if k == current_val:
                # 選択中のスタイル
                if k <= 2: color = "#ef4444"   # 赤
                elif k == 3: color = "#f97316" # オレンジ
                else: color = "#3b82f6"        # 青
                
                legend_html += f"<span style='color: {color}; font-weight: bold; font-size: 1.1rem; margin: 0 8px; display: inline-block;'>{k}. {v}</span>"
            else:
                # 非選択のスタイル
                legend_html += f"<span style='color: #cbd5e1; font-size: 0.8rem; margin: 0 5px; display: inline-block;'>{k}. {v}</span>"

        st.markdown(f"""
        <div style="text-align: center; line-height: 1.8; margin-bottom: 5px;">
            {legend_html}
        </div>
        """, unsafe_allow_html=True)
        
        # 3. スライダー (ラベルなし)
        val = st.select_slider(
            label="回答", 
            options=[1, 2, 3, 4, 5],
            value=3, 
            key=slider_key,
            label_visibility="collapsed"
        )
        
        cat_answers.append(val)
    
    user_scores[category] = statistics.mean(cat_answers)

st.markdown("---")

# ▼ 【下部】お名前入力欄 (Bottom) - 上部と同期
st.text_input(
    "お名前 (上部で未入力の場合はこちらへ)", 
    key="name_bottom",
    value=st.session_state["shared_name"], # 共有変数の値を表示
    on_change=sync_name_from_bottom,       # 変更時に同期関数を実行
    placeholder="例: 山田 太郎"
)

if st.button("診断結果を表示する"):
    # 名前チェックは共有変数を見る
    if not st.session_state["shared_name"]:
        st.error("お名前を入力してください。")
    else:
        name = st.session_state["shared_name"]
        
        # ▼ 【重要】 戻り値に「question」を追加して受け取る
        archetype_name, description, icon, question = calculate_archetype(user_scores)
        
        st.balloons()
        
        st.success(f"診断完了！ {name} さんの現在地が見つかりました。")
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            # レーダーチャート
            categories = list(user_scores.keys())
            values = list(user_scores.values())
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values, theta=categories, fill='toself', name=name,
                line_color='#1E3A8A', fillcolor='rgba(30, 58, 138, 0.2)'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, margin=dict(l=40, r=40, t=30, b=30))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"### {icon} {archetype_name}")
            
            # 説明文（既存）
            st.info(description)
            
            # ▼ 【重要】 「あなたへの問い」のデザインを変更（改行・太字・サイズ調整）
            st.markdown(f"""
            <div style="background-color: #fff7ed; border-left: 5px solid #f97316; padding: 15px; border-radius: 5px; margin-top: 10px; margin-bottom: 20px; color: #431407;">
                <span style="font-size: 0.9rem; color: #c2410c;">🤔 あなたへの問い</span>
                <div style="margin-top: 10px; font-weight: bold; font-size: 1.1rem; line-height: 1.5;">
                    {question}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### Life Elements Analysis")
            
            # 各要素の詳細レポート表示
            for cat, score in user_scores.items():
                # H/M/L 判定
                if score >= 4.0:
                    level, level_color = "H", "tag-blue"
                    bar_color = "blue"
                elif score >= 2.5:
                    level, level_color = "M", "tag-green"
                    bar_color = "green"
                else:
                    level, level_color = "L", "tag-red"
                    bar_color = "red"
                
                # 文章の取得
                tag_text, feedback_text = definitions[cat][level]
                
                # スコアバー表示
                bar_bg = f"background-color: {'#dbeafe' if bar_color=='blue' else '#dcfce7' if bar_color=='green' else '#fee2e2'};"
                st.markdown(f"""
                    <div style="margin-top: 10px; margin-bottom: 2px;">
                        <span style="font-weight:bold;">{cat}: {score:.1f}</span> 
                        <span class="{level_color}">{tag_text}</span>
                    </div>
                    <div style="width: 100%; background-color: #f3f4f6; border-radius: 5px; height: 8px;">
                        <div style="width: {score/5*100}%; {bar_bg} height: 8px; border-radius: 5px;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # フィードバック文章
                with st.expander(f"▼ {cat}のアドバイスを読む"):
                    st.markdown(f'<div class="feedback-box">{feedback_text}</div>', unsafe_allow_html=True)

        # Noteへの誘導
        st.markdown("---")
        st.markdown("### 🎁 Next Step")
        st.markdown(f"""
        **{archetype_name}** のあなたへ。
        
        この診断結果はあくまで「現在地」です。
        この診断結果をもとに、より詳細な地図を描いてみませんか？
        
        **👉 [Life Mapping Coaching (note)](https://note.com/toyamanchu1986/n/nd31342d61419)**
        """)