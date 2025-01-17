import streamlit as st
import json
from page.components.defendant import Respondent
from page.components.header import header
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
from page.components.section import (
    CreateSections,
    CommonCaseRespondent,
)

CASE_TYPE = "劳动争议纠纷"

new_sections = CreateSections(CASE_TYPE)

# 答辩事项问题列表
REPLY_QUESTIONS = [
    "对工资支付诉请的确认和异议",
    "对未签订书面劳动合同双倍工资诉请的确认和异议",
    "对未休年休假工资诉请的确认和异议",
    "对未依法缴纳社会保险费造成的经济损失诉请的确认和异议",
    "对解除劳动合同经济补偿诉请的确认和异议",
    "对违法解除劳动合同赔偿金诉请的确认和异议",
    "对劳动仲裁相关情况的确认和异议",
    "其他事由",
]



def respondent_details(thisCase):
    """答辩事项部分"""
    for i, question in enumerate(REPLY_QUESTIONS, 1):
        new_sections.create_radio_section(f"{i}. {question}", f"q{i}", thisCase.reply_matters)

    # 答辩依据部分
    st.subheader("10. 答辩的依据")
    law = st.text_area("法律及司法解释的规定，要写明具体条文", key="q10_1")
    thisCase.reply_matters.append(f"法律及司法解释的规定：{law}")

    # 证据清单
    st.subheader("11. 证据清单（可另附页）")
    evidence = st.text_area("证据清单", key="q11_1")
    thisCase.reply_matters.append(f"证据清单：{evidence}")





class LaborDisputeCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE
    BaseCaseFormatter.isComplaint = False

    @staticmethod
    def format_case(case):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(case.to_json())
        template_data = super(LaborDisputeCaseFormatter, LaborDisputeCaseFormatter).format_case(case)

        # 使用全局定义的问题列表
        reply_questions = REPLY_QUESTIONS + ["答辩的依据", "证据清单"]

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
            doc_bytes, filename = DocumentGenerator.generate_document(
                "defense_2p",
                thisCase,
                LaborDisputeCaseFormatter,
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
