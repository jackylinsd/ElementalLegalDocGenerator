import streamlit as st
from utils.ai_servers import AIServer


class AIComponent:
    def __init__(self, case_type='普通民事案件'):
        self.ai_server = AIServer()
        self.case_type = case_type

    def ai_optimize_text(self, text: str, id=None):
        if st.button("AI 优化", key=id):
            with st.spinner("AI 优化中"):
                ai_result = self.ai_server.optimize_text(text, self.case_type)
                with st.expander("展开"):
                    st.text_area(f"AI 优化结果", value=ai_result)
