import streamlit as st
from answerer import DocAnswerer

st.set_page_config(
    page_title="Docker Doc Assistant (BDA)",
    layout="wide"
)

st.title("🐳 BackendDocAssistant (BDA)")
st.write("針對 Docker 官方文件的版本感知檢索助手（基於 Perplexity Sonar）")


@st.cache_resource
def get_answerer():
    return DocAnswerer()


# 側邊欄：版本選擇（從 v0.6.7 到 v29.0）
with st.sidebar:
    st.header("查詢設定")

    # Docker 版本列表（依你提供的 deprecated 表格）
    versions = [
        "latest", "v29.0", "v28.4", "v28.3", "v28.2", "v28.0",
        "v27.0", "v26.0", "v25.0", "v24.0", "v23.0", "v20.10",
        "v19.03", "v18.09", "v18.06", "v17.12", "v17.10", "v17.09",
        "v17.06", "v17.05", "v1.13", "v1.12", "v1.11", "v1.10",
        "v1.9", "v1.8", "v1.6", "v0.10", "v0.6.7"
    ]

    version = st.selectbox(
        "Docker 版本",
        versions,
        index=0,
    )

    st.info(f"目前選擇：{version}")

# 主區：輸入問題
question = st.text_input(
    "請輸入你的問題：",
    placeholder="例如：Docker BuildKit 要如何啟用？"
)

if st.button("🔍 查詢官方文件", type="primary"):
    if not question.strip():
        st.warning("請先輸入問題。")
    else:
        with st.spinner("查詢中，請稍候..."):
            answerer = get_answerer()
            result = answerer.answer(question.strip(), version=version)

        # 顯示回答
        st.subheader("AI 回答")
        st.markdown(result["answer"])

        # 顯示來源文件（滾動視窗）
        st.subheader("參考來源")
        if not result["sources"]:
            st.write("未找到額外來源連結（可能已在回答中引用）。")
        else:
            # 用滾動區塊顯示多個來源
            with st.container():
                for i, url in enumerate(result["sources"], start=1):
                    st.markdown(f"[{i}] [{url}]({url})")
