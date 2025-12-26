# backend-doc-assistant
BackendDocAssistant (BDA) | 後端開發文件檢索 AI 助手
完整計畫書
專案名稱：BackendDocAssistant (BDA) - MVP 版本
專案簡述：面向後端開發者的 AI 文件檢索與版本感知查詢系統
項目類別：人工智能 + 機器學習 + 後端工程
計畫期間：2025 年 12 月 26 日 ~ 2025 年 1 月 8 日（2 週）
預期交付物：完整計畫書 + 可運行的 MVP Demo + GitHub 代碼倉庫

第一部分：項目背景與動機
1.1 問題陳述
在後端開發工作中，開發者面臨的核心問題：

文件查詢效率低

官方文件結構複雜，跨越多個頁面才能找到所需信息

尋找文件與官方範例平均耗時 15-20% 的開發時間

版本混淆成本高

不同版本的 API 使用方式差異大（如 Docker 19.03 vs 24.0）

開發者常面臨「用了過時的方法」或「查詢結果不適用當前版本」的問題

現有 AI 工具的限制

通用大型語言模型（ChatGPT、Gemini）易幻想答案，無明確版本保證

答案難以溯源，開發者難以驗證準確性

未針對「技術文件」進行專門優化

1.2 項目的創新點
BackendDocAssistant 的差異化：

特性	通用 LLM	GitHub Copilot	官方文件搜尋	BDA
版本感知	❌	❌	⚠️ 手動	✅ 自動
答案溯源	❌	❌	✅	✅
構造化回答	⚠️	⚠️	⚠️	✅
遷移指南	❌	❌	❌	✅
聚焦後端技術	❌	⚠️	✅	✅
第二部分：項目範圍與目標
2.1 MVP 版本的範圍定義
聚焦技術：Docker（官方文件）

版本覆蓋：

Docker 18.09

Docker 19.03

Docker 20.10

Docker 23.0

Docker 24.0

文件規模：~200-300 個清潔段落

為什麼選 Docker？

官方文件精簡且結構清晰（相比 Kubernetes）

開發者查詢頻繁，痛點明確

版本差異顯著，適合驗證「版本感知」功能

易於複製到其他技術棧（Go、Kubernetes 等）

2.2 MVP 的核心功能（3 大功能）
功能 1：版本感知型文件檢索
用戶場景：

text
輸入：「怎麼在 Docker 20.10 中使用 BuildKit？」
輸出：
  ✅ 來源：Docker Official Documentation, v20.10
  ✅ 段落：[相關的官方文件摘錄]
  ✅ 回答：[AI 生成的簡潔說明]
  ✅ 連結：https://docs.docker.com/...
實現方式：

向量檢索（Sentence-Transformers embedding）

版本過濾規則（移除不適用版本的結果）

結構化輸出（來源、段落、回答）

功能 2：版本間差異對比
用戶場景：

text
輸入：「Docker 19.03 升級到 24.0，有什麼破壞性改變？」
輸出：
  ✅ 版本對比表（主要改變列表）
  ✅ 遷移步驟（逐步說明）
  ✅ 風險標記（需要特別注意的項目）
實現方式：

檢索不同版本的官方文件

提取變更信息（从 Release Notes、Change Logs）

使用 LLM 生成結構化對比與遷移指南

功能 3：簡單的文件推薦
用戶場景：

text
輸入：「我想用 Docker 做持續集成，應該看哪些文件？」
輸出：
  ✅ 推薦文章 1：Docker in CI/CD
  ✅ 推薦文章 2：Best Practices for Building Images
  ✅ 推薦文章 3：Volume Management
實現方式：

基於查詢意圖推薦相關文檔

不需要複雜的推薦算法（簡單的向量相似度即可）

