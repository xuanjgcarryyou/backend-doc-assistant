from abc import ABC, abstractmethod
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()


class BaseDocAnswerer(ABC):
    """所有技術文檔助手的基類 - 改進版本"""

    def __init__(self):
        api_key = os.getenv("PPLX_API_KEY")
        if not api_key:
            raise RuntimeError("請在 .env 設定 PPLX_API_KEY")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai",
        )

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    @abstractmethod
    def get_versions(self) -> list:
        pass

    @abstractmethod
    def format_prompt(self, query: str, version: str) -> str:
        pass

    def answer(self, query: str, version: str = None) -> dict:
        """統一的回答方法 - 改進版本"""

        if version is None:
            version = self.get_versions()

        prompt = self.format_prompt(query, version)

        completion = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=800,
        )

        answer_text = completion.choices[0].message.content.strip()

        # 改進的來源提取（多重策略）
        sources = self._extract_sources_improved(answer_text)

        return {
            "technology": self.__class__.__name__,
            "question": query,
            "version": version,
            "answer": answer_text,
            "sources": sources,
            "raw_answer": answer_text,  # 保留原始答案便於除錯
        }

    def _extract_sources_improved(self, answer: str) -> list:
        """改進的 URL 提取 - 多重正則模式"""

        urls = []

        # 策略 1：標準 URL 模式
        pattern1 = r'https?://[^\s\)]+(?=[^\w\-]|$)'
        urls.extend(re.findall(pattern1, answer))

        # 策略 2：方括號內的 URL (markdown 格式)
        pattern2 = r'\[([https?://[^\]]+)\]'
        urls.extend(re.findall(pattern2, answer))

        # 策略 3：尖括號內的 URL
        pattern3 = r'<(https?://[^>]+)>'
        urls.extend(re.findall(pattern3, answer))

        # 策略 4：以 docs. 或 github. 等開頭（如果前面有 http://）
        pattern4 = r'(https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z0-9\-\.]+[/\w\-\.]*)'
        urls.extend(re.findall(pattern4, answer))

        # 去重並清理
        urls = list(set(urls))

        # 移除明顯的廢話
        urls = [
            url for url in urls
            if not url.endswith(('.', ',', ':', ';', '!', '?'))
               and len(url) > 10
               and 'example' not in url.lower()
        ]

        # 排序（優先顯示官方文件）
        priority_domains = [
            'docs.docker.com',
            'kubernetes.io',
            'golang.org',
            'learn.microsoft.com',
            'cppreference.com',
            'isocpp.org',
            'github.com',
        ]

        def get_priority(url):
            for i, domain in enumerate(priority_domains):
                if domain in url:
                    return i
            return len(priority_domains)

        urls.sort(key=get_priority)

        return urls

    def _extract_sources(self, answer: str) -> list:
        """舊版本 - 保留相容性"""
        return self._extract_sources_improved(answer)
