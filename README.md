# terraform_provider_checker_agent

## 虚拟环境
### Windows
 * `激活`: .\terraform_provider_checker_agent\Scripts\activate.bat
 * `关闭`：.\terraform_provider_checker_agent\Scripts\deactivate.bat
### Linux
 * `激活`: source .\bin\activate
 * `关闭`：source .\bin\deactivate

## PowerShell 执行策略
 * `开启`: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
 * `关闭`: Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser

## 安装所有依赖
    pip install -r requirements.txt