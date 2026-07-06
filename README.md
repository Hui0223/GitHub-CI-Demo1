# CI/CD 学习项目

## 📁 项目结构

```
cicd-demo/
├── app/
│   ├── __init__.py
│   └── main.py              ← FastAPI 应用
├── tests/
│   ├── __init__.py
│   └── test_main.py         ← 单元测试
├── .github/workflows/
│   ├── ci.yml               ← CI 流水线 (lint → test → build)
│   └── cd.yml               ← CD 流水线 (push → staging → production)
├── Dockerfile               ← 容器化构建 (多阶段)
├── requirements.txt         ← 生产依赖
├── requirements-dev.txt     ← 开发/测试依赖
├── pyproject.toml           ← 项目配置
├── .gitignore
└── .dockerignore
```

---

## 🚀 快速开始

### 本地运行

```bash
# 1. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # Linux/Mac

# 2. 安装依赖
pip install -r requirements-dev.txt

# 3. 运行应用
uvicorn app.main:app --reload

# 4. 访问
# http://127.0.0.1:8000
# http://127.0.0.1:8000/docs  (Swagger UI)
```

### 运行测试

```bash
pytest -v
```

### Docker 构建

```bash
docker build -t cicd-demo .
docker run -p 8000:8000 cicd-demo
```

---

## 📚 学习路线 (按步骤完成)

### Step 1: 理解 CI Pipeline (`.github/workflows/ci.yml`)

打开 `ci.yml`，它包含3个 Job:

```
lint (代码检查) → test (运行测试) → build (Docker构建)
```

**核心概念:**
- `on`: 什么事件触发 Pipeline
- `jobs`: Pipeline 中的阶段
- `needs`: Job 之间的依赖关系
- `steps`: 每个 Job 中的具体步骤
- `uses`: 引用社区 Action (可复用的构建块)
- `run`: 执行 shell 命令

**练习:**
1. ✏️ 故意让一个测试失败，观察 CI 报错
2. ✏️ 给 `app/main.py` 添加新接口，补充对应测试
3. ✏️ 添加测试覆盖率报告 (提示: `pytest-cov`)

---

### Step 2: 理解 CD Pipeline (`.github/workflows/cd.yml`)

```
CI通过 → 推送Docker镜像 → 部署Staging → (审批) → 部署Production
```

**核心概念:**
- `workflow_run`: 一个 workflow 完成后触发另一个
- `environment`: GitHub 环境，可配置保护规则和审批
- `secrets`: 敏感信息 (密码、Token) 安全存储

**练习:**
1. ✏️ 在 GitHub 仓库 Settings → Environments 创建 `staging` 和 `production`
2. ✏️ 给 `production` 环境添加 Required Reviewers (审批人)

---

### Step 3: Docker 容器化 (`Dockerfile`)

**核心概念:**
- 多阶段构建 (Multi-stage): 减小最终镜像体积
- 非 root 用户: 安全最佳实践
- `.dockerignore`: 排除不必要文件

**练习:**
1. ✏️ 用 `docker images` 查看镜像大小
2. ✏️ 试试去掉多阶段构建，对比镜像大小差异

---

### Step 4: 进阶练习

| 练习 | 难度 | 学到什么 |
|------|------|----------|
| 添加 `ruff format --check` | ⭐ | 代码格式化检查 |
| 添加 `pytest-cov` 覆盖率 | ⭐ | 测试覆盖率门槛 |
| 矩阵测试多Python版本 | ⭐⭐ | `strategy.matrix` |
| 添加 `docker-compose.yml` | ⭐⭐ | 多容器编排 |
| 添加数据库 + 集成测试 | ⭐⭐⭐ | Service Container |
| 部署到真实服务器 | ⭐⭐⭐ | SSH deploy / K8s |
| 添加 Slack/钉钉通知 | ⭐⭐ | Webhook 通知 |
| 实现蓝绿部署 | ⭐⭐⭐⭐ | 零停机部署 |

---

## 🔑 关键概念速查

| 概念 | 说明 |
|------|------|
| **Pipeline** | 从代码到部署的完整自动化流程 |
| **Job** | Pipeline 中的一个阶段 (如 test, build) |
| **Step** | Job 中的一个步骤 |
| **Artifact** | 构建产物 (Docker image, binary) |
| **Cache** | 缓存依赖，加速后续构建 |
| **Secret** | 加密的敏感变量 (token, password) |
| **Environment** | 部署目标 (staging, production) |
| **Branch Protection** | 主分支保护，强制通过CI才能合并 |

---

## 🏁 上手步骤

```bash
# 1. 初始化 Git
cd "C:\Users\hujiang\AI Work\cicd-demo"
git init
git add .
git commit -m "feat: initial CI/CD demo project"

# 2. 创建 GitHub 仓库并推送
# 去 https://github.com/new 创建仓库 cicd-demo
git remote add origin https://github.com/YOUR_USERNAME/cicd-demo.git
git branch -M main
git push -u origin main

# 3. 查看 GitHub → Actions 页面，观察 CI 自动运行！
```

---

## GitLab CI 对照学习 (`.gitlab-ci.yml`)

同一套项目也提供了 **GitLab CI** 配置，结构与 GitHub Actions 的 `ci.yml` 一致:

```
lint → test → build
```

### GitHub vs GitLab 概念对照

| GitHub Actions | GitLab CI | 本项目中对应位置 |
|----------------|-----------|------------------|
| `on: push` | `rules` / `only` | 两个文件顶部 |
| `jobs.lint` | `lint:` job | 第一阶段 |
| `needs: lint` | `needs: [lint]` | test 依赖 lint |
| `runs-on: ubuntu-latest` | `image: python:3.12-slim` | 运行环境 |
| `uses: actions/checkout` | 默认自动 checkout | GitLab Runner 内置 |
| `uses: actions/cache` | `cache: paths` | pip 缓存 |
| `run: pytest` | `script: pytest` | test 阶段 |
| `workflow` (CD) | multi-stage pipeline | `cd.yml` vs deploy stage |

### GitLab 上手步骤

```bash
cd "C:\Users\hujiang\AI Work\cicd-demo"
git remote add gitlab https://gitlab.com/YOUR_USERNAME/cicd-demo.git
git push -u gitlab main
# GitLab → Build → Pipelines
```

### 求职向：测试项目接入 CI 最小模板

**pytest（GitHub）:** `pytest -v --junitxml=junit.xml`

**pytest（GitLab）:** 同上，写在 `script:` 下

**Robot Framework 追加:** `robot --outputdir results path/to/tests`
###