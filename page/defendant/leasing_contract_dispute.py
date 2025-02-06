import streamlit as st
import json
from page.components.defendant import Respondent
from page.components.header import header
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
from page.components.section import (
CreateSections,
    CommonCaseRespondent,
)

CASE_TYPE = "融资租赁合同纠纷"

new_sections = CreateSections(CASE_TYPE)

# 集中定义所有问题
REPLY_QUESTIONS = [
    "对支付全部未付租金的诉请有无异议",
    "对违约金、滞纳金、损害赔偿金有无异议",
    "对确认租赁物归原告所有有无异议",
    "对解除合同有无异议",
    "对返还租赁物，并赔偿因解除合同而受到的损失有无异议",
    "对担保权利的诉请有无异议",
    "对实现债权的费用有无异议",
    "对其他请求有无异议",
    "对标的总额有无异议",
]

REASON_QUESTIONS = [
    "对合同签订情况有无异议",
    "对签订主体有无异议",
    "对租赁物情况有无异议",
    "对合同约定的租金及支付方式有无异议",
    "对合同约定的租赁期限、费用有无异议",
    "对到期后租赁物归属有无异议",
    "对合同约定的违约责任有无异议",
    "对是否约定加速到期条款有无异议",
    "对是否约定回收租赁物条件有无异议",
    "对是否约定解除合同条件有无异议",
    "对租赁物交付时间有无异议",
    "对租赁物情况有无异议",
    "对租金支付情况有无异议",
    "对逾期未付租金情况有无异议",
    "对是否签订物的担保合同有无异议",
    "对担保人、担保物有无异议",
    "对最高额抵押担保有无异议",
    "对是否办理抵押/质押登记有无异议",
    "对是否签订保证合同有无异议",
    "对保证方式有无异议",
    "对其他担保方式有无异议",
    "有无其他免责/减责事由",
]


def respondent_details(thisCase):
    """答辩事项部分"""
    for i, question in enumerate(REPLY_QUESTIONS, 1):
        new_sections.create_radio_section(f"{i}. {question}", f"q{i}", thisCase.reply_matters)

    # 答辩依据部分
    st.subheader("10. 答辩依据")
    contract = st.text_area("合同约定", key="q10_1")
    law = st.text_area("法律规定", key="q10_2")
    thisCase.reply_matters.append(f"合同约定：{contract}\n法律规定：{law}")


def fact_reason(thisCase):
    """事实和理由部分"""
    for i, question in enumerate(REASON_QUESTIONS, 1):
        new_sections.create_radio_section(f"{i}. {question}", f"f{i}", thisCase.reasons,isDefendant=True)

    # 其他说明和证据清单
    new_sections.create_text_section("23. 其他需要说明的内容", "f23_content", thisCase.reasons,isDefendant=True)
    new_sections.create_text_section("24. 证据清单", "f24_content", thisCase.reasons,isDefendant=True)


class FinancialLeaseCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE
    BaseCaseFormatter.isComplaint = False

    @staticmethod
    def format_case(case):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(case.to_json())
        template_data = super(
            FinancialLeaseCaseFormatter, FinancialLeaseCaseFormatter
        ).format_case(case)

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

# 事实和理由
st.header("事实和理由（对起诉状事实与理由的确认或者异议）")
fact_reason(thisCase)

# 生成文档按钮
if st.button("生成答辩状"):
    # st.write("案件信息（JSON 格式）:")
    # st.json(thisCase.to_json())

    try:
        with st.spinner("生成中..."):
            doc_bytes, filename,preview = DocumentGenerator.generate_document(
                "defense",
                thisCase,
                FinancialLeaseCaseFormatter,
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
