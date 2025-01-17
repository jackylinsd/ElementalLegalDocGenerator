import streamlit as st
from page.components.complaint import Plaintiff
from page.components.jurisdiction_and_preservation import JurisdictionAndPreservation
from page.components.header import header
from page.components.ai_ui import AIComponent
from page.components.section import create_text_section, create_radio_section, CommonCasePlaintiff
from page.components.complaint import Defendant, Plaintiff, ThirdParty
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import json
from utils.tools import st_date_input

# 定义案件类型
CASE_TYPE = "劳动争议纠纷"

ai_component = AIComponent(case_type=CASE_TYPE)

# 定义诉讼请求和依据的问题
REPLY_QUESTIONS = [
    "工资支付",
    "未签订书面劳动合同",
    "加班费",
    "未休年休假工资",
    "未依法缴纳社会保险",
    "解除劳动合同经济补偿",
    "违法解除劳动合同赔偿",
    "诉讼费用承担",
    "是否已经申请诉前保全"
]

# 定义事实和理由的问题
REASON_QUESTIONS = [
    "劳动合同签订情况",
    "劳动合同履行情况",
    "解除或终止劳动关系情况",
    "工伤情况",
    "劳动仲裁相关情况",
    "其他相关情况",
    "诉请依据",
    "证据清单"
]

# 初始化案件对象
thisCase = CommonCasePlaintiff()