2.3 MVP 的目標與成功指標
技術指標
指標	目標值	評估方法
檢索準確度 (NDCG@5)	≥ 0.70	20-30 個測試查詢
版本過濾準確度	≥ 0.80	人工檢核
平均回應時間	< 2 秒	性能監測
代碼覆蓋率	≥ 70%	單元測試
用戶體驗指標
指標	目標值	說明
Demo 可用性	100%	可在本地運行，無依賴問題
答案完整度	≥ 0.80	回答覆蓋用戶需求的程度
引用準確度	≥ 0.90	引用段落確實支持答案
第三部分：技術設計
3.1 系統架構
text
┌─────────────────────────────────┐
│      使用者查詢 (Streamlit UI)   │
└────────────┬────────────────────┘
             │ "Docker 20.10 怎麼用 BuildKit?"
             ▼
┌─────────────────────────────────┐
│   查詢理解與版本提取              │
│   (簡單的 regex + 關鍵詞匹配)    │
└────────────┬────────────────────┘
             │ query="BuildKit", version="20.10"
             ▼
┌─────────────────────────────────┐
│   文檔段落檢索                   │
│   (向量相似度搜尋)               │
│   - Embedding: Sentence-Transformers
│   - Index: Faiss                │
└────────────┬────────────────────┘
             │ top-3 相關段落
             ▼
┌─────────────────────────────────┐
│   版本相關性過濾                  │
│   (簡單規則：匹配版本標籤)        │
└────────────┬────────────────────┘
             │ 過濾後的相關段落
             ▼
┌─────────────────────────────────┐
│   LLM 答案生成                   │
│   (OpenAI GPT-3.5 API)          │
│   - Prompt 工程                 │
│   - 引用生成                    │
└────────────┬────────────────────┘
             │ 自然語言回答 + 引用
             ▼
┌─────────────────────────────────┐
│   結果展示與引用                  │
│   - 答案                        │
│   - 來源 URL                    │
│   - 段落內容                    │
└─────────────────────────────────┘
3.2 技術棧選擇
層次	技術選擇	原因
數據爬蟲	BeautifulSoup4 + Selenium	簡單、快速、無複雜依賴
Embedding	Sentence-Transformers (all-MiniLM-L6-v2)	開源、輕量、效果好、本地運行
向量索引	Faiss	快速、無需外部服務、易整合
LLM	OpenAI GPT-3.5 Turbo	API 簡單、成本低（<$1）、效果穩定
Web UI	Streamlit	快速開發、無需前端知識、易部署
版本控制	Git + GitHub	標準做法、便於展示與協作
3.3 機器學習任務設計
任務 1：文檔段落檢索（Document Retrieval）
任務類型：向量檢索 + 排序

模型方案：

Embedding 模型：sentence-transformers/all-MiniLM-L6-v2（預訓練，無需微調）

向量資料庫：Faiss（本地構建）

檢索方法：余弦相似度 + Top-K 返回

訓練資料需求：

200-300 個官方文檔段落（自動爬蟲獲得）

20-30 個「查詢-段落」標註對（用於評估）

不需要新建訓練集，使用預訓練模型

評估指標：

NDCG@5（Normalized Discounted Cumulative Gain）

Precision@5（前 5 個結果的相關性）

任務 2：版本相關性判斷（Version Filtering）
任務類型：規則型過濾（不使用 ML 模型）

過濾規則：

python
def filter_by_version(passages, user_version):
    """
    移除明顯不適用該版本的段落
    規則：
    1. 移除版本號比用戶版本明顯新的段落（可能涉及新功能）
    2. 移除標記為"deprecated"的段落
    3. 優先排序與用戶版本完全匹配的段落
    4. 次優排序同主版本的段落（如 20.10.x）
    """
    # 實現邏輯見代碼
為什麼不用 ML 模型？

時間限制（3 週內需要成品）

標註數據有限

簡單規則已能達到 80% 的準確率

後期迭代時可加入微調模型

任務 3：答案生成（Answer Generation）
任務類型：文本生成（使用現成 LLM，無需訓練）

