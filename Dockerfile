# 使用輕量級的 Python 3.12 基礎映像檔
FROM python:3.12-slim

# 複製 uv 執行檔 (由官方映像檔提供)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 設定工作目錄
WORKDIR /app

# 先複製套件管理設定以利用 Docker 緩存
COPY pyproject.toml uv.lock ./

# 使用 uv 同步套件依賴 (會建立在 /.venv 中)
RUN uv sync --frozen --no-dev

# 複製專案所有程式碼 (會根據 .dockerignore 排除特定檔案)
COPY . .

# 透過 uv 執行 Python 主程式
CMD ["uv", "run", "python", "src/main.py"]
