from abc import ABC, abstractmethod
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()


class BaseDocAnswerer(ABC):
    """所有技術文檔助手的基類"""

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
        """統一的回答方法"""

        if version is None:
            version = self.get_versions()[0]

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
        sources = self._extract_sources(answer_text)

        return {
            "technology": self.__class__.__name__,
            "question": query,
            "version": version,
            "answer": answer_text,
            "sources": sources,
        }

    def _extract_sources(self, answer: str) -> list:
        """從回答中提取 URL"""
        urls = re.findall(r'https?://[^\s\]]+', answer)
        return list(set(urls))
