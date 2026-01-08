import streamlit as st
import time

# ページ設定
st.set_page_config(page_title="RKT-Metrics Global Test", layout="centered")

# CSSで見た目を調整
st.markdown("""
<style>
.stTextArea textarea { font-size: 16px !important; }
.stTextInput input { font-size: 16px !important; }
/* ボタンのスタイル調整 */
div.stButton > button {
    background-color: #f0f2f6;
    border: 1px solid #d0d0d5;
    color: black;
    font-weight: bold;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# タイトル
st.title("📐 RKT-Metrics 総合診断テスト")
st.caption("Developed by RKT Global Team")
st.info("制限時間：15分 / Total Time: 15 min")

# ユーザー名入力
name = st.text_input("氏名 (Student Name):")

# セッション状態の初期化
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# 各問題の回答を保存するセッションステートを初期化
questions = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "reasoning"]
for q in questions:
    if q not in st.session_state:
        st.session_state[q] = ""

# --- 数学リモコン機能 (サイドバー) ---
with st.sidebar:
    st.header("🎛 数学リモコン")
    st.write("記号を入力したい場所を選んでください")
    
    # 入力先を選択
    target = st.radio(
        "入力ターゲット:",
        (
            "Q1 (因数分解)", "Q2 (二次関数)", "Q3 (三角比)", "Q4 (確率)", "Q5 (多面体)",
            "Q6 (円)", "Q7 (図形と式)", "Q8 (sin75)", "Q9 (積分)", "Q10 (数列)", 
            "Part2 (記述)"
        )
    )
    
    # ターゲットに対応するセッションキーを取得
    target_key = "reasoning" if "Part2" in target else target.split(" ")[0].lower()

    st.write("---")
    st.write("**記号パレット**")
    
    # 記号ボタン配置
    col1, col2, col3 = st.columns(3)
    
    def add_to_target(symbol):
        st.session_state[target_key] += symbol

    with col1:
        st.button("√", on_click=add_to_target, args=("√",))
        st.button("x²", on_click=add_to_target, args=("^2",))
    with col2:
        st.button("π", on_click=add_to_target, args=("π",))
        st.button("x³", on_click=add_to_target, args=("^3",))
    with col3:
        st.button("/", on_click=add_to_target, args=("/",))
        st.button("θ", on_click=add_to_target, args=("θ",))

    st.caption("※ボタンを押すと、選択したターゲットの末尾に入力されます。")

# --- テスト開始・タイマー処理 ---
if st.session_state.start_time is None:
    st.write("準備ができたらスタートボタンを押してください。")
    if st.button("🚀 テストを開始する (START)"):
        st.session_state.start_time = time.time()
        st.rerun()
else:
    # 経過時間の計算
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = 900 - elapsed_time

    # タイマー表示
    if remaining_time <= 0:
        st.error("⏰ TIME UP! テスト終了です。提出ボタンを押してください。")
    else:
        st.progress(max(0.0, remaining_time / 900))
        mins, secs = divmod(int(remaining_time), 60)
        st.metric("残り時間", f"{mins}分 {secs}秒")

    st.write("---")

    # === Part 1: Technique & Knowledge (必答問題) ===
    st.header("Part 1: 基礎・処理能力 (Q1~Q10)")
    
    # 問題リストとLaTeXデータ
    q_data = [
        ("Q1", r"x^{2}+2xy+x+y^{2}+y-6", "次の式を因数分解せよ"),
        ("Q2", r"3点 (0,2),(2,4),(-2,8)", "を通る二次関数の方程式を答えよ"),
        ("Q3", r"CA=\sqrt{7}, CB=3\sqrt{3}, \angle ABC=30^{\circ}", "のとき、ABを求めよ"),
        ("Q4", r"", "プレゼント交換で、自分で自分のプレゼントを選ばない確率を求めよ"),
        ("Q5", r"", "正十二面体の辺の数を求めよ"),
        ("Q6", r"中心が y=2x 上, 点(1,3)を通る, y軸に接する", "円の方程式を求めよ"),
        ("Q7", r"x^{2}+y^{2}-4y=0 が x+y-1=0", "から切り取る線分の長さを求めよ"),
        ("Q8", r"\sin 75^{\circ}", "の値を求めよ"),
        ("Q9", r"y=x^{2}+1 と y=2x, y=-2x", "に囲まれた図形の面積を求めよ"),
        ("Q10", r"a_{n}=1,2,4,8,16...", "第n項までの和を求めよ"),
    ]

    # ループで問題を表示 (keyをq1~q10に設定)
    for q_id, latex_text, q_text in q_data:
        st.write(f"**({q_id})** {q_text}")
        if latex_text:
            st.latex(latex_text)
        # keyを指定することで、サイドバーからの入力とリンクさせる
        st.text_input(f"{q_id}の回答:", key=q_id.lower())

    st.markdown("---")

    # === Part 2: Reasoning Selection (選択問題) ===
    st.header("Part 2: 思考タイプ選択 (Q11~Q13)")
    st.info("以下の3問から1つだけ選び、解答してください。選択肢を変えると問題が表示されます。")

    choice = st.radio("挑戦する問題を選択:", 
                      ("[11] 幾何 (Visual)", "[12] 代数 (Struct)", "[13] 論理 (Logic)"))

    st.markdown("### 選択した問題")
    if choice == "[11] 幾何 (Visual)":
        st.latex(r"\sqrt{x^{2}+1}+\sqrt{x^{2}-6x+18}\ge5 \text{ を示せ}")
    elif choice == "[12] 代数 (Struct)":
        st.latex(r"x^{4}-x^{3}+x^{2}+2 \text{ を因数分解せよ}") 
    elif choice == "[13] 論理 (Logic)":
        st.write("$p$ を5以上の素数とする。$p^{2}-1$ は必ず24の倍数であることを示せ")

    # 記述回答エリア
    st.text_area("記述回答欄 (サイドバーのターゲットを 'Part2' にして入力):", key="reasoning", height=200)

    st.write("---")
    
    # 提出ボタン
    if st.button("📩 回答を提出する (Submit)"):
        st.session_state.submitted = True
        # 全データを辞書にまとめる
        answers = {
            "Name": name,
            "Selection": choice,
            "Reasoning": st.session_state.reasoning
        }
        for i in range(1, 11):
            key = f"q{i}"
            answers[f"Q{i}"] = st.session_state[key]
        st.session_state.answers = answers

    # --- 提出後の表示処理 ---
    if st.session_state.submitted:
        st.success(f"提出完了！お疲れ様でした、{name}さん。")
        st.balloons()
        
        st.subheader("📝 提出データ確認（先生用）")
        st.json(st.session_state.answers)
        st.warning("※現在、この画面を閉じるとデータは消えます。記録する場合はスクリーンショットを撮ってください。")
