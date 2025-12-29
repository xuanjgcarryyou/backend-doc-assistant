import streamlit as st
from technology_answerers import (
    DockerAnswerer, CAnswerer, CPPAnswerer,
    CSharpAnswerer, GoAnswerer, KubernetesAnswerer
)

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

# 側邊欄
with st.sidebar:
    st.header("⚙️ 查詢設定")

    selected_tech_name = st.selectbox(
        "選擇技術棧",
        list(TECHNOLOGIES.keys()),
    )

    selected_tech_class = TECHNOLOGIES[selected_tech_name]
    versions = selected_tech_class().get_versions()

    if selected_tech_name == "#️⃣ C#":
        version_display = [f"{c} + {d}" for c, d in versions]
        selected_idx = st.selectbox("版本選擇", range(len(version_display)),
                                    format_func=lambda i: version_display[i])
        selected_version = versions[selected_idx]
    else:
        selected_version = st.selectbox("版本選擇", versions)

    st.info(f"📌 已選擇：{selected_tech_name} {selected_version}")

# 主區域
question = st.text_area(
    "輸入你的問題",
    placeholder="例如：如何在 Docker 中使用 BuildKit？",
    height=100
)

if st.button("🔍 查詢官方文件", type="primary"):
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

                # 顯示來源
                st.markdown("---")
                st.subheader("📚 參考來源")

                if result["sources"]:
                    for i, url in enumerate(result["sources"], 1):
                        st.markdown(f"[{i}] [{url}]({url})")
                else:
                    st.info("ℹ️ 來源已在回答中標註")

            except Exception as e:
                st.error(f"❌ 查詢失敗：{str(e)}")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>🔧 BackendDocAssistant (BDA) | 基於 Perplexity Sonar API</div>",
    unsafe_allow_html=True)
