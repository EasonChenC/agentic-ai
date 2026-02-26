# 反思模式智能体工作流 - 图表生成

基于反思设计模式的自我改进数据可视化生成系统。

## 📁 项目结构

```
.
├── main.py                 # 主程序入口
├── chart_workflow.py       # 核心工作流实现
├── utils.py               # 辅助工具模块
├── requirements.txt       # 依赖包列表
├── .env.example          # 环境变量模板
└── coffee_sales.csv      # 示例数据集
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # 可选
GOOGLE_API_KEY=your_google_api_key_here        # 可选，用于Gemini
```

### 3. 运行工作流

```bash
python main.py
```

## 🔄 工作流程

1. **生成V1代码** - LLM生成初始版本的matplotlib代码
2. **执行V1** - 运行代码生成第一版图表
3. **反思评审** - 多模态LLM分析图表并提出改进建议
4. **生成V2代码** - 根据反馈生成改进版代码
5. **执行V2** - 生成优化后的图表

## ⚙️ 自定义配置

编辑 `main.py` 中的参数：

```python
# 修改用户需求
user_instructions = "你的图表需求描述"

# 选择模型
generation_model = "gemini-1.5-flash"  # 快速生成
reflection_model = "gemini-1.5-pro"    # 深度反思

# 自定义输出文件名
image_basename = "my_chart"
```

## 📊 支持的模型

- **OpenAI**: gpt-4o, gpt-4o-mini, gpt-3.5-turbo
- **Anthropic**: claude-3-opus, claude-3-sonnet
- **Google Gemini**: gemini-1.5-pro, gemini-1.5-flash, gemini-pro-vision

## 📝 输出文件

- `{basename}_v1.png` - 初始版本图表
- `{basename}_v2.png` - 改进版本图表

## 💡 使用提示

1. **生成阶段使用快速模型节省成本**
   - OpenAI: gpt-4o-mini
   - Google: gemini-1.5-flash
   - Anthropic: claude-3-haiku

2. **反思阶段使用强推理模型提升质量**
   - OpenAI: gpt-4o
   - Google: gemini-1.5-pro
   - Anthropic: claude-3-opus

3. **混合使用不同供应商**
   - 例如：生成用Gemini Flash，反思用GPT-4o
   - 充分利用各家模型的优势

4. 查看两个版本的图表对比改进效果
