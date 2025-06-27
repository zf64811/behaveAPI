# BehaveAPI - API 自动化测试框架

[![Test and Deploy](https://github.com/USERNAME/REPO_NAME/actions/workflows/test-and-deploy.yml/badge.svg)](https://github.com/USERNAME/REPO_NAME/actions/workflows/test-and-deploy.yml)
[![GitHub Pages](https://img.shields.io/badge/Test%20Reports-GitHub%20Pages-blue)](https://USERNAME.github.io/REPO_NAME/)

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

### 生成测试报告

```bash
# 生成 JSON 格式报告
behave -f json -o reports/report.json

# 生成 JUnit 格式报告
behave --junit --junit-directory reports/
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

## CI/CD Integration

This project includes GitHub Actions workflow for continuous integration and deployment of test reports to GitHub Pages.

### Features

- **Automated Test Execution**: Tests run automatically on push to main branch and pull requests
- **HTML Test Reports**: Beautiful HTML reports generated for each test run
- **GitHub Pages Deployment**: Test reports are automatically deployed and accessible online
- **Test Artifacts**: Test reports are saved as artifacts for each workflow run

### Setup

1. **Enable GitHub Pages** in your repository:

   - Go to Settings → Pages
   - Set Source to "GitHub Actions"

2. **Configure Secrets** (if needed):

   - Add any API keys or sensitive data as repository secrets
   - Reference them in the workflow file

3. **Push to Main Branch**:
   - The workflow will automatically trigger
   - Tests will run and reports will be generated
   - Reports will be deployed to GitHub Pages

### Accessing Test Reports

After the workflow completes successfully:

1. **GitHub Pages URL**:

   - `https://<username>.github.io/<repository-name>/`
   - You'll find links to all available reports

2. **Workflow Artifacts**:

   - Go to Actions tab → Select a workflow run
   - Download test-reports artifact

3. **Report Types**:
   - **Enhanced Report**: Custom HTML report with statistics and visualizations
   - **Behave HTML Report**: Standard behave HTML report
   - **Behave JSON Report**: Raw JSON data for further processing

### Workflow Triggers

The CI/CD pipeline triggers on:

- Push to `main` or `master` branch
- Pull requests to `main` or `master` branch
- Manual trigger via GitHub Actions UI

### Local Report Generation

To generate reports locally:

```bash
# Run tests with JSON output
python -m behave -f json -o reports/behave-report.json

# Generate enhanced HTML report
python generate_report.py

# Open report
start reports/enhanced-report.html  # Windows
open reports/enhanced-report.html   # macOS
xdg-open reports/enhanced-report.html  # Linux
```

### Customization

You can customize the workflow by editing `.github/workflows/test-and-deploy.yml`:

- Add more Python versions for matrix testing
- Include additional test frameworks
- Add notification steps (Slack, email, etc.)
- Customize report generation

## Professional Test Reports

本项目集成了多种专业的测试报告框架，提供丰富的测试结果展示和分析功能。

### 集成的报告类型

#### 1. Allure Report

最专业的测试报告框架，提供：

- 📊 **测试趋势分析** - 历史数据和趋势图表
- 🏷️ **测试分类** - 按功能、严重程度等分类
- 📸 **附件支持** - 截图、日志、请求响应等
- 🔍 **失败分析** - 详细的失败原因和堆栈跟踪
- 📈 **统计图表** - 饼图、柱状图等可视化
- 🕐 **执行时间线** - 测试执行的时间分布

#### 2. Enhanced HTML Report

自定义增强报告，特点：

- ✅ 清晰的测试统计概览
- 📱 响应式设计，支持移动设备
- 🎨 美观的 UI 设计
- ⚡ 快速加载，无需外部依赖

#### 3. Behave HTML Report

标准的 Behave HTML 报告：

- 📝 详细的步骤执行信息
- 🔗 场景和特性的层级展示
- 💡 简洁明了的测试结果

### 本地使用 Allure 报告

#### 安装 Allure 命令行工具

**Windows 用户：**

```bash
# 使用Scoop（推荐）
scoop install allure

# 使用Chocolatey
choco install allure

# 使用npm
npm install -g allure-commandline
```

**macOS 用户：**

```bash
# 使用Homebrew
brew install allure

# 使用npm
npm install -g allure-commandline
```

**Linux 用户：**

```bash
# 下载并解压
wget https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz
tar -zxvf allure-2.24.1.tgz
export PATH=$PATH:/path/to/allure-2.24.1/bin

# 或使用npm
npm install -g allure-commandline
```

#### 运行测试并生成 Allure 报告

使用提供的脚本：

```bash
# 运行所有测试
python run_tests_with_allure.py

# 运行特定标签的测试
python run_tests_with_allure.py --tags=@smoke

# 运行特定feature
python run_tests_with_allure.py features/websocket/sample_ws.feature
```

或手动运行：

```bash
# 1. 运行测试并生成Allure结果
python -m behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# 2. 生成Allure报告
allure generate reports/allure-results -o reports/allure-report --clean

# 3. 查看报告
allure open reports/allure-report
```

### 在测试中添加 Allure 特性

#### 1. 添加测试描述和链接

```python
from allure_behave import fixture
import allure

@allure.feature('WebSocket Testing')
@allure.story('Order Book Subscription')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://jira.example.com/TASK-123', name='JIRA Ticket')
def step_impl(context):
    """Test implementation"""
    pass
```

#### 2. 添加附件

```python
@when('I send the API request')
def step_send_request(context):
    response = requests.post(url, json=payload)

    # 附加请求信息
    allure.attach(
        json.dumps(payload, indent=2),
        name="Request Payload",
        attachment_type=allure.attachment_type.JSON
    )

    # 附加响应信息
    allure.attach(
        json.dumps(response.json(), indent=2),
        name="Response Body",
        attachment_type=allure.attachment_type.JSON
    )
```

#### 3. 添加测试步骤

```python
@then('the response should be valid')
def step_validate_response(context):
    with allure.step("Check response status code"):
        assert context.response.status_code == 200

    with allure.step("Validate response schema"):
        validate_schema(context.response.json())

    with allure.step("Check business logic"):
        assert context.response.json()['status'] == 'success'
```

### 其他可集成的测试报告

1. **ReportPortal** - 企业级测试管理平台

   - 实时测试结果
   - AI 驱动的失败分析
   - 团队协作功能

2. **ExtentReports** - 美观的测试报告

   - 丰富的图表和统计
   - 支持多种测试框架

3. **Cucumber Reports** - Cucumber 风格报告
   - 与 Jenkins 完美集成
   - 支持并行执行报告

### CI/CD 中的报告访问

GitHub Actions 工作流会自动生成所有类型的报告，并部署到 GitHub Pages：

1. **在线查看**: `https://<username>.github.io/<repository>/`
2. **Allure 历史**: 保留最近 20 次构建的历史记录
3. **下载离线查看**: 从 Actions 工作流的 Artifacts 下载

## Test Reports
