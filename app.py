import streamlit as st
from technology_answerers import (
    DockerAnswerer, CAnswerer, CPPAnswerer,
    CSharpAnswerer, GoAnswerer, KubernetesAnswerer
)
import json
import csv
from datetime import datetime
import math
import pandas as pd


# ===== 計算 NDCG@5 的函數 =====
def calculate_ndcg_at_5(scores, ground_truths):
    """
    計算 NDCG@5 指標
    scores: 用戶給出的評分 (0-3)
    ground_truths: 官方評分 (0-5)
    """
    dcg = 0
    for i, score in enumerate(scores[:5]):
        if score > 0:
            dcg += score / math.log2(i + 2)

    ideal_scores = sorted(ground_truths, reverse=True)[:5]
    idcg = 0
    for i, score in enumerate(ideal_scores):
        if score > 0:
            idcg += score / math.log2(i + 2)

    if idcg == 0:
        return 0
    ndcg = dcg / idcg

    return ndcg


# ===== 初始化 session state =====
if 'eval_results' not in st.session_state:
    st.session_state.eval_results = []

if 'eval_result' not in st.session_state:
    st.session_state.eval_result = None

if 'eval_history' not in st.session_state:
    st.session_state.eval_history = []

st.set_page_config(
    page_title="BackendDocAssistant (BDA)",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 BackendDocAssistant (BDA)")
st.write("官方文件智能檢索 - 基於 Perplexity Sonar API")

TECHNOLOGIES = {
    "🐳 Docker": DockerAnswerer,
    "🔤 C": CAnswerer,
    "⬆️ C++": CPPAnswerer,
    "#️⃣ C#": CSharpAnswerer,
    "🐹 Go": GoAnswerer,
    "☸️ Kubernetes": KubernetesAnswerer,
}

# 示例問題（用於評估模式）
EXAMPLE_QUESTIONS = [
    "Docker Compose 怎麼設定 volume？",
    "如何在 Docker 中使用 BuildKit？",
    "Kubernetes Service 和 Deployment 的區別？",
    "C++ 中的智能指針有哪幾種？",
    "Go 語言的 goroutine 和線程有什麼區別？",
]

# ============ 頁籤選擇 ============
tab1, tab2, tab3 = st.tabs(["📚 查詢模式", "📊 評估模式 (ML Demo)", "📈 評估統計"])

# ============ 標籤頁 1：查詢模式 ============
with tab1:
    # 側邊欄
    with st.sidebar:
        st.header("⚙️ 查詢設定")

        selected_tech_name = st.selectbox(
            "選擇技術棧",
            list(TECHNOLOGIES.keys()),
            key="tab1_tech"
        )

        selected_tech_class = TECHNOLOGIES[selected_tech_name]
        versions = selected_tech_class().get_versions()

        if selected_tech_name == "#️⃣ C#":
            version_display = [f"{c} + {d}" for c, d in versions]
            selected_idx = st.selectbox("版本選擇", range(len(version_display)),
                                        format_func=lambda i: version_display[i],
                                        key="tab1_version")
            selected_version = versions[selected_idx]
        else:
            selected_version = st.selectbox("版本選擇", versions, key="tab1_version2")

        st.info(f"📌 已選擇：{selected_tech_name} {selected_version}")

    # 主區域
    st.subheader("💬 提問")
    question = st.text_area(
        "輸入你的問題",
        placeholder="例如：如何在 Docker 中使用 BuildKit？",
        height=100,
        key="tab1_question"
    )

    col1, col2 = st.columns([4, 1])
    with col2:
        query_button = st.button("🔍 查詢", type="primary", use_container_width=True)

    if query_button:
        if not question.strip():
            st.warning("⚠️ 請先輸入問題。")
        else:
            with st.spinner(f"查詢 {selected_tech_name} 官方文件中..."):
                try:
                    answerer = TECHNOLOGIES[selected_tech_name]()
                    result = answerer.answer(question.strip(), version=selected_version)

                    # 顯示回答
                    st.markdown("---")
                    st.subheader("💬 AI 回答")
                    st.markdown(result["answer"])

                    # 顯示來源（改進版）
                    st.markdown("---")
                    st.subheader("📚 參考來源")

                    if result["sources"]:
                        for i, url in enumerate(result["sources"], 1):
                            st.markdown(f"[{i}]({url})")
                            st.caption(url)
                    else:
                        import re

                        urls_in_answer = re.findall(r'https?://[^\s\)]+', result["answer"])
                        if urls_in_answer:
                            st.info("✓ 來源已包含在回答內容中")
                            for url in set(urls_in_answer):
                                st.markdown(f"- [{url}]({url})")
                        else:
                            st.info("ℹ️ 未找到參考連結，請參考回答中的官方文件參考")

                    # 儲存查詢紀錄（選擇性）
                    if st.checkbox("💾 儲存此次查詢", key="save_query"):
                        save_feedback = st.selectbox(
                            "這個回答有幫助嗎？",
                            ["👍 有幫助", "👎 沒幫助", "⭐ 非常好"],
                            key="feedback_select"
                        )
                        st.success(f"感謝反饋：{save_feedback}")

                except Exception as e:
                    st.error(f"❌ 查詢失敗：{str(e)}")
                    st.error("請確認：\n1. .env 中有 PPLX_API_KEY\n2. API KEY 有效\n3. 網路連接正常")

# ============ 標籤頁 2：評估模式（ML Demo）============
with tab2:
    st.header("📊 Tab 2 - AI 回答評估")

    # 選擇問題
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_eval_question = st.selectbox(
            "選擇一個問題進行評估",
            options=EXAMPLE_QUESTIONS,
            key="eval_question"
        )

    with col2:
        if st.button("🚀 執行評估查詢", key="run_eval"):
            with st.spinner("正在查詢..."):
                try:
                    # ✅ 改這裡：用 DockerAnswerer 作示例（你可以改成其他技術）
                    answerer = DockerAnswerer()
                    result = answerer.answer(selected_eval_question)

                    # 模擬評估段落（因為 answerer 可能沒有返回這些）
                    if 'eval_paragraphs' not in result:
                        result['eval_paragraphs'] = [
                            {
                                'content': result['answer'][:200] + "...",
                                'ground_truth': 5
                            },
                            {
                                'content': "第二個關鍵點的內容",
                                'ground_truth': 4
                            },
                            {
                                'content': "第三個參考信息",
                                'ground_truth': 3
                            }
                        ]

                    st.session_state.eval_result = result
                    st.success("✅ 查詢成功")

                except Exception as e:
                    st.error(f"❌ 查詢失敗：{str(e)}")

    # 如果有評估結果，顯示評估界面
    if st.session_state.eval_result is not None:
        result = st.session_state.eval_result

        # ===== 新的評估說明 =====
        st.markdown("---")
        st.subheader("📊 評估 AI 的回答 - 幫助模型改進")

        st.info("""
💡 **評估說明**（以 AI 改進為目標）

👉 **你在評估什麼？**
AI 給出的回答是否準確、是否按照官方文件的最佳方式回答。

👉 **打分含義**（評估 AI 與官方標準答案的匹配度）
- **0 分** = AI 完全偏離官方（缺信息或有誤）
- **1 分** = AI 部分符合（有缺漏或錯誤）
- **2 分** = AI 大部分符合（涵蓋了大部分但不夠完整）
- **3 分** = AI 完全準確（涵蓋了所有關鍵點，準確清楚）

👉 **你的評分會幫助 AI：**
- 知道下次要涵蓋哪些關鍵點
- 學習怎樣更接近官方標準
- 知道怎樣給出更準確的回答

💡 **評估時問自己：**
✓ AI 有沒有提到所有關鍵配置？
✓ AI 的解釋是否準確、清楚？
✓ AI 有沒有遺漏或錯誤？
        """)

        # ===== 顯示 AI 的回答 =====
        st.markdown("---")
        st.subheader("📖 AI 的回答（需要被評估）")
        st.info(f"**問題：** {selected_eval_question}")

        ai_answer = result.get('answer', '')
        st.markdown(ai_answer)

        # ===== 顯示官方標準答案說明 =====
        st.markdown("---")
        st.subheader("📚 官方標準答案（評估標準）")
        st.write("下面是官方文件中對這個問題的標準答案。請比較 AI 的回答是否涵蓋了這些關鍵點。")
        st.markdown("---")

        # ===== 評估段落 =====
        eval_paragraphs = result.get('eval_paragraphs', [])

        if not eval_paragraphs:
            st.warning("⚠️ 沒有找到評估段落")
        else:
            scores = []

            for i, para in enumerate(eval_paragraphs):
                ground_truth = para.get("ground_truth", 0)

                # 顯示官方關鍵點
                importance_stars = "⭐" * ground_truth if ground_truth > 0 else "○"
                st.markdown(f"### 📌 官方關鍵點 {i + 1} - 重要性：{importance_stars}")

                # 根據重要性顯示說明
                if ground_truth == 5:
                    st.write("💎 **關鍵信息** - AI 的回答應該完全涵蓋這個點")
                elif ground_truth == 4:
                    st.write("⭐ **重要信息** - AI 的回答最好涵蓋這個點")
                else:
                    st.write("ℹ️ **參考信息** - AI 可以涵蓋這個點")

                # 顯示官方段落
                para_content = para.get('content', '')
                st.markdown(f"**官方說法：**\n{para_content}")

                # 評分滑塊
                score = st.slider(
                    f"AI 涵蓋這個點的程度",
                    min_value=0,
                    max_value=3,
                    value=0,
                    step=1,
                    key=f"score_{i}",
                    help="0=完全沒提到, 1=部分提到, 2=大部分準確, 3=完全準確"
                )

                scores.append(score)

                # 顯示評分說明
                score_text = {
                    0: "❌ AI 完全沒有涵蓋",
                    1: "△ AI 部分涵蓋（有缺漏）",
                    2: "✓ AI 大部分涵蓋（不夠完整）",
                    3: "✅ AI 完全準確"
                }
                st.write(f"**你的評分：** {score_text[score]}")

                st.markdown("---")

            # ===== 計算 NDCG@5 =====
            if st.button("🧮 計算 NDCG@5 指標", key="calc_ndcg"):
                if scores:
                    # 取得官方評分
                    ground_truths = [para.get("ground_truth", 0) for para in eval_paragraphs]

                    # 計算 NDCG@5
                    ndcg_score = calculate_ndcg_at_5(scores, ground_truths)

                    # 保存結果
                    eval_record = {
                        "question": selected_eval_question,
                        "scores": scores,
                        "ground_truths": ground_truths,
                        "ndcg": ndcg_score,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    st.session_state.eval_results.append(eval_record)
                    st.session_state.eval_history.append(eval_record)

                    # ===== 顯示結果 =====
                    st.markdown("---")
                    st.subheader("📊 評估結果 - AI 的改進方向")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("AI 準確度", f"{ndcg_score:.2%}")

                    with col2:
                        if ndcg_score >= 0.8:
                            st.success("✅ 優秀")
                        elif ndcg_score >= 0.7:
                            st.info("ℹ️ 良好")
                        else:
                            st.warning("⚠️ 需改進")

                    with col3:
                        improvement_space = (1.0 - ndcg_score) * 100
                        st.metric("改進空間", f"{improvement_space:.1f}%")

                    # 詳細反饋
                    st.success(f"""
✅ **評估完成！**

**AI 的準確度：{ndcg_score:.2%}**

**評估分析：**
""")

                    # 逐項分析
                    for i, (score, gt) in enumerate(zip(scores, ground_truths)):
                        if score < gt:
                            st.warning(f"⚠️ 關鍵點 {i + 1}：AI 的評分 {score}，期望 {gt}（缺漏或不準確）")
                        elif score == gt:
                            st.success(f"✅ 關鍵點 {i + 1}：完全符合")
                        else:
                            st.info(f"ℹ️ 關鍵點 {i + 1}：評分超出期望")

                    st.info("""
**建議：**
- 如果分數 < 0.7：AI 需要改進，可能遺漏或誤解了關鍵信息
- 如果分數 0.7-0.8：AI 表現良好，可以進一步完善細節
- 如果分數 > 0.8：AI 表現優秀，已很接近官方標準

進入 **Tab 3** 查看改進趨勢！
                    """)
                else:
                    st.warning("⚠️ 請先給出評分")

# ============ 標籤頁 3：評估統計 ============
with tab3:
    st.subheader("📈 評估統計與機器學習進度")

    if st.session_state.eval_history and len(st.session_state.eval_history) > 0:
        eval_history = st.session_state.eval_history

        # 顯示歷史紀錄
        st.write(f"**累計評估次數**：{len(eval_history)}")

        # 計算平均 NDCG
        ndcg_scores = [record['ndcg'] for record in eval_history]
        avg_ndcg = sum(ndcg_scores) / len(ndcg_scores)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("平均 NDCG@5", f"{avg_ndcg:.3f}")
        with col2:
            st.metric("最高 NDCG@5", f"{max(ndcg_scores):.3f}")
        with col3:
            st.metric("最低 NDCG@5", f"{min(ndcg_scores):.3f}")

        # 折線圖
        chart_data = pd.DataFrame({
            "NDCG@5": ndcg_scores,
            "目標 (0.7)": [0.7] * len(ndcg_scores),
            "優秀 (0.8)": [0.8] * len(ndcg_scores),
        })
        st.line_chart(chart_data)

        # 詳細記錄表
        st.subheader("詳細評估記錄")
        history_df = []
        for idx, record in enumerate(eval_history, 1):
            history_df.append({
                "序號": idx,
                "時間": record['timestamp'],
                "問題": record['question'][:40] + "...",
                "NDCG@5": f"{record['ndcg']:.3f}",
            })

        st.dataframe(history_df, use_container_width=True)

        # 導出結果
        if st.button("📥 導出評估結果為 CSV", key="export_eval"):
            csv_str = "timestamp,question,ndcg\n"
            for record in eval_history:
                csv_str += f"{record['timestamp']},\"{record['question']}\",{record['ndcg']}\n"

            st.download_button(
                label="下載 CSV",
                data=csv_str,
                file_name=f"bda_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        st.info("""
        **機器學習意義**：
        - 這些評估結果代表我們的檢索系統在標準資料集上的表現。
        - 通過累積這些評估，我們可以：
          1. 追蹤系統性能改進
          2. 發現哪些問題類型表現較差
          3. 優化檢索策略與超參數
          4. 未來用這些資料微調檢索模型
        """)

    else:
        st.info("📊 尚無評估記錄。請先在「評估模式」中執行評估。")

# 頁尾
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.8rem;'>"
    "🚀 BackendDocAssistant (BDA) | 基於 Perplexity Sonar API<br>"
    "含機器學習檢索評估與優化功能"
    "</div>",
    unsafe_allow_html=True
)