# 定义诉讼请求和依据部分
def claim(thisCase):
    st.subheader("1. 是否主张工资支付")
    q1_1 = st.radio("是否主张工资支付", ["是", "否"], key="wage_claim", horizontal=True)
    if q1_1 == "是":
        q1_2 = st.text_area("明细", key="wage_details", placeholder="请输入工资支付明细")
        ai_component.ai_optimize_text(q1_2, "q1_2_b")
        thisCase.reply_matters.append(
            {"type": "1. 是否主张工资支付", "information": f"是☑ 明细：{q1_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "1. 是否主张工资支付", "information": "是☐ 明细：\n否☑"}
        )

    st.subheader("2. 是否主张未签订书面劳动合同")
    q2_1 = st.radio("是否主张未签订书面劳动合同", ["是", "否"], key="contract_claim", horizontal=True)
    if q2_1 == "是":
        q2_2 = st.text_area("明细", key="contract_details", placeholder="请输入未签订书面劳动合同明细")
        ai_component.ai_optimize_text(q2_2, "q2_2_b")
        thisCase.reply_matters.append(
            {"type": "2. 是否主张未签订书面劳动合同", "information": f"是☑ 明细：{q2_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "2. 是否主张未签订书面劳动合同", "information": "是☐ 明细：\n否☑"}
        )

    st.subheader("3. 是否主张加班费")
    q3_1 = st.radio("是否主张加班费", ["是", "否"], key="overtime_claim", horizontal=True)
    if q3_1 == "是":
        q3_2 = st.text_area("明细", key="overtime_details", placeholder="请输入加班费明细")
        ai_component.ai_optimize_text(q3_2, "q3_2_b")
        thisCase.reply_matters.append(
            {"type": "3. 是否主张加班费", "information": f"是☑ 明细：{q3_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "3. 是否主张加班费", "information": "是☐ 明细：\n否☑"}
        )

    st.subheader("4. 是否主张未休年休假工资")
    q4_1 = st.radio("是否主张未休年休假工资", ["是", "否"], key="vacation_claim", horizontal=True)
    if q4_1 == "是":
        q4_2 = st.text_area("明细", key="vacation_details", placeholder="请输入未休年休假工资明细")
        ai_component.ai_optimize_text(q4_2, "q4_2_b")
        thisCase.reply_matters.append(
            {"type": "4. 是否主张未休年休假工资", "information": f"是☑ 明细：{q4_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "4. 是否主张未休年休假工资", "information": "是☐ 明细：\n否☑"}
        )

    st.subheader("5. 是否主张未依法缴纳社会保险")
    q5_1 = st.radio("是否主张未依法缴纳社会保险", ["是", "否"], key="social_security_claim", horizontal=True)
    if q5_1 == "是":
        q5_2 = st.text_area("明细", key="social_security_details", placeholder="请输入未依法缴纳社会保险明细")
        ai_component.ai_optimize_text(q5_2, "q5_2_b")
        thisCase.reply_matters.append(
            {"type": "5. 是否主张未依法缴纳社会保险", "information": f"是☑ 明细：{q5_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "5. 是否主张未依法缴纳社会保险", "information": "是☐ 明细：\n否☑"}
        )

    st.subheader("6. 是否主张解除劳动合同经济补偿")
    q6_1 = st.radio("是否主张解除劳动合同经济补偿", ["是", "否"], key="compensation_claim", horizontal=True)
    if q6_1 == "是":
        q6_2 = st.text_area("明细", key="compensation_details", placeholder="请输入解除劳动合同经济补偿明细")
        ai_component.ai_optimize_text(q6_2, "q6_2_b")
        thisCase.reply_matters.append(
            {"type": "6. 是否主张解除劳动合同经济补偿", "information": f"是☑ 明细：{q6_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "6. 是否主张解除劳动合同经济补偿", "information": "是☐ 明细：\n否☑"}
        )

    st.subheader("7. 是否主张违法解除劳动合同赔偿")
    q7_1 = st.radio("是否主张违法解除劳动合同赔偿", ["是", "否"], key="illegal_dismissal_claim", horizontal=True)
    if q7_1 == "是":
        q7_2 = st.text_area("明细", key="illegal_dismissal_details", placeholder="请输入违法解除劳动合同赔偿明细")
        ai_component.ai_optimize_text(q7_2, "q7_2_b")
        thisCase.reply_matters.append(
            {"type": "7. 是否主张违法解除劳动合同赔偿", "information": f"是☑ 明细：{q7_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "7. 是否主张违法解除劳动合同赔偿", "information": "是☐ 明细：\n否☑"}
        )

    st.subheader("8. 本表未列明的其他请求")
    q8_1 = st.text_area("本表未列明的其他请求", key="other_requests", placeholder="请输入其他请求")
    ai_component.ai_optimize_text(q8_1, "q8_1_b")
    thisCase.reply_matters.append(
        {"type": "8. 本表未列明的其他请求", "information": q8_1}
    )

    st.subheader("9. 诉讼费用承担")
    q9_1 = st.text_area("诉讼费用承担", key="legal_costs", placeholder="金额及具体主张")
    ai_component.ai_optimize_text(q9_1, "q9_1_b")
    thisCase.reply_matters.append(
        {"type": "9. 诉讼费用承担", "information": q9_1}
    )

    st.subheader("10. 是否已经申请诉前保全")
    q10_1 = st.radio("是否已经申请诉前保全", ["否", "是"], key="preservation_claim", horizontal=True)
    if q10_1 == "是":
        q10_2 = st.text_input("保全法院", key="preservation_apply_court", placeholder="请输入保全法院的名称")
        q10_3 = st.text_input("保全文书", key="preservation_apply_doc", placeholder="请输入保全文书信息")
        thisCase.reply_matters.append(
            {"type": "10. 是否已经申请诉前保全", "information": f"是☑\n保全法院：{q10_2}\n保全文书：{q10_3}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "10. 是否已经申请诉前保全", "information": f"是☐\n保全法院：\n保全文书：\n否☑"}
        )

# 定义事实和理由部分
def fact(thisCase):
    st.subheader("1. 劳动合同签订情况")
    q11_0 = st.radio("填写方式", ["模版填写", "自定义填写"], key="q11", horizontal=True)
    if q11_0 == "模版填写":
        q11_1 = st.text_input("合同主体", key="contract_party", placeholder="请输入合同主体")
        q11_2 = st.text_input("签订时间", key="contract_sign_date", placeholder="请输入签订时间")
        q11_3 = st.text_input("签订地点", key="contract_sign_location", placeholder="请输入签订地点")
        q11_4 = st.text_input("合同名称", key="contract_name", placeholder="请输入合同名称")
        thisCase.reasons.append(
            {"type": "1. 劳动合同签订情况", "information": f"合同主体：{q11_1}\n签订时间：{q11_2}\n签订地点：{q11_3}\n合同名称：{q11_4}"}
        )
    else:
        q11_t = st.text_area("签订情况", key="contract_info", placeholder="合同主体、签订时间、地点、合同名称等")
        ai_component.ai_optimize_text(q11_t, "q11_t_b")
        thisCase.reasons.append(
            {"type": "1. 劳动合同签订情况", "information": q11_t}
        )

    st.subheader("2. 劳动合同履行情况")
    q12_0 = st.radio("填写方式", ["模版填写", "自定义填写"], key="q12", horizontal=True)
    if q12_0 == "模版填写":
        q12_1 = st.text_input("入职时间", key="employment_date", placeholder="请输入入职时间")
        q12_2 = st.text_input("用人单位", key="employer", placeholder="请输入用人单位")
        q12_3 = st.text_input("工作岗位", key="job_position", placeholder="请输入工作岗位")
        q12_4 = st.text_input("工作地点", key="work_location", placeholder="请输入工作地点")
        q12_5 = st.text_input("合同约定的每月工资数额及工资构成", key="contract_salary", placeholder="请输入合同约定的每月工资数额及工资构成")
        q12_6 = st.text_input("办理社会保险的时间及险种", key="social_security", placeholder="请输入办理社会保险的时间及险种")
        q12_7 = st.text_input("劳动者实际领取的每月工资数额及工资构成", key="actual_salary", placeholder="请输入劳动者实际领取的每月工资数额及工资构成")
        q12_8 = st.text_input("加班工资计算基数及计算方法", key="overtime_calculation", placeholder="请输入加班工资计算基数及计算方法")
        q12_9 = st.text_input("原告加班时间及加班费", key="overtime_details_reason", placeholder="请输入原告加班时间及加班费")
        q12_10 = st.text_input("年休假", key="annual_leave", placeholder="请输入年休假信息")
        thisCase.reasons.append(
            {"type": "2. 劳动合同履行情况", "information": f"入职时间：{q12_1}\n用人单位：{q12_2}\n工作岗位：{q12_3}\n工作地点：{q12_4}\n合同约定的每月工资数额及工资构成：{q12_5}\n办理社会保险的时间及险种：{q12_6}\n劳动者实际领取的每月工资数额及工资构成：{q12_7}\n加班工资计算基数及计算方法：{q12_8}\n原告加班时间及加班费：{q12_9}\n年休假：{q12_10}"}
        )
    else:
        q12_t = st.text_area("履行情况", key="employment_info", placeholder="入职时间、用人单位、工作岗位、工作地点、合同约定的每月工资数额及工资构成、办理社会保险的时间及险种、劳动者实际领取的每月工资数额及工资构成、加班工资计算基数及计算方法、原告加班时间及加班费、年休假等")
        ai_component.ai_optimize_text(q12_t, "q12_t_b")
        thisCase.reasons.append(
            {"type": "2. 劳动合同履行情况", "information": q12_t}
        )

    st.subheader("3. 解除或终止劳动关系情况")
    q13_0 = st.radio("填写方式", ["模版填写", "自定义填写"], key="q13", horizontal=True)
    if q13_0 == "模版填写":
        q13_1 = st.text_input("解除或终止劳动关系的原因", key="termination_reason", placeholder="请输入解除或终止劳动关系的原因")
        q13_2 = st.text_input("经济补偿/赔偿金数额", key="compensation_amount", placeholder="请输入经济补偿/赔偿金数额")
        thisCase.reasons.append(
            {"type": "3. 解除或终止劳动关系情况", "information": f"解除或终止劳动关系的原因：{q13_1}\n经济补偿/赔偿金数额：{q13_2}"}
        )
    else:
        q13_t = st.text_area("解除或终止劳动关系情况", key="termination_info", placeholder="解除或终止劳动关系的原因、经济补偿/赔偿金数额等")
        ai_component.ai_optimize_text(q13_t, "q13_t_b")
        thisCase.reasons.append(
            {"type": "3. 解除或终止劳动关系情况", "information": q13_t}
        )

    st.subheader("4. 工伤情况")
    q14_0 = st.radio("填写方式", ["模版填写", "自定义填写"], key="q14", horizontal=True)
    if q14_0 == "模版填写":
        q14_1 = st.text_input("发生工伤时间", key="injury_date", placeholder="请输入发生工伤时间")
        q14_2 = st.text_input("工伤认定情况", key="injury_identification", placeholder="请输入工伤认定情况")
        q14_3 = st.text_input("工伤伤残等级", key="injury_level", placeholder="请输入工伤伤残等级")
        q14_4 = st.text_input("工伤费用", key="injury_cost", placeholder="请输入工伤费用")
        thisCase.reasons.append(
            {"type": "4. 工伤情况", "information": f"发生工伤时间：{q14_1}\n工伤认定情况：{q14_2}\n工伤伤残等级：{q14_3}\n工伤费用：{q14_4}"}
        )
    else:
        q14_t = st.text_area("工伤情况", key="injury_info", placeholder="发生工伤时间、工伤认定情况、工伤伤残等级、工伤费用等")
        ai_component.ai_optimize_text(q14_t, "q14_t_b")
        thisCase.reasons.append(
            {"type": "4. 工伤情况", "information": q14_t}
        )

    st.subheader("5. 劳动仲裁相关情况")
    q15_0 = st.radio("填写方式", ["模版填写", "自定义填写"], key="q15", horizontal=True)
    if q15_0 == "模版填写":
        q15_1 = st.text_input("申请劳动仲裁时间", key="arbitration_date", placeholder="请输入申请劳动仲裁时间")
        q15_2 = st.text_input("仲裁请求", key="arbitration_request", placeholder="请输入仲裁请求")
        q15_3 = st.text_input("仲裁文书", key="arbitration_document", placeholder="请输入仲裁文书")
        q15_4 = st.text_input("仲裁结果", key="arbitration_result", placeholder="请输入仲裁结果")
        thisCase.reasons.append(
            {"type": "5. 劳动仲裁相关情况", "information": f"申请劳动仲裁时间：{q15_1}\n仲裁请求：{q15_2}\n仲裁文书：{q15_3}\n仲裁结果：{q15_4}"}
        )
    else:
        q15_t = st.text_area("劳动仲裁相关情况", key="arbitration_info", placeholder="申请劳动仲裁时间、仲裁请求、仲裁文书、仲裁结果等")
        ai_component.ai_optimize_text(q15_t, "q15_t_b")
        thisCase.reasons.append(
            {"type": "5. 劳动仲裁相关情况", "information": q15_t}
        )

    st.subheader("6. 其他相关情况")
    q16_1 = st.text_area("其他可能与本案相关的情况", key="other_information", placeholder="请输入其他可能与本案相关的情况，如是否为农民工等")
    ai_component.ai_optimize_text(q16_1, "q16_1_b")
    thisCase.reasons.append(
        {"type": "6. 其他相关情况", "information": q16_1}
    )

    st.subheader("7. 诉请依据")
    q17_1 = st.text_area("法律及司法解释的规定", key="legal_basis", placeholder="法律及司法解释的规定，要写明具体条文")
    ai_component.ai_optimize_text(q17_1, "q17_1_b")
    thisCase.reasons.append(
        {"type": "7. 诉请依据", "information": q17_1}
    )

    st.subheader("8. 证据清单（可另附页）")
    q18_1 = st.text_area("证据清单（可另附页）", key="evidence_list", placeholder="请输入证据清单（可另附页）")
    thisCase.reasons.append(
        {"type": "8. 证据清单（可另附页）", "information": q18_1}
    )

# 定义数据格式化器
class LaborDisputeCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(thisCase):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(thisCase.to_json())
        template_data = super(LaborDisputeCaseFormatter,
                              LaborDisputeCaseFormatter).format_case(thisCase)

        template_data.update(
            {
                "reply_matters": thisCase.reply_matters,
                "reasons": thisCase.reasons,
            }
        )
        return template_data

# 页面布局
header(CASE_TYPE)
st.markdown("""______""")
st.header("当事人信息")
# 原告部分
plaintiff = Plaintiff(CASE_TYPE)
plaintiff.show()
thisCase.plaintiff = plaintiff

# 被告部分
defendant = Defendant(CASE_TYPE)
defendant.show()
thisCase.defendant = defendant

st.markdown("""______""")
st.header("诉讼请求和依据")
claim(thisCase)

st.markdown("""______""")
st.header("事实和理由")
fact(thisCase)

# 生成起诉状
if st.button("生成起诉状"):
    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "complaint_2p",
                thisCase,
                LaborDisputeCaseFormatter,
                thisCase.plaintiff.plaintiffs[0].get("name", ""),
                thisCase.defendant.defendants[0].get("name", ""),
            )

        st.download_button(
            label="下载起诉状",
            data=doc_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"生成文档时出错: {str(e)}")