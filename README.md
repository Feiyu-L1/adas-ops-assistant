# ADAS 智能运维助手

基于多 Agent 架构的 ADAS（高级驾驶辅助系统）智能运维问答助手。用户输入运维问题后，系统自动判断问题类型，调用对应 Agent 进行分析，给出分析结果或文档回答，并标注参考来源。

## 系统架构

```
用户输入
   ↓
TriageAgent（意图分类）
   ├── 日志异常 / 性能问题 → LogAgent → ResponseAgent → EscalationAgent
   └── 配置问题 / 常规问题 → DocAgent
```

整个流程由 LangGraph StateGraph 驱动，知识库由 Dify 提供。

## 环境要求

- Python 3.11+
- Mimo API Key（用于调用 LLM）
- Dify API Key + Dataset ID（用于知识库检索）

## 安装步骤

**1. 克隆项目**

```bash
git clone <your-repo-url>
cd adas-ops-assistant
```

**2. 安装依赖**

```bash
pip install -r requirements.txt
```

**3. 配置环境变量**

复制示例文件并填入你自己的 API Key：

```bash
cp .env.example .env
```

编辑 `.env`：

```
MIMO_API_KEY=你的 Mimo API Key
DIFY_API_KEY=你的 Dify API Key
DIFY_DATASET_ID=你的 Dify 知识库 ID
USE_DIFY_STORE=true
DIFY_SEARCH_METHOD=keyword_search
```

`DIFY_SEARCH_METHOD` 支持三种值：
- `keyword_search`：关键词匹配，无需额外配置（默认）
- `full_text_search`：全文检索，中文效果更好
- `semantic_search`：语义检索，效果最好，需在 Dify 中配置 Embedding 模型

**4. 配置 Dify 知识库**

在 Dify 平台创建一个知识库，上传 ADAS 相关文档（如传感器手册、故障处理规范等），将知识库 ID 填入 `.env` 的 `DIFY_DATASET_ID`。

**5. 启动**

```bash
streamlit run app.py
```

浏览器访问 http://localhost:8501

## 项目结构

```
adas-ops-assistant/
├── app.py                 # Streamlit 前端
├── config.py              # 模型与知识库配置
├── agents/
│   ├── base.py            # Agent 抽象基类
│   ├── triage.py          # 意图分类
│   ├── log.py             # 日志分析
│   ├── doc.py             # 文档问答
│   ├── response.py        # 故障报告生成
│   └── escalation.py      # 升级判断
├── core/
│   ├── graph.py           # LangGraph 状态机
│   ├── model_adapter.py   # 模型接口封装
│   ├── knowledge_store.py # 知识库（Mock / Dify）
│   └── message.py         # 消息数据结构
└── tests/                 # 单元测试
```

## 不使用 Dify 的情况

将 `.env` 中 `USE_DIFY_STORE` 设为 `false`，系统会使用本地 MockStore（内存存储，简单关键词匹配）。适合本地开发调试，知识库为空时模型会告知用户无相关信息。
