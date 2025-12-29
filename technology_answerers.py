from base_answerer import BaseDocAnswerer


class DockerAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return "你是專業的 Docker 技術文件助手，回答必須基於官方文件並附上來源。"

    def get_versions(self) -> list:
        return ["latest", "v29.0", "v28.0", "v27.0", "v26.0", "v25.0", "v24.0", "v23.0", "v20.10", "v19.03"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 Docker 官方文件（[https://docs.docker.com](https://docs.docker.com)）回答問題。
限制：只使用 docs.docker.com 的內容。
版本：Docker {version}
問題：{query}"""


class CAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return "你是 C 語言專家，回答必須基於 C 官方文檔（cppreference.com）並附上來源。"

    def get_versions(self) -> list:
        return ["C23", "C17", "C11", "C99", "C89"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 C 官方文檔（en.cppreference.com）回答問題。
限制：只使用官方文檔的內容。
版本：C {version}
問題：{query}"""


class CPPAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return "你是 C++ 語言專家，回答必須基於 C++ 官方文檔並附上來源。"

    def get_versions(self) -> list:
        return ["C++23", "C++20", "C++17", "C++14", "C++11", "C++03"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 C++ 官方文檔（en.cppreference.com、isocpp.org）回答問題。
限制：只使用官方文檔的內容。
版本：C++ {version}
問題：{query}"""


class CSharpAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return "你是 C# 與 .NET 專家，回答必須基於微軟官方文檔並附上來源。"

    def get_versions(self) -> list:
        return [
            ("C# 14", ".NET 10"),
            ("C# 13", ".NET 9"),
            ("C# 12", ".NET 8"),
            ("C# 11", ".NET 7"),
            ("C# 10", ".NET 6"),
        ]

    def format_prompt(self, query: str, version: str) -> str:
        csharp_ver = version[0] if isinstance(version, tuple) else version
        dotnet_ver = version[1] if isinstance(version, tuple) else "latest"
        return f"""根據微軟官方文檔（learn.microsoft.com）回答問題。
限制：只使用微軟官方文檔的內容。
版本：C# {csharp_ver} (.NET {dotnet_ver})
問題：{query}"""


class GoAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return "你是 Go 語言專家，回答必須基於 Go 官方文檔並附上來源。"

    def get_versions(self) -> list:
        return ["1.22", "1.21", "1.20", "1.19", "1.18", "1.17", "1.16"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 Go 官方文檔（golang.org、pkg.go.dev）回答問題。
限制：只使用官方文檔的內容。
版本：Go {version}
問題：{query}
請提供可運行的代碼示例。"""


class KubernetesAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return "你是 Kubernetes 架構師，回答必須基於 K8s 官方文檔並附上來源。"

    def get_versions(self) -> list:
        return ["1.30", "1.29", "1.28", "1.27", "1.26", "1.25", "1.24"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 K8s 官方文檔（kubernetes.io）回答問題。
限制：只使用 kubernetes.io 的內容。
版本：K8s {version}
問題：{query}
請提供 YAML 配置示例。"""
