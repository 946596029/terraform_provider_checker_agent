# Prompt Module - Structured Prompt Template System

A structured prompt template system that uses JSON format to define prompts and converts them to Markdown format for LLM interaction.

## Features

- **JSON-based Templates**: Define prompts in structured JSON format
- **Markdown Conversion**: Automatically convert JSON templates to Markdown format
- **Template Management**: Load, save, and update templates easily
- **Auto-wrapping**: Text automatically wraps at 120 characters per line

## Structure

```
prompt_module/
├── __init__.py              # Module exports
├── core/
│   ├── __init__.py
│   ├── prompt_template.py   # PromptTemplate class
│   └── prompt_converter.py  # PromptConverter class
└── templates/               # JSON template files
    ├── fibonacci_example.json
    └── terraform_provider_checker.json
```

## Usage

### Basic Usage

```python
from prompt_module import PromptTemplate, PromptConverter

# Load template from JSON file
template = PromptTemplate.from_json_file("prompt_module/templates/fibonacci_example.json")

# Convert to Markdown
converter = PromptConverter()
markdown = converter.to_markdown(template)

print(markdown)
```

### Create Template from Dictionary

```python
template_data = {
    "role": "你是一位专业的编程专家",
    "task": "编写一个程序",
    "context": ["使用 Python 语言"],
    "input": ["用户输入"],
    "output_requirements": {
        "format": "代码",
        "language": "Python",
        "length": "50 行以内"
    },
    "examples": {
        "input": "示例输入",
        "output": "示例输出"
    },
    "additional_instructions": "额外说明"
}

template = PromptTemplate(template_data=template_data)
converter = PromptConverter()
markdown = converter.to_markdown(template)
```

### Update Template Dynamically

```python
template = PromptTemplate()
template.update(
    role="你是一位数据分析专家",
    task="分析数据",
    context=["数据集包含销售数据"]
)
```

### Save Template to File

```python
template = PromptTemplate()
template.update(role="角色", task="任务")
template.save_to_file("my_template.json")
```

## JSON Template Structure

```json
{
  "role": "角色描述",
  "task": "任务描述",
  "context": [
    "上下文信息1",
    "上下文信息2"
  ],
  "input": [
    "输入要求1",
    "输入要求2"
  ],
  "output_requirements": {
    "format": "输出格式",
    "language": "输出语言",
    "length": "输出长度限制"
  },
  "examples": {
    "input": "输入示例",
    "output": "输出示例（支持代码块）"
  },
  "additional_instructions": "额外说明"
}
```

## Integration with LLM

```python
from prompt_module import PromptTemplate, PromptConverter
from llm_module.core.llm_client import LLMClient

# Load and convert template
template = PromptTemplate.from_json_file("prompt_module/templates/fibonacci_example.json")
converter = PromptConverter()
markdown_prompt = converter.to_markdown(template)

# Use with LLM
client = LLMClient(platform="alibaba")
messages = [{"role": "user", "content": markdown_prompt}]
response = client.chat(messages=messages, model="qwen-turbo", max_tokens=1000)
```

## API Reference

### PromptTemplate

- `PromptTemplate(template_data=None)` - Create template from dictionary
- `from_json_file(file_path)` - Load template from JSON file
- `from_json_string(json_string)` - Load template from JSON string
- `to_dict()` - Convert to dictionary
- `to_json_string(indent=2)` - Convert to JSON string
- `save_to_file(file_path, indent=2)` - Save to JSON file
- `update(**kwargs)` - Update template fields
- `get(key, default=None)` - Get field value

### PromptConverter

- `to_markdown(template, wrap_width=120)` - Convert template to Markdown format

