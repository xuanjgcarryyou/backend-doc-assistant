from base_answerer import BaseDocAnswerer


class DockerAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return """你是專業的 Docker 技術文件助手。

回答規則：
1. 只根據 Docker 官方文件（docs.docker.com）回答
2. 在回答中必須列出相關的官方文件 URL
3. 如果涉及多個方面，列出多個 URL
4. 使用繁體中文回答，保持清楚的結構"""

    def get_versions(self) -> list:
        return ["latest", "v29.0", "v28.0", "v27.0", "v26.0", "v25.0", "v24.0", "v23.0", "v20.10", "v19.03"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 Docker 官方文件回答以下問題。

官方文件來源：https://docs.docker.com/

問題版本：Docker {version}

用戶問題：{query}

回答時請：
1. 列出相關的官方 docs.docker.com URL
2. 說明該功能在該版本的用法
3. 如有版本差異，請說明"""


class CAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return """你是 C 語言專家。

回答規則：
1. 只根據 C 官方文檔（cppreference.com）回答
2. 在回答中必須列出官方文件 URL
3. 說明該功能在各 C 版本（C89/C99/C11/C17/C23）中的差異
4. 使用繁體中文和程式碼範例"""

    def get_versions(self) -> list:
        return ["C23", "C17", "C11", "C99", "C89"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 C 官方文檔回答以下問題。

官方文件來源：https://en.cppreference.com/w/c/

問題版本：C {version}

用戶問題：{query}

回答時請：
1. 列出相關的官方 cppreference.com URL
2. 說明該功能首次出現的 C 版本
3. 如有已廢棄的標記，請說明"""


class CPPAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return """你是 C++ 語言專家。

回答規則：
1. 只根據 C++ 官方文檔（cppreference.com 與 isocpp.org）回答
2. 在回答中必須列出官方文件 URL
3. 說明該功能在各 C++ 標準中的差異
4. 提供程式碼範例"""

    def get_versions(self) -> list:
        return ["C++23", "C++20", "C++17", "C++14", "C++11", "C++03"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 C++ 官方文檔回答以下問題。

官方文件來源：
- https://en.cppreference.com/w/cpp/
- https://isocpp.org/

問題版本：C++ {version}

用戶問題：{query}

回答時請：
1. 列出相關的官方 URL（cppreference 或 isocpp.org）
2. 說明該功能首次引入的 C++ 標準版本
3. 提供具體的程式碼範例"""


class CSharpAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return """你是 C# 與 .NET 專家。

回答規則：
1. 只根據微軟官方文檔（learn.microsoft.com）回答
2. 在回答中必須列出官方文件 URL
3. 說明該功能在各 .NET 版本中的差異
4. 提供可運行的程式碼範例"""

    def get_versions(self) -> list:
        return [
            ("C# 14", ".NET 10"),
            ("C# 13", ".NET 9"),
            ("C# 12", ".NET 8"),
            ("C# 11", ".NET 7"),
            ("C# 10", ".NET 6"),
        ]

    def format_prompt(self, query: str, version: str) -> str:
        csharp_ver = version if isinstance(version, tuple) else version
        dotnet_ver = version if isinstance(version, tuple) else "latest"

        return f"""根據微軟官方文檔回答以下問題。

官方文件來源：https://learn.microsoft.com/

問題版本：C# {csharp_ver} (.NET {dotnet_ver})

用戶問題：{query}

回答時請：
1. 列出相關的官方 learn.microsoft.com URL
2. 說明該功能在各 .NET 版本的支援情況
3. 提供完整程式碼範例
4. 說明任何必要的套件或 using 引用"""


class GoAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return """你是 Go 語言專家。

回答規則：
1. 只根據 Go 官方文檔（golang.org、pkg.go.dev）回答
2. 在回答中必須列出官方文件 URL
3. 說明該功能在各 Go 版本中的差異
4. 提供完整可運行的程式碼範例"""

    def get_versions(self) -> list:
        return ["1.22", "1.21", "1.20", "1.19", "1.18", "1.17", "1.16"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 Go 官方文檔回答以下問題。

官方文件來源：
- https://golang.org/
- https://pkg.go.dev/

問題版本：Go {version}

用戶問題：{query}

回答時請：
1. 列出相關的官方 URL（golang.org 或 pkg.go.dev）
2. 說明該功能在該 Go 版本的用法
3. 提供可直接執行的完整程式碼範例
4. 說明常見的使用 pattern（如 goroutine、channel 等）"""


class KubernetesAnswerer(BaseDocAnswerer):
    def get_system_prompt(self) -> str:
        return """你是 Kubernetes 架構師。

回答規則：
1. 只根據 K8s 官方文檔（kubernetes.io）回答
2. 在回答中必須列出官方文件 URL
3. 說明該功能在各 K8s 版本中的差異
4. 提供完整的 YAML 配置範例"""

    def get_versions(self) -> list:
        return ["1.30", "1.29", "1.28", "1.27", "1.26", "1.25", "1.24"]

    def format_prompt(self, query: str, version: str) -> str:
        return f"""根據 K8s 官方文檔回答以下問題。

官方文件來源：https://kubernetes.io/

問題版本：Kubernetes {version}

用戶問題：{query}

回答時請：
1. 列出相關的官方 kubernetes.io URL
2. 說明該功能在該 K8s 版本的用法
3. 提供完整可用的 YAML 配置範例
4. 說明任何必要的先決條件（如 API 版本、namespace 等）
5. 如功能已廢棄，請明確說明"""

