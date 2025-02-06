import streamlit as st
from utils.ai_servers import AIServer


class AIComponent:
    def __init__(self, case_type='普通民事案件'):
        self.ai_server = AIServer()
        self.case_type = case_type

    def ai_optimize_text(self, text: str, id=None, isDefendant=False):
        if st.button("AI 优化", key=id):
            if text == "":
                st.error("请输入文本")
                return
                
            placeholder = st.empty()
            full_response = ""
            
            with st.spinner("AI 优化中"):
                    for response_chunk in self.ai_server.optimize_text_async(text, self.case_type,isDefendant):
                        full_response += response_chunk
                        # 实时更新显示的内容
                        placeholder.markdown(full_response + "▌")
            with st.expander("展开"):        
                    # 完成后显示最终结果
                    placeholder.markdown("")
                    st.text_area("AI 优化结果（仅供参考，请复制所需内容至上方）", full_response)
                    # st.markdown(full_response)
