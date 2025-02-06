from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class AIServer:
    def __init__(
        self,
        model: str = os.getenv("MODEL", ""),
        api_key: str = os.getenv("API_KEY", ""),
        base_url: str = os.getenv("URL_BASE", "")
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

    def optimize_text(self, text: str, case_type='普通民事案件') -> str:
        # 非流式输出，暂留
        prompt = f"这是一个{
            case_type}。请优化以下文字，使其更加专业，符合法律文本的需求，符合案件所需要的准确表述。请不要额外添加事实性内容。只需要返回优化后的文本:\n\n{text}"

        current_messages = self.messages.copy()
        current_messages.append({"role": "user", "content": prompt})
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=current_messages,
                temperature=0.1,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            return "出现错误，请检查你的API_KEY/URL_BASE/MODEL是否正确配置。错误原因：{}".format(e)

    def optimize_text_async(self, text: str, case_type='普通民事案件', isDefendant=False):
        prompt = f"""请对以下{case_type}{"起诉状" if isDefendant == False else "答辩状"}中的内容段落进行优化。

                        要求：
                        1. 保持原有事实内容不变，不添加、不删除任何事实性内容
                        2. 使用准确的法律术语和表述方式
                        3. 调整语言表达更加规范、专业
                        4. 确保表述逻辑清晰，因果关系明确
                        5. 删除口语化、情绪化的表达

                        原文内容：
                        {text}

                        请直接返回优化后的文本，不要包含任何说明、解释或其他内容。"""

        current_messages = self.messages.copy()
        current_messages.append({"role": "user", "content": prompt})
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=current_messages,
                temperature=0.1,
                max_tokens=4096,
                stream=True  # 启用流式输出
            )

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield "出现错误，请检查你的API_KEY/URL_BASE/MODEL是否正确配置。错误原因：{}".format(e)