模型方案：

LLM：OpenAI GPT-3.5 Turbo（或 Claude 備選）

方法：Prompt 工程 + Few-shot learning

Prompt 設計：

text
You are a Docker documentation expert.

User Query: {user_query}

Relevant Documentation Passages:
{passages}

Instructions:
1. Provide a clear, concise answer based on the documentation
2. Include citations like [Ref 1], [Ref 2] etc.
3. If information is not in the documentation, say so
4. Prefer official examples and best practices

Answer:
成本估算：

200-300 次查詢 × ~200 tokens/query = ~60K tokens

成本：~60K × $0.001 / 1K tokens = $0.06（非常便宜）

3.4 數據準備策略
數據來源
來源	內容	收集方法
官方文檔	Docker docs (v18.09-24.0)	爬蟲 (BeautifulSoup + Selenium)
Release Notes	版本變更記錄	爬蟲 + 手動整理
FAQ	常見問題	爬蟲
數據處理流程
text
Raw HTML
  ↓
清理 (去除導航、廣告、腳本)
  ↓
段落分割 (按標題或固定字數)
  ↓
版本標記 (記錄每段來源版本)
  ↓
向量化 (Sentence-Transformers)
  ↓
建立索引 (Faiss)
  ↓
準備評估集 (20-30 查詢 + 標註)
預期規模
項目	數量	人工工作量
官方文檔段落	200-300	0（自動爬蟲）
清潔檢查	10-20 樣本	1-2 小時
評估查詢集	20-30	2-3 小時
版本標記驗證	全部	1 小時
總計		4-6 小時
第四部分：項目計畫與時間表
4.1 3 週的詳細時間表
第 1 週（Dec 26 - Jan 1）：基礎準備
目標：搭建基礎架構 + 收集數據

日期	任務	交付物
Dec 26-27	範圍確定 + 開發環境設置	GitHub repo 初始化 + 環境配置說明
Dec 28-29	Docker 官方文檔爬蟲開發	爬蟲代碼 + 200-300 段落的原始語料
Dec 30	數據清理 + 版本標記	清潔版本語料庫 (CSV 格式)
Dec 31 - Jan 1	計畫書初稿 + 評審	完整計畫書 v1.0
每日檢查清單：

 Dec 27 晚：虛擬環境建立，依賴安裝完成

 Dec 29 晚：爬蟲運行，成功提取 200+ 段落

 Dec 30 晚：清潔數據驗證，版本標籤完整

 Jan 1 晚：計畫書初稿完成，GitHub repo 整潔

第 2 週（Jan 2 - Jan 8）：核心系統開發
目標：實現檢索 + 版本過濾 + LLM 整合

日期	任務	交付物
Jan 2-3	向量化 + Faiss 索引建立	可查詢的向量索引
Jan 4-5	版本過濾規則開發	版本過濾模組 + 測試用例
Jan 6-7	LLM 整合 + Prompt 優化	答案生成模組 + 引用機制
Jan 7	整合測試	端到端工作流驗證
每日檢查清單：

 Jan 3 晚：python test_retrieval.py 返回合理結果

 Jan 5 晚：版本過濾規則正確率 ≥ 80%

 Jan 7 晚：10 個測試查詢能生成回答，格式正確

第 3 週（Jan 9 - Jan 15）：UI + 優化 + 最終準備
目標：可展示的 Demo + 完整文檔

日期	任務	交付物
Jan 9-10	Streamlit Web UI 開發	可運行的 Web 應用
Jan 11-12	性能優化 + Bug 修復	穩定的系統，平均回應 < 2 秒
Jan 13-14	評估 + 結果報告	評估報告 (準確度、性能)
Jan 15	Demo 最終檢查 + 文檔完善	可展示的成品
每日檢查清單：

 Jan 10 晚：streamlit run app.py 可在瀏覽器打開

 Jan 12 晚：20 個測試查詢全部運行成功

 Jan 14 晚：評估報告完成，指標達成

 Jan 15 晚：GitHub repo 整潔，README 清晰，可一鍵運行

