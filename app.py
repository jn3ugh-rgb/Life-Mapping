import streamlit as st
# --- 1. ページ設定 (アプリ全体の基本設定) ---
st.set_page_config(
    page_title="ライフ・ストラテジー診断 | Life Mapping",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://note.com/toyamanchu1986/n/nd31342d61419',
        'Report a bug': None,
        'About': "# ライフ・ストラテジー診断\nあなたの人生の「現在地」を測り、理想の未来への地図を描きます。"
    }
)

# --- 2. OGP設定 (SNSシェア時のサムネイル) ---
st.markdown(
    '<meta property="og:image" content="https://github.com/jn3ugh-rgb/Life-Mapping/raw/main/Life%20Mapping.png">',
    unsafe_allow_html=True
)
import pandas as pd
import plotly.graph_objects as go
import statistics

# --- CSS (デザイン調整) ---
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1E3A8A; text-align: center; font-weight: 700; margin-bottom: 1rem;}
    .sub-header {font-size: 1.2rem; color: #4B5563; text-align: center; margin-bottom: 2rem;}
    .category-header {color: #1E3A8A; border-bottom: 2px solid #1E3A8A; padding-bottom: 5px; margin-top: 20px; font-weight: bold;}
    
    /* ▼ ここを修正しました（colorを追加） */
    .feedback-box {
        background-color: #f8fafc; 
        border-left: 5px solid #1E3A8A; 
        padding: 15px; 
        border-radius: 5px; 
        margin-top: 10px; 
        margin-bottom: 20px;
        color: #334155; /* 文字色を強制的に濃い色にする */
    }
    
    .tag-blue {color: #1d4ed8; font-weight: bold;} 
    .tag-green {color: #15803d; font-weight: bold;}
    .tag-red {color: #b91c1c; font-weight: bold;}
    div.stButton > button:first-child {background-color: #1E3A8A; color: white; border-radius: 8px; font-size: 1.2rem; width: 100%; padding: 0.5rem;}
    div.stButton > button:hover {background-color: #2563EB; border: none;}
</style>
""", unsafe_allow_html=True)

# --- 1. 設問データ (Database) ---
questions_data = {
    "哲学 (Philosophy)": [
        "私は、「自分にとっての幸せとは何か」を自分の言葉で語れる。",
        "社会の常識や他人の期待よりも、自分の心の声を優先できている。",
        "日々の生活の中で、心から「満たされている」と感じる瞬間が多い。",
        "過去の選択に対して後悔はなく、すべての経験に意味があったと思える。",
        "もし明日人生が終わるとしても、今の生き方に納得できる。",
        "自分の「核」となる価値観を言語化できている",
        "迷った時、立ち返るべき判断基準がある",
    ],
    "環境 (Environment)": [
        "現在の住まいや活動場所は、自分にとって居心地が良く、エネルギーが充電できる場所だ。",
        "将来への不安に脅かされることなく、安心して暮らせる経済的な基盤がある。",
        "忙しさに追われることなく、何もしない時間や趣味を楽しむ「余白」がある。",
        "身の回りには、自分がときめく物や好きな物だけを置いている。",
        "嫌なことや合わない環境からは、距離を置くことができている。",
        "心から安らげる居場所（家庭やコミュニティ）がある",
        "経済的な不安に脅かされることなく生活できている",
        "自分の能力を発揮できる環境に身を置いている",
    ],
    "才能 (Talent)": [
        "自分が情熱を注げる「強み」や「ギフト」を自覚している",
        "その才能を使って、他者に貢献している実感がある",
        "仕事や活動の中で、フロー状態（没頭）になることが多い",
        "時間を忘れて没頭できることや、やっていて苦にならない「得意なこと」がある。",
        "自分の才能や強みを使って、誰かに喜んでもらえた経験がある。",
        "仕事や活動において、無理をして自分を偽ることなく、自然体でいられる。",
        "「あなたにお願いしたい」「あなたと居たい」と言われる独自の魅力がある。",
        "新しい知識や体験に触れ、自分をアップデートすることを楽しんでいる。",
    ],
    "構想 (Vision)": [
        "1年後、3年後の理想の未来が鮮明に描けている",
        "夢や目標に向かって、具体的な計画が進んでいる",
        "未来のことを考えるとワクワクする",
        "3年後、5年後に「こうなっていたい」という理想のライフスタイルが描けている。",
        "夢や目標を実現するために、今日できる小さな一歩を踏み出している。",
        "「死ぬまでにやりたいことリスト」のような、人生の楽しみの計画がある。",
        "予期せぬ変化が起きても、「それはそれで面白い」と柔軟に捉えられる。",
        "未来のことを考えると、不安よりもワクワクする気持ちの方が大きい。",
    ],
    "健康 (Vitality)": [
        "毎日、十分なエネルギーを持って活動できている",
        "睡眠や食事など、身体のケアを大切にしている",
        "ストレスを適切に解消し、メンタルが安定している",
        "毎朝、すっきりとした気分と十分なエネルギーで目覚めている。",
        "食事は味わってとり、自分の身体が喜ぶものを食べている感覚がある。",
        "日中、身体の重さやだるさを感じることなく、快適に動けている。",
        "質の高い睡眠をとるために、夜の過ごし方を大切にしている。",
        "自分の身体からのサイン（疲れや痛み）に気づき、すぐにケアできている。"
    ],
    "繋がり (Connection)": [
        "本音を話せる信頼できるパートナーや友人がいる",
        "愛し愛されているという実感がある",
        "異なる価値観を持つ人とも、建設的な対話ができる",
        "本音で語り合える家族、パートナー、または友人がそばにいる。",
        "周囲の人に対して、感謝の気持ちを素直に伝えることができている。",
        "損得勘定抜きで、誰かのために行動することに喜びを感じる。",
        "孤独感を感じることは少なく、世界や社会と緩やかにつながっている感覚がある。",
        "自分とは違う考え方の人も受け入れ、対話を楽しむことができる。",
    ]
}

# 詳細フィードバック文章 (Definitions)
definitions = {
    "哲学 (Philosophy)": {
        "H": ("【確立】", "あなたは確かな「自分軸」を持っており、魂が喜ぶ選択を重ねてこられました。素晴らしいことです。一方で、その揺るがない信念が、時に周囲の人にとって「入り込みづらい壁」になっていないでしょうか？ あなたの正しさを少しだけ緩めたとき、世界はもっと優しく広がるかもしれません。"),
        "M": ("【模索】", "今、新しい価値観に触れながら「本当の自分」を探している最中ですね。その迷いは成長の証です。ただ、正解を探そうとして思考が止まってしまっていませんか？ 迷ったときは、頭で考えるのをやめて、あなたの「心が温かくなる方」を選んでみてください。"),
        "L": ("【不在】", "周囲の期待に応えようと、柔軟に合わせてきたあなたの優しさを感じます。でも、そのために自分の声を後回しにしすぎてはいませんか？ 誰かの人生を生きるのではなく、まずは1日5分だけ、あなた自身のために時間を使ってあげてください。")
    },
    "環境 (Environment)": {
        "H": ("【調和】", "心安らぐ場所と、経済的な安心感。あなたは今、とても豊かな土台の上に立っています。今の心地よさを十分に味わいつつ、もし心のどこかに「まだ行ける」という小さな灯火があるなら、少しだけ冒険の旅に出てみるのも素敵ですよ。"),
        "M": ("【均衡】", "日々の暮らしは守られており、その中でしっかりと役割を果たされていますね。一方で、「これで十分だ」と自分に言い聞かせて、小さな違和感に蓋をしていませんか？ あなたの感性が求めている「余白」や「遊び」を、生活の中に少し招き入れてみましょう。"),
        "L": ("【疲弊】", "今の環境に適応しようと、人一倍頑張ってきましたね。その忍耐強さは本当に立派です。でも、もう十分に戦いました。これ以上自分を削る必要はありません。「逃げる」ことは「負け」ではなく、大切なあなた自身を守るための「愛ある選択」です。")
    },
    "才能 (Talent)": {
        "H": ("【開花】", "あなたのギフト（才能）は、すでに誰かの笑顔を生み出しています。どうか自信を持ってください。ただ、今の「得意」に安住してしまうのはもったいないかもしれません。あなたの中には、まだ開けられていない才能の箱が眠っているはずですから。"),
        "M": ("【原石】", "「これかもしれない」という手応えを感じ始めていますね。その芽を大切にしましょう。もし「もっとすごくならないと」と焦っているなら、肩の力を抜いて。誰かに褒められるためではなく、あなたが「つい夢中になってしまう時間」を増やすだけで十分です。"),
        "L": ("【封印】", "慎重で謙虚なあなたは、まだ自分の輝きを過小評価しているようです。「私には何もない」と思っていませんか？ 実は、あなたが「当たり前にできていること」の中にこそ、最強の武器が隠されています。自分の良さを、もっと許してあげてください。")
    },
    "構想 (Vision)": {
        "H": ("【鮮明】", "理想の未来がクリアに見えていますね。人生の脚本家はあなた自身です。そのワクワクする景色を大切にしてください。もし足元が少しおろそかになっていると感じたら、遠くを見つめる時間を少し減らし、今日の一歩を愛でる時間を作ってみましょう。"),
        "M": ("【展望】", "「こうなったらいいな」という予感に胸を膨らませている状態ですね。その希望はとても大切です。その夢を「いつか」のままにせず、少しだけ解像度を上げてみませんか？ 具体的な「匂い」や「音」まで想像できたとき、現実は動き出します。"),
        "L": ("【漂流】", "目の前のことに誠実に向き合い、今日を懸命に生きています。その実直さはあなたの強みです。ただ、もし「どこへ向かっているんだろう」という不安があるなら、一度立ち止まって星を見上げてみましょう。現在地を知ることは、決して時間の無駄ではありませんよ。")
    },
    "健康 (Vitality)": {
        "H": ("【充実】", "生命力が溢れ、直感も冴え渡っていますね！ その高いエネルギーは、あなたの人生を切り拓く最高のギフトです。この万能感を楽しんでください。そして、走り続けるためにこそ、時にはあえてペースを落とし、羽を休める時間も自分にプレゼントしてあげましょう。"),
        "M": ("【維持】", "自分のリズムを保ち、大きな波風なく過ごせています。セルフケアができている証拠です。ただ、「なんとなくダルい」という身体の声を「いつものこと」と流していませんか？ その小さなサインを丁寧に拾うことで、あなたのパフォーマンスはもっと安定します。"),
        "L": ("【枯渇】", "気力だけで責任を果たしてきた、あなたの責任感の強さには頭が下がります。でも、身体は正直です。今は「頑張る」ことよりも「休む」ことが、あなたにとって一番大切な仕事です。泥のように眠ることを、どうか自分に許してあげてください。")
    },
    "繋がり (Connection)": {
        "H": ("【愛】", "あなたは愛し愛される喜びに包まれ、温かい安心感の中にいます。それは何にも代えがたい宝物です。その安全基地があるあなたなら、もう少し外の世界へ冒険に出ても大丈夫。異なる価値観を持つ人々との出会いが、あなたの愛をさらに深くするでしょう。"),
        "M": ("【協調】", "誰とでも円滑に関われるコミュニケーション能力をお持ちですね。素敵です。一方で、心の奥底にある「弱さ」を見せることに、少し怖さを感じていませんか？ 完璧でないあなたを見せたときこそ、本当の深い絆が結ばれるかもしれません。"),
        "L": ("【孤独】", "誰にも依存せず、独りで立ち続ける強さを持っています。その自立心は誇るべきものです。でも、もし心が張り詰めているなら、ほんの少しだけ荷物を降ろしてみませんか？ 世界はあなたが思っているよりも、ずっと優しくて温かい場所ですよ。")
    }
}

# --- 2. 判定ロジック (Archetype Logic) ---
def calculate_archetype(scores):
    phi = scores.get("哲学 (Philosophy)", 0)
    env = scores.get("環境 (Environment)", 0)
    tal = scores.get("才能 (Talent)", 0)
    des = scores.get("構想 (Vision)", 0)
    vit = scores.get("健康 (Vitality)", 0)
    con = scores.get("繋がり (Connection)", 0)
    
    min_score = min(scores.values())
    max_score = max(scores.values())

    # 1. Type 5 (統合された統治者) - 全て4.0以上
    if min_score >= 4.0:
        return "Type 5: 統合された統治者", "人生のあらゆる要素が調和し、あなたは自分の王国をしっかりと治めています。完璧に見える今だからこそ、あえて「隙」や「遊び」を作ることで、魅力はさらに深まるでしょう。", "👑"

    # 2. Type 1 (傷ついた戦士) - 健康<3.0 or 全体<2.5
    if vit < 3.0 or max_score < 2.5:
        return "Type 1: 傷ついた戦士", "責任感と優しさゆえに、あなたは誰よりも戦い続けてきました。でも、もう十分です。今はその重い鎧を脱いで、戦場から離れてみませんか？ 傷を癒やすことは、弱さではなく、次に進むための勇気ある選択です。", "🛡️"

    # 3. 複合タイプ
    if con >= 4.0 and des >= 4.0 and vit >= 3.5:
        return "Type 9: 求心力あるリーダー", "あなたの周りには自然と人が集まり、大きな渦が生まれます。皆の想いを背負って進むことができるリーダーです。期待に応えることも大切ですが、あなた自身の魂の純度を保つことが、結果として皆を幸せにします。", "🌞"
    if tal >= 4.0 and des >= 4.0:
        return "Type 13: 構想する建築家", "あなたの頭の中には、美しい未来の設計図が完成しています。その才能とビジョンは世界を変える力があります。あとは、それを現実に降ろすための「土台（環境）」作りが鍵となるでしょう。", "🏗️"
    if tal >= 4.0 and con >= 4.0:
        return "Type 10: 輝ける表現者", "あなたには人々を魅了する華があります。才能と愛嬌を兼ね備えたあなたは、ステージに立つべくして生まれた人。他者の評価よりも、あなた自身が「楽しむ」ことを最優先にしてください。", "🌟"
    if phi >= 4.0 and des >= 4.0:
        return "Type 7: 戦略的な策士", "確固たる信念と、未来を見通す目を持っています。感情に流されず、最短距離でゴールを目指す知性があります。その冷徹なまでの賢さに「愛敬」が加われば、あなたは無敵です。", "♟️"

    # 4. 単独タイプ
    if phi >= 4.0:
        return "Type 4: 哲学する賢者", "あなたは揺るがない「自分軸」と深い知恵を持っています。周囲の雑音に惑わされることはありません。その高潔な精神性を、今度は「他者」と分かち合うことで、あなたの世界はさらに広がります。", "🦉"
    if env >= 4.0:
        return "Type 2: 守り育てる守護者", "あなたには安心できる豊かな土台があります。周囲の人を守り、育てる包容力に溢れています。与えるばかりではなく、時にはあなた自身が「守られる」喜びも味わってください。", "🌳"
    if tal >= 4.0:
        return "Type 8: 孤高の職人", "卓越したスキルと才能を持っています。誰にも真似できないクオリティを生み出す力は、一種の魔法です。その才能を自分だけのものにせず、世界へのギフトとして開放する時が来ています。", "🔨"
    if des >= 4.0:
        return "Type 12: 夢見る旅人", "誰よりも遠くの未来を見ています。あなたの語る夢は、人々に希望を与えます。あとは「最初の一歩」を踏み出すだけ。夢を現実にするための泥臭い行動が、あなたを真の勇者にします。", "🌈"
    if vit >= 4.0:
        return "Type 6: 活気ある冒険家", "生命力とエネルギーに満ち溢れています。あなたの存在そのものが、周囲を明るく照らすパワーです。その有り余るエネルギーを、誰かのために使った時、伝説が始まります。", "🔥"
    if con >= 4.0:
        return "Type 11: 愛の人", "あなたの人生は愛と喜びに満ちています。人との繋がりこそがあなたのエネルギー源です。その温かさで周囲を癒やしつつ、時には自分自身の内なる声（哲学）にも耳を傾けてみてください。", "💞"

    # 5. デフォルト
    return "Type 3: 調和する市民", "あなたはバランス感覚に優れ、どのような環境でも適応できる柔軟性を持っています。今はまだ「これだ！」という武器が見つかっていないかもしれませんが、それは何にでもなれる可能性の証です。まずは一番低いスコアの要素を磨いてみましょう。", "🌱"

# --- 3. UI構築 ---

st.markdown('<div class="main-header">Life Mapping Diagnosis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">人生の現在地を測る 36の問い</div>', unsafe_allow_html=True)

# ★追加: 導入メッセージエリア
# ユーザーに安心感を与え、診断への没入感を高めます
st.markdown("""
<div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid #1E3A8A; color: #475569;">
    <p style="margin:0; line-height: 1.8;">
        ようこそ、Life Mappingへ！<br>
        この診断は、あなたの人生を構成する<b>6つの要素（哲学・環境・才能・構想・健康・繋がり）</b>の状態を可視化し、
        今あなたがどのような<b>「アーキタイプ（冒険者としてのタイプ）」</b>を生きているのかを紐解きます。<br><br>
        <b>所要時間は約2～3分です。</b><br>
        あまり深く考えすぎず、今の感覚に一番近いものを直感的に選んでください。<br>
        あなたの現在地を知ることが、理想の未来へ進むための最初の一歩になります。
    </p>
</div>
""", unsafe_allow_html=True)

# フォームなし（リアルタイム反映のため）
name = st.text_input("お名前 (Name)", placeholder="例: 山田 太郎")
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

if st.button("診断結果を表示する"):
    if not name:
        st.error("お名前を入力してください。")
    else:
        archetype_name, description, icon = calculate_archetype(user_scores)
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
            st.info(description)
            
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