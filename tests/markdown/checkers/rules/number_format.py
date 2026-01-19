"""
Number format checking rule.
"""

from ..line_checker import LineBasedChecker
from ..base import CheckResult, CheckSeverity
from typing import Optional
from code_checker.prompt_template import build_chat_prompt
from code_checker.chains.models import build_chat_model
from code_checker.chains.parsers import default_parser
from code_checker.config import ensure_api_key
import re

def create_number_format_checker() -> LineBasedChecker:
    """
    Create a checker for number format validation.
    
    Checks that numbers in markdown follow the format: 1,234 (with commas for thousands).
    """
    def check_number_format(line: str, line_num: int) -> Optional[CheckResult]:
        """
        Check if numbers in the line follow the correct format.
        
        This is a simple example - you can customize the pattern as needed.
        """
        
        # 搜索特征，当前行含有数字
        pattern = r'\b([1-9]+)\b'
        re.compile(pattern)
        
        # 如果当前行不含有数字，则跳过
        if not re.search(pattern, line):
            return None
         
        # 如果含有数字，则检查数字是否符合格式
        role = "code checker"
        task = "检查Markdown文本是否符合要求"
        context = """
        数字格式化要求：
          1. 该目标只针对 `数字内容` 进行约束，请结合上下文判断是否需要格式化
            例如时间戳，版本号，网址IP等不需要格式化
          2. `数字内容` 需要每3位使用逗号分隔，例如 1234567 应该格式化为 1,234,567
          3. `数字内容` 需要使用 ` 或 ** 包裹，例如 `123,456` 或 **123,456**
        """
        instructions = []
        limitations = [
            "仅遵从传入的规范"
        ]
        input = [line]
        output_requirements = {
            "format": "json",
        }

        examples = {}

        prompt = build_chat_prompt(role, task, context, instructions, limitations, input, output_requirements, examples)
        chain = prompt | build_chat_model() | default_parser

        ensure_api_key()
        # 打印检查结果
        response = chain.invoke({})
        print("--------------------------------")
        print(line)
        print(response)
        print("--------------------------------")
        return None

        # matches = re.finditer(pattern, line)
        # for match in matches:
        #     number = match.group(1)
        #     # Skip if it's part of a URL, code block, or other special context
        #     start_pos = match.start()
        #     end_pos = match.end()
            
        #     # Check if it's in a code span or code block
        #     before = line[:start_pos]
        #     after = line[end_pos:]
            
        #     # Skip if surrounded by backticks (code)
        #     if '`' in before[-10:] or '`' in after[:10]:
        #         continue
            
        #     # Skip if it's part of a URL
        #     if 'http://' in before[-20:] or 'https://' in before[-20:]:
        #         continue
            
        #     # Format the number with commas
        #     formatted = format(int(number), ',')
            
        #     return CheckResult(
        #         rule_name="Number Format",
        #         severity=CheckSeverity.WARNING,
        #         message=f"Number '{number}' should be formatted with commas: '{formatted}'",
        #         line_number=line_num,
        #         column_number=start_pos + 1,
        #         context=line.strip(),
        #         suggestion=f"Replace '{number}' with '{formatted}'"
        #     )
        
        return None
    
    return LineBasedChecker(
        name="Number Format Checker",
        description="Checks that large numbers are formatted with comma separators",
        check_function=check_number_format
    )

