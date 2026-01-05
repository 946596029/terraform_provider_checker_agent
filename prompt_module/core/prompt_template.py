"""
Prompt Template - Manages structured prompt templates
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path


class PromptTemplate:
    """Manages structured prompt templates in JSON format"""

    def __init__(self, template_data: Optional[Dict[str, Any]] = None):
        """
        Initialize prompt template
        
        Args:
            template_data: Dictionary containing prompt template structure
        """
        self.template_data = template_data or self._default_template()
        self._validate_template()

    def _default_template(self) -> Dict[str, Any]:
        """Returns default template structure"""
        return {
            "role": "",
            "task": "",
            "context": [],
            "input": [],
            "output_requirements": {
                "format": "",
                "language": "",
                "length": ""
            },
            "examples": {
                "input": "",
                "output": ""
            },
            "additional_instructions": ""
        }

    def _validate_template(self):
        """Validate template structure"""
        required_keys = ["role", "task"]
        for key in required_keys:
            if key not in self.template_data:
                raise ValueError(f"Missing required key: {key}")

    @classmethod
    def from_json_file(cls, file_path: str) -> "PromptTemplate":
        """
        Load template from JSON file
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            PromptTemplate instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Template file not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        return cls(template_data=template_data)

    @classmethod
    def from_json_string(cls, json_string: str) -> "PromptTemplate":
        """
        Load template from JSON string
        
        Args:
            json_string: JSON string containing template data
            
        Returns:
            PromptTemplate instance
        """
        template_data = json.loads(json_string)
        return cls(template_data=template_data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary"""
        return self.template_data.copy()

    def to_json_string(self, indent: int = 2) -> str:
        """
        Convert template to JSON string
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON string
        """
        return json.dumps(self.template_data, indent=indent, ensure_ascii=False)

    def save_to_file(self, file_path: str, indent: int = 2):
        """
        Save template to JSON file
        
        Args:
            file_path: Path to save JSON file
            indent: JSON indentation level
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.template_data, f, indent=indent, ensure_ascii=False)

    def update(self, **kwargs):
        """
        Update template fields
        
        Args:
            **kwargs: Key-value pairs to update
        """
        for key, value in kwargs.items():
            if key in self.template_data:
                if isinstance(self.template_data[key], dict) and isinstance(value, dict):
                    self.template_data[key].update(value)
                else:
                    self.template_data[key] = value
            else:
                self.template_data[key] = value
        self._validate_template()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get template field value
        
        Args:
            key: Field key
            default: Default value if key not found
            
        Returns:
            Field value
        """
        return self.template_data.get(key, default)

