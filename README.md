# BehaveAPI - API 自动化测试框架

基于 Python Behave 的 API 自动化测试框架，支持 REST API 和 WebSocket 接口测试。

## 项目概述

BehaveAPI 是一个基于 Python 和 Behave 的 BDD（行为驱动开发）测试框架，支持 REST API 和 WebSocket 的自动化测试。

## 项目结构

```
behaveAPI/
├── features/                    # Feature 文件目录
│   ├── rest/                   # REST API 测试用例
│   │   └── candlestick.feature # K线数据接口测试
│   └── websocket/              # WebSocket 测试用例
├── features/steps/             # Step 定义目录
│   ├── rest_steps.py          # REST API 步骤定义
│   ├── ws_steps.py            # WebSocket 步骤定义
│   └── common_steps.py        # 通用步骤定义
├── features/environment.py     # Behave 环境配置
├── config/                     # 配置文件目录
│   ├── config.yml             # 主配置文件
│   └── .env.example           # 环境变量示例
├── test_data/                  # 测试数据目录
│   └── test_data.json         # 测试数据文件
├── utils/                      # 工具模块
│   ├── __init__.py
│   ├── assertions.py          # 断言工具
│   ├── logger.py              # 日志工具
│   └── config_manager.py      # 配置管理
├── reports/                    # 测试报告目录
├── requirements.txt            # 依赖包列表
├── .env                        # 环境变量文件（需自行创建）
├── .gitignore                 # Git 忽略文件
└── README.md                   # 项目说明文档
```

## 技术栈

- **Python 3.8+**
- **Behave**: BDD 测试框架
- **Requests**: REST API 请求库
- **websocket-client**: WebSocket 客户端库
- **PyYAML**: YAML 配置文件解析
- **python-dotenv**: 环境变量管理
- **jsonschema**: JSON Schema 验证

## 安装说明

1. 克隆项目

```bash
git clone <repository_url>
cd behaveAPI
```

2. 创建虚拟环境（推荐）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置环境变量

```bash
cp config/.env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

## 配置说明

### 环境变量 (.env)

```
BASE_URL=https://uat-api.3ona.co
TIMEOUT=30
LOG_LEVEL=INFO
```

### 配置文件 (config/config.yml)

```yaml
api:
  base_url: ${BASE_URL}
  timeout: ${TIMEOUT}
  headers:
    Content-Type: application/json

logging:
  level: ${LOG_LEVEL}
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## 测试用例设计

### REST API 测试

#### 场景一：正确参数请求

- 发送包含所有必需参数的 GET 请求
- 验证响应状态码为 200
- 验证响应体包含 result.data
- 验证数据包含 o, h, l, c 等字段

#### 场景二：错误参数请求

- 发送缺少必需参数的请求
- 验证返回错误状态码
- 验证错误响应结构

## 执行方式

### 运行所有测试

```bash
behave
```

### 运行特定功能测试

```bash
# 只运行 REST API 测试
behave features/rest/

# 只运行 WebSocket 测试
behave features/websocket/
```

### 运行特定标签的测试

```bash
# 运行标记为 @smoke 的测试
behave --tags=@smoke

# 运行标记为 @rest 的测试
behave --tags=@rest
```

## 日志说明

日志文件将保存在 `reports/` 目录下，包含：

- 请求详情（URL、Headers、Body）
- 响应详情（状态码、Headers、Body）
- 断言结果
- 错误信息

## 扩展说明

### 添加新的测试用例

1. 在 `features/` 对应目录下创建 `.feature` 文件
2. 在 `features/steps/` 中实现对应的步骤定义
3. 如需新的测试数据，在 `test_data/` 中添加

### 添加新的断言方法

在 `utils/assertions.py` 中添加自定义断言方法

### 添加新的配置项

1. 在 `.env` 中添加环境变量
2. 在 `config/config.yml` 中引用环境变量
3. 在代码中通过 `config_manager` 获取配置

## 常见问题

### Q: 如何切换测试环境？

A: 修改 `.env` 文件中的 `BASE_URL` 变量

### Q: 如何调试失败的测试？

A:

1. 查看 `reports/` 目录下的日志文件
2. 使用 `behave --no-capture` 查看实时输出
3. 在步骤定义中添加断点调试

### Q: 如何添加新的请求头？

A: 在 `config/config.yml` 的 `headers` 部分添加，或在步骤定义中动态设置

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
