from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_version="2024-12-01-preview",  # 根据你的 Azure OpenAI 版本调整
)