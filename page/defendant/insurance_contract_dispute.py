import streamlit as st
import json
from page.components.defendant import Respondent
from page.components.header import header
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
from page.components.section import (
    CreateSections,
    CommonCaseRespondent,
)

CASE_TYPE = "保证保险合同纠纷"

new_sections = CreateSections(CASE_TYPE)

# 答辩事项问题列表
REPLY_QUESTIONS = [
    "对理赔款有无异议",
    "对实现债权的费用有无异议",
    "对其他请求有无异议",
    "对标的总额有无异议",
]

# 事实和理由问题列表
REASON_QUESTIONS = [
    "对保证保险合同的签订情况有无异议",
    "对保证保险合同的主要约定有无异议",
    "对原告对被告就保证保险合同主要条款进行提示注意、说明的情况有无异议",
    "对被告借款合同的主要约定有无异议",
    "对被告逾期未还款情况有无异议",
    "对保证保险合同的履行情况有无异议",
    "对追索情况有无异议",
    "有无其他免责/减责事由",
]


def respondent_details(thisCase):
    """答辩事项部分"""
    for i, question in enumerate(REPLY_QUESTIONS, 1):
        new_sections.create_radio_section(f"{i}. {question}", f"q{
            i}", thisCase.reply_matters, isDefendant=True)

    # 答辩依据部分
    st.subheader("6. 答辩依据")
    contract = st.text_area("合同约定", key="q6_1")
    law = st.text_area("法律规定", key="q6_2")
    thisCase.reply_matters.append(f"合同约定：{contract}\n法律规定：{law}")


def fact_reason(thisCase):
    """事实和理由部分"""
    for i, question in enumerate(REASON_QUESTIONS, 1):
        new_sections.create_radio_section(
            f"{i}. {question}", f"f{i}", thisCase.reasons, isDefendant=True)

    # 其他说明和证据清单
    new_sections.create_text_section(
        "9. 其他需要说明的内容（可另附页）", "f9_content", thisCase.reasons, isDefendant=True)
    new_sections.create_text_section(
        "10. 证据清单（可另附页）", "f10_content", thisCase.reasons, isDefendant=True)


class InsuranceCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE
    BaseCaseFormatter.isComplaint = False

    @staticmethod
    def format_case(case):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(case.to_json())
        template_data = super(InsuranceCaseFormatter,
                              InsuranceCaseFormatter).format_case(case)

        # 使用全局定义的问题列表
        reply_questions = REPLY_QUESTIONS + ["答辩依据"]
        reason_questions = REASON_QUESTIONS + [
            "其他需要说明的内容（可另附页）",
            "证据清单（可另附页）",
        ]

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
                "reasons": [
                    {"type": f"{i+1}. {q}", "information": info if info else ""}
                    for i, (q, info) in enumerate(
                        zip(
                            reason_questions,
                            case_data.get("reasons", [])
                            + [""]
                            * (
                                len(reason_questions)
                                - len(case_data.get("reasons", []))
                            ),
                        )
                    )
                ],
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

# 事实和理由
st.header("事实和理由（对起诉状事实与理由的确认或者异议）")
fact_reason(thisCase)

# 生成文档按钮
if st.button("生成答辩状"):
    # st.write("案件信息（JSON 格式）:")
    # st.json(thisCase.to_json())

    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "defense",
                thisCase,
                InsuranceCaseFormatter,
                thisCase.respondent.respondents[0]["name"],
            )

        st.download_button(
            label="下载答辩状",
            data=doc_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    except Exception as e:
        st.error(f"生成文档时出错: {str(e)}")
