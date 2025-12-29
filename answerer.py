from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class DocAnswerer:
    """使用 Perplexity Sonar 搜尋 Docker 官方文件並附上來源"""

    def __init__(self):
        api_key = os.getenv("PPLX_API_KEY")
        if not api_key:
            raise RuntimeError("請在 .env 設定 PPLX_API_KEY")

        # Perplexity Sonar API（相容 OpenAI 格式）
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai",
        )

    def answer(self, query: str, version: str = "latest") -> dict:
        """
        輸入問題與版本，Sonar 搜尋並回答
        回答會自動附上來源引用
        """

        # Prompt 設計：限制 Sonar 只查 Docker 官方文件
        prompt = f"""
你是 Docker 官方文件專家。根據 Docker 官方文件（[https://docs.docker.com/](https://docs.docker.com/)）回答問題。

限制條件：
1. 只使用 Docker 官方來源（docs.docker.com）
2. 對於 Docker {version} 版本，如果功能已 deprecated 或 removed，明確說明
3. 回答結尾必須列出所有引用來源的 URL，格式如下：

   參考資料：
   [1] https://docs.docker.com/...
   [2] https://docs.docker.com/...

4. 回答請用繁體中文，3-5 段即可

用戶查詢版本：Docker {version}

用戶問題：{query}
"""

        completion = self.client.chat.completions.create(
            model="sonar",  # Perplexity Sonar 模型，內建網路搜尋
            messages=[
                {
                    "role": "system",
                    "content": "你是專業的 Docker 技術文件助手，回答必須基於官方文件並附上來源。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=600,
        )

        answer_text = completion.choices[0].message.content.strip()

        # Sonar 的回答通常會內嵌引用，我們不需要額外處理
        # 但可以從回答中解析出引用的 URL（如果有）
        sources = self._extract_sources(answer_text)

        return {
            "question": query,
            "version": version,
            "answer": answer_text,
            "sources": sources,
        }

    def _extract_sources(self, answer: str) -> list:
        """從回答中提取 URL（簡單版）"""
        import re
        urls = re.findall(r'https?://[^\s\]]+', answer)
        # 去重
        return list(set(urls))


if __name__ == "__main__":
    da = DocAnswerer()
    result = da.answer(
        "Docker BuildKit 在 v20.10 如何啟用？",
        version="v20.10"
    )

    print("Q:", result["question"])
    print("Version:", result["version"])
    print("\nAnswer:\n", result["answer"])
    print("\nSources:")
    for s in result["sources"]:
        print("-", s)

