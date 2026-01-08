import streamlit as st
import time

# ページ設定
st.set_page_config(page_title="RKT-Metrics Global Test", layout="centered")

# CSSで見た目を調整
st.markdown("""
<style>
.stTextArea textarea { font-size: 16px !important; }
.stTextInput input { font-size: 16px !important; }
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

# --- テスト開始・タイマー処理 ---
if st.session_state.start_time is None:
    st.write("準備ができたらスタートボタンを押してください。")
    if st.button("🚀 テストを開始する (START)"):
        st.session_state.start_time = time.time()
        st.rerun()
else:
    # 経過時間の計算
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = 900 - elapsed_time  # 900秒 = 15分

    # タイマー表示
    if remaining_time <= 0:
        st.error("⏰ TIME UP! テスト終了です。提出ボタンを押してください。")
    else:
        # 残り時間をバーと数値で表示
        st.progress(max(0.0, remaining_time / 900))
        mins, secs = divmod(int(remaining_time), 60)
        st.metric("残り時間", f"{mins}分 {secs}秒")

    st.write("---")

    # === Part 1: Technique & Knowledge (必答問題) ===
    st.header("Part 1: 基礎・処理能力 (Q1~Q10)")
    
    # フォーム作成
    with st.form("rkt_test_form"):
        # [cite_start]PDFの問題内容 [cite: 1-10]
        st.write("**(1)** 次の式を因数分解せよ")
        st.latex(r"x^{2}+2xy+x+y^{2}+y-6")
        a1 = st.text_input("A1", key="q1")

        st.write("**(2)** 3点 $(0,2),(2,4),(-2,8)$ を通る二次関数の方程式を答えよ")
        a2 = st.text_input("A2", key="q2")

        st.write("**(3)** $\\triangle ABC$について、$CA=\\sqrt{7}, CB=3\\sqrt{3}, \\angle ABC=30^{\\circ}$ のとき、$AB$を求めよ")
        a3 = st.text_input("A3", key="q3")

        st.write("**(4)** 1人1つプレゼントを持ち寄り、3人でプレゼント交換を行う。全員無作為にプレゼントを選ぶとき、自分で自分のプレゼントを選ばない確率を求めよ")
        a4 = st.text_input("A4", key="q4")

        st.write("**(5)** 正十二面体の辺の数を求めよ")
        a5 = st.text_input("A5", key="q5")

        st.write("**(6)** 中心が直線 $y=2x$ 上にあり、y軸に接する、点 $(1,3)$ を通る円の方程式を求めよ")
        a6 = st.text_input("A6", key="q6")

        st.write("**(7)** 円 $x^{2}+y^{2}-4y=0$ が直線 $x+y-1=0$ から切り取る線分の長さを求めよ")
        a7 = st.text_input("A7", key="q7")

        st.write("**(8)** $\\sin 75^{\\circ}$ の値を求めよ")
        a8 = st.text_input("A8", key="q8")

        st.write("**(9)** $y=x^{2}+1$ と $y=2x, y=-2x$ に囲まれた図形の面積を求めよ")
        a9 = st.text_input("A9", key="q9")

        st.write("**(10)** 数列 $a_{n}=1,2,4,8,16...$ であるとき、第n項までの和を求めよ")
        a10 = st.text_input("A10", key="q10")

        st.markdown("---")

        # === Part 2: Reasoning Selection (選択問題) ===
        st.header("Part 2: 思考タイプ選択 (Q11~Q13)")
        st.info("以下の3問から1つだけ選び、解答してください。")
        choice = st.radio("挑戦する問題を選択:", 
                          ("[11] 幾何的証明 (Visual)", 
                           "[12] 構造的代数 (Struct)", 
                           "[13] 論理的証明 (Logic)"))

        st.markdown("### 選択した問題")
        
        # 選択肢に応じて問題を表示
        if choice == "[11] 幾何的証明 (Visual)":
            st.write("**選択(11)** すべての実数 $x$ について、次の不等式を示せ")
            st.latex(r"\sqrt{x^{2}+1}+\sqrt{x^{2}-6x+18}\ge5")
        
        elif choice == "[12] 構造的代数 (Struct)":
            st.write("**選択(12)** 次の式を因数分解せよ")
            st.latex(r"x^{4}-x^{3}+x^{2}+2") 
            
        elif choice == "[13] 論理的証明 (Logic)":
            st.write("**選択(13)** $p$ を5以上の素数とする。$p^{2}-1$ は必ず24の倍数であることを示せ")

        # 記述回答エリア
        reasoning_answer = st.text_area("記述回答欄 (証明や途中式も記入):", height=200)

        st.write("---")
        
        # 提出ボタン
        submitted = st.form_submit_button("📩 回答を提出する (Submit)")
        
        if submitted:
            st.session_state.submitted = True
            st.session_state.answers = {
                "Name": name,
                "Q1": a1, "Q2": a2, "Q3": a3, "Q4": a4, "Q5": a5,
                "Q6": a6, "Q7": a7, "Q8": a8, "Q9": a9, "Q10": a10,
                "Selection": choice,
                "Reasoning": reasoning_answer
            }

    # --- 提出後の表示処理 ---
    if st.session_state.submitted:
        st.success(f"提出完了！お疲れ様でした、{name}さん。")
        st.balloons()
        
        st.subheader("📝 提出データ確認（先生用）")
        st.json(st.session_state.answers)
        st.warning("※現在、この画面を閉じるとデータは消えます。記録する場合はスクリーンショットを撮ってください。")
