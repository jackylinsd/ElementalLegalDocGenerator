import streamlit as st
import json
from page.components.defendant import Respondent
from page.components.header import header
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
from page.components.section import (
CreateSections,
    CommonCaseRespondent,
)

CASE_TYPE = "机动车交通事故责任纠纷"

new_sections = CreateSections(CASE_TYPE)

# 集中定义所有问题
REPLY_QUESTIONS = [
    "对交通事故事实有无异议",
    "对交通事故责任认定有无异议",
    "对各项费用有无异议",
    "对鉴定意见有无异议",
    "对原告诉讼请求有无异议",
]


def respondent_details(thisCase):
    """答辩事项部分"""
    for i, question in enumerate(REPLY_QUESTIONS, 1):
        new_sections.create_radio_section(f"{i}. {question}", f"q{i}", thisCase.reply_matters,isDefendant=True)

    new_sections.create_text_section("6. 证据清单（可另附页）", "q6", thisCase.reply_matters,isDefendant=True)


class TrafficAccidentCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE
    BaseCaseFormatter.isComplaint = False

    @staticmethod
    def format_case(case):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(case.to_json())
        template_data = super(
            TrafficAccidentCaseFormatter, TrafficAccidentCaseFormatter
        ).format_case(case)

        # 使用全局定义的问题列表
        reply_questions = REPLY_QUESTIONS + ["证据清单（可另附页）"]

        template_data.update(
            {
                "reply_matters": [
                    {"type": f"{i+1}. {q}", "information": info if info else ""}
                    for i, (q, info) in enumerate(
                        zip(
                            reply_questions,
                            case_data.get("reply_matters", [])
                            + [""]
                            * (
                                len(reply_questions)
                                - len(case_data.get("reply_matters", []))
                            ),
                        )
                    )
                ],
                "case_num": case_data.get("case_num", "")
            }
        )
        return template_data


thisCase = CommonCaseRespondent()

# 页面标题
header(CASE_TYPE, "答辩状")

# 案号输入
st.markdown("______")
st.subheader("案号")
thisCase.case_num = st.text_input(
    "请输入案号：", "", placeholder="示例：(2025)粤01民终0001号"
)

# 当事人信息
st.header("当事人信息")
respondent = Respondent(CASE_TYPE)
respondent.show()
thisCase.respondent = respondent

# 答辩事项和依据
st.markdown("______")
st.header("答辩事项和依据（对原告诉讼请求的确认或者异议）")
respondent_details(thisCase)


# 生成文档按钮
if st.button("生成答辩状"):
    # st.write("案件信息（JSON 格式）:")
    # st.json(thisCase.to_json())

    try:
        with st.spinner("生成中..."):
            doc_bytes, filename,preview = DocumentGenerator.generate_document(
                "defense_2p",
                thisCase,
                TrafficAccidentCaseFormatter,
                thisCase.respondent.respondents[0]["name"],
            )
        with st.expander("预览"):
            st.markdown(preview, unsafe_allow_html=True)
        st.download_button(
            label="下载答辩状",
            data=doc_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    except Exception as e:
        st.error(f"生成文档时出错: {str(e)}")
