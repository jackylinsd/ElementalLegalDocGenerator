import streamlit as st
import json
from page.components.defendant import Respondent
from page.components.header import header
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import logging
import pandas as pd
from datetime import date, datetime
from page.components.ai_ui import AIComponent

logger = logging.getLogger(__name__)

CASE_TYPE = '离婚纠纷'
ai_server = AIComponent(case_type=CASE_TYPE)

def respondent_details(thisCase: dict):
    # 1. 对解除婚姻关系的确认和异议
    st.subheader("1. 对解除婚姻关系的确认和异议")
    q1_options = st.radio(label="对解除婚姻关系的确认和异议", options=["确认", "异议"], key="q1_options", horizontal=True, label_visibility="collapsed")
    q1_fact = st.text_area(label="具体原因", value="", key="q1_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q1_fact,"q1_fact_b",isDefendant=True)

    if q1_options == "确认":
        q1_detail = f'确认☑      异议☐\n{q1_fact}'
    else:
        q1_detail = f'确认☐      异议☑\n{q1_fact}'
    thisCase.reply_matters.append(q1_detail)

    # 2. 对夫妻共同财产诉请的确认和异议
    st.subheader("2. 对夫妻共同财产诉请的确认和异议")
    q2_options = st.radio(label="对夫妻共同财产诉请的确认和异议", options=["确认", "异议"], key="q2_options", horizontal=True, label_visibility="collapsed")
    q2_fact = st.text_area(label="具体原因", value="", key="q2_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q2_fact,"q2_fact_b",isDefendant=True)

    if q2_options == "确认":
        q2_detail = f'确认☑      异议☐\n{q2_fact}'
    else:
        q2_detail = f'确认☐      异议☑\n{q2_fact}'
    thisCase.reply_matters.append(q2_detail)

    # 3. 对夫妻共同债务诉请的确认和异议
    st.subheader("3. 对夫妻共同债务诉请的确认和异议")
    q3_options = st.radio(label="对夫妻共同债务诉请的确认和异议", options=["确认", "异议"], key="q3_options", horizontal=True, label_visibility="collapsed")
    q3_fact = st.text_area(label="具体原因", value="", key="q3_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q3_fact,"q3_fact_b",isDefendant=True)

    if q3_options == "确认":
        q3_detail = f'确认☑      异议☐\n{q3_fact}'
    else:
        q3_detail = f'确认☐      异议☑\n{q3_fact}'
    thisCase.reply_matters.append(q3_detail)

    # 4. 对子女直接抚养诉请的确认和异议
    st.subheader("4. 对子女直接抚养诉请的确认和异议")
    q4_options = st.radio(label="对子女直接抚养诉请的确认和异议", options=["确认", "异议"], key="q4_options", horizontal=True, label_visibility="collapsed")
    q4_fact = st.text_area(label="具体原因", value="", key="q4_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q4_fact,"q4_fact_b",isDefendant=True)

    if q4_options == "确认":
        q4_detail = f'确认☑      异议☐\n{q4_fact}'
    else:
        q4_detail = f'确认☐      异议☑\n{q4_fact}'
    thisCase.reply_matters.append(q4_detail)

    # 5. 对子女抚养费诉请的确认和异议
    st.subheader("5. 对子女抚养费诉请的确认和异议")
    q5_options = st.radio(label="对子女抚养费诉请的确认和异议", options=["确认", "异议"], key="q5_options", horizontal=True, label_visibility="collapsed")
    q5_fact = st.text_area(label="具体原因", value="", key="q5_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q5_fact,"q5_fact_b",isDefendant=True)

    if q5_options == "确认":
        q5_detail = f'确认☑      异议☐\n{q5_fact}'
    else:
        q5_detail = f'确认☐      异议☑\n{q5_fact}'
    thisCase.reply_matters.append(q5_detail)

    # 6. 对子女探望权诉请的确认和异议
    st.subheader("6. 对子女探望权诉请的确认和异议")
    q6_options = st.radio(label="对子女探望权诉请的确认和异议", options=["确认", "异议"], key="q6_options", horizontal=True, label_visibility="collapsed")
    q6_fact = st.text_area(label="具体原因", value="", key="q6_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q6_fact,"q6_fact_b",isDefendant=True)

    if q6_options == "确认":
        q6_detail = f'确认☑      异议☐\n{q6_fact}'
    else:
        q6_detail = f'确认☐      异议☑\n{q6_fact}'
    thisCase.reply_matters.append(q6_detail)

    # 7. 对赔偿/补偿/经济帮助的确认和异议
    st.subheader("7. 对赔偿/补偿/经济帮助的确认和异议")
    q7_options = st.radio(label="对赔偿/补偿/经济帮助的确认和异议", options=["确认", "异议"], key="q7_options", horizontal=True, label_visibility="collapsed")
    q7_fact = st.text_area(label="具体原因", value="", key="q7_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q7_fact,"q7_fact_b",isDefendant=True)

    if q7_options == "确认":
        q7_detail = f'确认☑      异议☐\n{q7_fact}'
    else:
        q7_detail = f'确认☐      异议☑\n{q7_fact}'
    thisCase.reply_matters.append(q7_detail)

    # 8. 其他事由
    st.subheader("8. 其他事由")
    q8_fact = st.text_area(label="其他事由", value="", key="q8_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q8_fact,"q8_fact_b",isDefendant=True)
    thisCase.reply_matters.append(q8_fact)

    # 9. 答辩的依据
    st.subheader("9. 答辩的依据")
    q9_fact = st.text_area(label="法律及司法解释的规定，要写明具体条文", value="", key="q9_fact", label_visibility="collapsed")
    ai_server.ai_optimize_text(q9_fact,"q9_fact_b",isDefendant=True)
    thisCase.reply_matters.append(q9_fact)

    # 10. 证据清单（可另附页）
    st.subheader("10. 证据清单（可另附页）")
    q10_fact = st.text_area(label="证据清单", value="附页", key="q10_fact", label_visibility="collapsed")
    thisCase.reply_matters.append(q10_fact)

class DivorceCaseFormatter(BaseCaseFormatter):
    """离婚案件数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE
    BaseCaseFormatter.isComplaint = False

    @staticmethod
    def format_case(case):
        """将离婚案件对象转换为适合文档模板的格式"""
        try:
            case_data = json.loads(case.to_json())

            # 调用父类的通用格式化方法
            template_data = super(DivorceCaseFormatter,
                                DivorceCaseFormatter).format_case(case)

            # 添加离婚案件的自定义部分
            template_data.update({
                "reply_matters": DivorceCaseFormatter._format_reply_matters(case_data)
            })

            return template_data

        except Exception as e:
            logger.error(f"格式化离婚案件数据时出错: {str(e)}")
            raise ValueError(f"格式化离婚案件数据失败: {str(e)}")

    @staticmethod
    def _format_reply_matters(case_data):
        """Format reply matters from the case data"""
        # Get the reply matters array from case data
        reply_matters = case_data.get('reply_matters', [])
        
        # The indices correspond to the questions in respondent_details
        matter_types = [
            "1. 对解除婚姻关系的确认和异议",
            "2. 对夫妻共同财产诉请的确认和异议",
            "3. 对夫妻共同债务诉请的确认和异议",
            "4. 对子女直接抚养诉请的确认和异议",
            "5. 对子女抚养费诉请的确认和异议",
            "6. 对子女探望权诉请的确认和异议",
            "7. 对赔偿/补偿/经济帮助的确认和异议",
            "8. 其他事由",
            "9. 答辩的依据",
            "10. 证据清单"
        ]

        formatted_matters = []
        
        # Format each reply matter with its corresponding type
        for i, matter_type in enumerate(matter_types):
            if i < len(reply_matters):
                formatted_matters.append({
                    "type": matter_type,
                    "information": reply_matters[i]
                })
            else:
                formatted_matters.append({
                    "type": matter_type,
                    "information": ""
                })

        return formatted_matters

class DivorceCaseRespondent:
    def __init__(self):
        self.respondent = None
        self.case_num = None
        self.reply_matters = []

    def to_json(self):
        # 自定义序列化函数
        def default_serializer(obj):
            if isinstance(obj, date):  # 处理 datetime.date 对象
                return obj.isoformat()
            elif hasattr(obj, '__dict__'):  # 处理普通对象
                return obj.__dict__
            elif isinstance(obj, pd.DataFrame):  # 处理 DataFrame 对象
                return obj.to_dict(orient='records')
            else:
                return str(obj)  # 其他情况转换为字符串

        # 使用自定义的序列化函数
        return json.dumps(self.__dict__, default=default_serializer, indent=4)

thisCase = DivorceCaseRespondent()


header(CASE_TYPE,"答辩状")

st.markdown("""______""")
st.subheader('案号')
thisCase.case_num = st.text_input('请输入案号：', '',placeholder='示例：(2025)粤01民终0001号')
st.header("当事人信息")
# 答辩人部分
respondent = Respondent(CASE_TYPE)
respondent.show()
thisCase.respondent = respondent
st.markdown("""______""")
st.header("答辩事项和依据（对原告诉讼请求的确认或者异议）")
respondent_details(thisCase)

if st.button("生成答辩状"):
    # 输出 JSON 格式的案件信息
    # st.write("案件信息（JSON 格式）:")
    # st.json(thisCase.to_json())


    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "defense_2p",
                thisCase,
                DivorceCaseFormatter,
                thisCase.respondent.respondents[0]["name"],
            )

        st.download_button(
            label="下载答辩状",
            data=doc_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"生成文档时出错: {str(e)}")