4.2 交付物清單（Jan 16）
交付物 1：計畫書
 完整的 AI 設計文檔（本文件的擴展版）

 3 週進度報告

 技術評估與改進方向

格式：Word / PDF，可直接打印或提交

交付物 2：代碼倉庫（GitHub）
text
backend-doc-assistant/
├── README.md                          # 使用說明 + 快速開始
├── PLAN.md                            # 計畫書
├── EVALUATION_REPORT.md               # 評估報告
├── requirements.txt                   # 依賴列表
├── .gitignore
│
├── data/
│   ├── docker_docs.csv               # 爬蟲結果（段落 + 版本）
│   └── docker_faiss.index            # 向量索引
│
├── src/
│   ├── __init__.py
│   ├── crawler.py                    # 網頁爬蟲
│   ├── data_cleaner.py               # 數據清理
│   ├── vectorizer.py                 # 向量化
│   ├── retrieval.py                  # 檢索系統
│   ├── version_filter.py             # 版本過濾規則
│   ├── llm_integration.py            # LLM 調用
│   └── utils.py                      # 工具函數
│
├── app.py                             # Streamlit 應用主文件
├── tests/
│   ├── test_retrieval.py             # 檢索測試
│   ├── test_version_filter.py        # 版本過濾測試
│   └── test_integration.py           # 端到端測試
│
└── demo_queries.txt                   # 示例查詢
交付物 3：可運行的 Demo
bash
# 一鍵運行
git clone <repo_url>
cd backend-doc-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key"
streamlit run app.py
交付物 4：評估報告
內容包括：

檢索準確度 (NDCG@5, Precision@5)

版本過濾準確度

系統性能 (延遲、吞吐量)

已知限制與改進方向

用戶反饋 (如有)

第五部分：風險管理與應對方案
5.1 主要風險識別
風險	發生機率	影響程度	應對方案
OpenAI API 額度不足	低	中	切換到 Claude 或本地 Llama 2
Docker 文檔爬蟲失敗	中	高	手動下載 HTML，改進爬蟲邏輯
向量檢索精度不足	中	中	調整 embedding 模型或搜尋參數
Streamlit 部署問題	低	中	改用 Flask + 簡單前端
時間不夠	中	高	減少測試用例，優先核心功能
版本標記不準	中	中	人工檢核 + 改進規則
5.2 應對策略
時間壓力的應對：

優先完成：爬蟲 → 向量索引 → Streamlit UI

可延遲到 Phase 2：高級版本過濾、License 分析、IDE 插件

質量保證：

每天執行單元測試 (pytest)

每週評估準確度指標

如數據質量不達預期，及時調整

第六部分：成功標準
6.1 硬指標（必須達成）
✅ GitHub repo 可運行，streamlit run app.py 不出錯

✅ 20 個測試查詢能生成合理回答

✅ 每個查詢返回相關段落 + 版本標籤 + 連結

✅ 平均回應時間 < 3 秒

✅ README + 計畫書完整清晰

6.2 軟指標（優先達成）
✅ 檢索準確度 (NDCG@5) ≥ 0.70

✅ 版本過濾準確度 ≥ 0.80

✅ 答案引用準確度 ≥ 0.85

✅ 代碼註釋清楚，便於理解與擴展

✅ Demo 展示效果直觀

第七部分：後續擴展方向（Phase 2 及之後）
Phase 2（1 月 17 日 - 2 月 28 日）：擴展到多技術
 複製 Docker 的 pipeline 到 Go 官方文檔

 複製到 Kubernetes 官方文檔

 複製到 C# 官方文檔

 統一管理多技術的版本與索引

 實施版本相關性的 ML 分類器（用真實標註數據微調 BERT）

