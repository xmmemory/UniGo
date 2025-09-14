import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取SECRET_KEY
secret_key = os.getenv("SECRET_KEY", "default-secret-key")
print(f"Loaded SECRET_KEY: {secret_key}")

# 检查.env文件是否存在
if os.path.exists(".env"):
    print(".env file exists")
    # 读取.env文件内容
    with open(".env", "r") as f:
        content = f.read()
        print(".env file content:")
        print(content)
else:
    print(".env file does not exist")