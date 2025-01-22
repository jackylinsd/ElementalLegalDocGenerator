from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class AIServer:
    def __init__(
        self,
        model: str = os.getenv("MODEL",""),
        api_key: str = os.getenv("API_KEY",""),
        base_url: str = os.getenv("URL_BASE","")
    ):
        if not api_key or not base_url or not model:
            pass

        self.model = model

        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        except Exception as e:
            raise ValueError("请检查你的API_KEY URL_BASE MODEL是否正确")
        self.messages = []
        self.messages.append({
            "role": "system",
            "content": "你是一个专业律师，擅长提供专业的法律指导。"
        })

    def optimize_text(self, text: str,case_type='普通民事案件') -> str:
        prompt = f"这是一个{case_type}。请优化以下文字，使其更加专业，符合法律文本的需求，符合案件所需要的准确表述。只需要返回优化后的文本:\n\n{text}"
        
        current_messages = self.messages.copy()
        current_messages.append({"role": "user", "content": prompt})
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=current_messages,
                temperature=0.1,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return "出现错误，请检查你的API_KEY URL_BASE MODEL是否正确配置。错误原因：{}".format(e)

    
    async def optimize_text_async(self, text: str) -> str:
        prompt = f"请优化以下文字，使其更加专业，符合法律文本的需求，只需要返回优化后的文本:\n\n{text}"
        
        current_messages = self.messages.copy()
        current_messages.append({"role": "user", "content": prompt})
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=current_messages,
                temperature=0.1,
                max_tokens=1024
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return "出现错误，请检查你的API_KEY URL_BASE MODEL是否正确配置。错误原因：{}".format(e)