Phase 3（3 月 - 4 月）：加入進階功能
 License 與合規性分析模組

 錯誤訊息對應官方文檔

 最佳實踐建議

 實時文檔監控（官方文檔更新時自動重新索引）

Phase 4（5 月及以後）：產品化
 部署到雲端 (AWS / Google Cloud)

 開發 VSCode / JetBrains IDE 插件

 用戶認證 + 使用統計

 API 公開，供第三方整合

 社群協作改進（眾包標註）

第八部分：技術亮點與創新
8.1 創新之處
版本感知的文檔檢索

首次在後端開發工具中，系統地處理「版本」這一維度

不僅找到相關文檔，還確保版本適用性

高可驗證性

每個答案都附帶來源 URL 和原文段落

用戶可以一鍵驗證

聚焦後端開發者

不是通用 AI，而是為特定用戶群體優化

更精準的答案與建議

可複製的架構

完整的 pipeline（爬蟲 → 向量化 → 檢索 → 生成）

易於複製到其他技術棧（Go、Kubernetes、C# 等）

8.2 研究價值
本項目涉及的技術方向：

信息檢索：密集檢索 (Dense Retrieval) 在技術文檔上的應用

RAG（檢索增強生成）：結合向量檢索與 LLM 生成

版本控制與知識圖譜：多版本信息的管理與聚合

Prompt 工程：如何設計提示詞以生成高質量的技術回答

第九部分：預算概估
9.1 費用明細
項目	數量	單價	合計
OpenAI API (GPT-3.5)	200-300 queries	$0.001/1K tokens	< $1
Sentence-Transformers	開源	免費	$0
Faiss	開源	免費	$0
Streamlit	免費版本	免費	$0
GitHub	免費公開倉庫	免費	$0
合計			< $5
結論：項目成本極低，主要是時間投入。

第十部分：團隊與資源
10.1 團隊組成
角色	人數	責任
AI/ML 工程師	1	模型選擇、數據準備、系統開發
後端工程師	1 (同上)	API 開發、系統整合
QA/測試	1 (同上)	測試用例、評估指標
Note：此項目由 1 人全職完成。

10.2 必需資源
開發機器：能運行 Python 3.11+，4GB+ RAM（標準筆電足夠）

網絡：穩定互聯網（用於 API 調用）

API Key：OpenAI API 免費試用額度或自備（成本 < $1）

工具軟件：VS Code、Git 等（均開源免費）

第十一部分：附錄
11.1 參考資源
技術文檔：

Hugging Face Transformers：https://huggingface.co/transformers/

Faiss Wiki：https://github.com/facebookresearch/faiss

Streamlit Docs：https://docs.streamlit.io/

OpenAI API：https://platform.openai.com/docs/

研究論文：

Dense Passage Retrieval (Facebook AI Research)

REALM: Retrieval-Augmented Language Model

Attention Is All You Need (Transformer)

相關項目：

LangChain：https://github.com/langchain-ai/langchain

Llama Index：https://www.llamaindex.ai/

ColBERT：Dense Retrieval 的最新進展

11.2 詞彙表
詞彙	解釋
Embedding	將文本轉換為向量的過程
RAG	檢索增強生成 (Retrieval-Augmented Generation)
NDCG	歸一化折扣累積增益，用於評估排序質量
Faiss	Facebook AI 相似度搜索庫
Prompt Engineering	設計提示詞以指導 AI 模型的過程
MVP	最小可行產品 (Minimum Viable Product)
Dense Retrieval	使用密集向量進行文檔檢索
第十二部分：簽署與確認
計畫書版本：v1.0
編制日期：2025 年 12 月 26 日
預計交付日期：2025 年 1 月 8 日

確認事項：

 項目範圍清晰（只做 Docker，3 週內）

 技術方案可行（預訓練模型 + 規則過濾）

 時間計畫現實（3 週內交付 MVP）

 成本可控（< $5）

 團隊資源充足（1 人全職）
