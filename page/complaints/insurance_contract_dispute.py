import streamlit as st
from page.components.complaint import Plaintiff
from page.components.header import header
from page.components.ai_ui import AIComponent
from page.components.section import  CommonCasePlaintiff
from page.components.complaint import Defendant, Plaintiff, ThirdParty
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import json
from utils.tools import st_date_input


CASE_TYPE = "保证保险合同纠纷"

ai_component = AIComponent(CASE_TYPE)

REPLY_QUESTIONS = [
    "理赔款",
    "保险费、违约金等",
    "是否主张实现债权的费用",
    "其他请求",
    "标的总额",
    "请求依据"
]

REASON_QUESTIONS = [
    "保证保险合同的签订情况（合同名称、主体、签订时间、地点行等）",
    "保证保险合同的主要约定",
    "是否对被告就保证保险合同主要条款进行提示注意、说明",
    "被告借款合同的主要约定（借款金额、期限、用途、利息标准、还款方式、担保、违约责任、解除条件、管辖约定）",
    "被告逾期未还款情况",
    "保证保险合同的履行情况",
    "追索情况",
    "其他需要说明的内容（可另附页）",
    "证据清单（可另附页）",
]

thisCase = CommonCasePlaintiff()


def claim(thisCase):
    st.subheader("1. 理赔款")
    q1_1 = st.number_input("理赔款（人民币，下同；如外币需特别注明）",
                           key="claim_amount", placeholder="请输入理赔款")
    q1_2 = st.checkbox("外币")
    if q1_2:
        q1_3 = st.text_input("外币币种", key="claim_currency",
                             placeholder="请输入外币币种")
    thisCase.reply_matters.append({"type": "1. 理赔款", "information": f"支付理赔款{
                                   q1_1}元（{"人民币，下同；如外币需特别注明" if not q1_2 else q1_3}）；"})

    st.subheader("2. 保险费、违约金等")
    q2_1 = st_date_input("截至至以下日期", key="due_date")
    q2_2 = st.number_input(
        "欠保险费、违约金等共计", key="due_amount", placeholder="请输入金额")
    q2_3 = st_date_input("自以下日期之后的保险费、违约金等各项费用计算至实际清偿之日止", key="start_date")
    q2_4 = st.text_area("明细", key="details", placeholder="请输入明细")

    thisCase.reply_matters.append(
        {"type": "2. 保险费、违约金等", "information": f"截至{q2_1}止，欠保险费、违约金等共计{
            q2_2}元；自{q2_3}之后的保险费、违约金等各项费用按照保证保险合同约定计算至实际清偿之日止；\n明细：{q2_4}"}
    )

    st.subheader("3. 是否主张实现债权的费用")
    q3_1 = st.radio("是否主张实现债权的费用", ["否", "是"], key="claim_legal_fees",horizontal=True)
    if q3_1 == "是":
        q3_2 = st.text_area("费用明细", key="legal_fees_details",
                            placeholder="请输入费用明细")
        thisCase.reply_matters.append(
            {"type": "3. 是否主张实现债权的费用", "information": f"是☑  费用明细：{q3_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "3. 是否主张实现债权的费用", "information": "是☐  费用明细：\n否☑"}
        )

    st.subheader("4. 其他请求")
    q4_1 = st.text_area("其他请求", key="other_requests", placeholder="请输入其他请求")
    ai_component.ai_optimize_text(q4_1,"q4_1_b")
    thisCase.reply_matters.append(
        {"type": "4. 其他请求", "information": q4_1}
    )

    st.subheader("5. 标的总额")
    q5_1 = st.text_area("标的总额", key="total_amount", placeholder="请输入标的总额")
    thisCase.reply_matters.append(
        {"type": "5. 标的总额", "information": q5_1}
    )

    st.subheader("6. 请求依据")
    q6_1 = st.text_area("合同约定", key="contract_terms", placeholder="请输入合同约定")
    q6_2 = st.text_area("法律规定", key="legal_provisions", placeholder="请输入法律规定")
    thisCase.reply_matters.append(
        {"type": "6. 请求依据", "information": f"合同约定：{q6_1}\n法律规定：{q6_2}"}
    )


def fact(thisCase):
    st.subheader("1. 保证保险合同的签订情况")
    q7_1 = st.text_input("合同名称", key="contract_name", placeholder="请输入合同名称")
    q7_2 = st.text_input("合同主体", key="contract_parties", placeholder="请输入合同主体")
    q7_3 = st_date_input("签订时间", key="contract_date")
    q7_4 = st.text_input("签订地点", key="contract_location", placeholder="请输入签订地点")
    q7_5 = st.text_area("其他", key="other_signing_details", placeholder="请输入其他需要说明的内容，可留空")
    thisCase.reasons.append(
        {"type": "1. 保证保险合同的签订情况", "information": f"合同名称：{q7_1}；合同主体：{q7_2}；签订时间：{q7_3}；签订地点：{q7_4}\n{q7_5 if q7_5 else ''}"}
    )

    st.subheader("2. 保证保险合同的主要约定")
    q8_1 = st.text_input("保证保险金额", key="insurance_amount", placeholder="请输入保证保险金额")
    q8_2 = st.text_input("保费金额", key="premium_amount", placeholder="请输入保费金额")
    q8_3 = st.text_input("保险期间", key="insurance_period", placeholder="请输入保险期间")
    q8_4 = st.text_input("保险费缴纳方式", key="premium_payment_method", placeholder="请输入保险费缴纳方式")
    q8_5 = st.text_area("理赔条件", key="claim_conditions", placeholder="请输入理赔条件")
    q8_6 = st.text_area("理赔款项和未付保费的追索", key="claim_recovery", placeholder="请输入理赔款项和未付保费的追索")
    q8_7 = st.text_area("违约事由及违约责任", key="breach_terms", placeholder="请输入违约事由及违约责任")
    q8_8 = st.text_area("特别约定", key="special_terms", placeholder="请输入特别约定")
    q8_9 = st.text_area("其他", key="other_terms", placeholder="请输入其他约定")
    thisCase.reasons.append(
        {"type": "2. 保证保险合同的主要约定", "information": f"保证保险金额：{q8_1}元；\n保费金额：{q8_2}元；\n保险期间：{q8_3}；\n保险费缴纳方式：{q8_4}；\n理赔条件：{q8_5}；\n理赔款项和未付保费的追索：{q8_6}；\n违约事由及违约责任：{q8_7}；\n特别约定：{q8_8}；\n其他：{q8_9}"}
    )

    st.subheader("3. 是否对被告就保证保险合同主要条款进行提示注意、说明")
    q9_1 = st.radio("是否对被告进行提示注意、说明", ["是", "否"], key="notice_given", horizontal=True)
    if q9_1 == "是":
        q9_2 = st.text_area("提示说明的具体方式以及时间地点", key="notice_details", placeholder="请输入提示说明的具体方式以及时间地点")
        thisCase.reasons.append(
            {"type": "3. 是否对被告就保证保险合同主要条款进行提示注意、说明", "information": f"是☑  提示说明的具体方式以及时间地点：{q9_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "3. 是否对被告就保证保险合同主要条款进行提示注意、说明", "information": "是☐  提示说明的具体方式以及时间地点：\n否☑"}
        )

    st.subheader("4. 被告借款合同的主要约定")
    q10_1 = st.text_area("主要约定内容", key="loan_amount", placeholder="请输入借款金额、期限、用途、利息标准、还款方式、担保、违约责任、解除条件、管辖约定等")
    thisCase.reasons.append(
        {"type": "4. 被告借款合同的主要约定（借款金额、期限、用途、利息标准、还款方式、担保、违约责任、解除条件、管辖约定）", "information": f"{q10_1}"}
    )

    st.subheader("5. 被告逾期未还款情况")
    q11_0 = st.radio("填写方式",["模版填写", "自定义填写"],key="q11")
    if q11_0 == "模版填写":
        q11_1 = st_date_input("自以下日期开始", key="overdue_start_date",value="today")
        q11_2 = st_date_input("截至以下日期", key="overdue_end_date",value="today")
        q11_3 = st.number_input("已还款金额", key="repaid_amount", placeholder="请输入已还款金额")
        q11_4 = st.number_input("逾期但已还款金额", key="overdue_repaid_amount", placeholder="请输入逾期但已还款金额")
        q11_5 = st.number_input("共归还本金", key="principal_repaid", placeholder="请输入共归还本金")
        q11_6 = st.number_input("共归还利息", key="interest_repaid", placeholder="请输入共归还利息")
        q11_15 = st_date_input("自以下日期开始逾期", key="overdue_start_date_2", value="2025-01-01")
        q11_16 = st_date_input("逾期金额计算至以下日期", key="overdue_end_date_2", value="today")
        q11_7 = st.number_input("欠付借款本金", key="outstanding_principal", placeholder="请输入欠付借款本金")
        q11_8 = st.number_input("欠付利息", key="outstanding_interest", placeholder="请输入欠付利息")
        q11_9 = st.number_input("欠付罚息", key="outstanding_penalty", placeholder="请输入欠付罚息")
        q11_10 = st.number_input("欠付复利", key="outstanding_compound_interest", placeholder="请输入欠付复利")
        q11_11 = st.number_input("欠付滞纳金", key="outstanding_late_fee", placeholder="请输入欠付滞纳金")
        q11_12 = st.number_input("欠付违约金", key="outstanding_penalty_fee", placeholder="请输入欠付违约金")
        q11_13 = st.number_input("欠付手续费", key="outstanding_service_fee", placeholder="请输入欠付手续费")
        q11_14 = st.text_area("明细", key="overdue_details", placeholder="请输入明细")
        thisCase.reasons.append(
            {"type": "5. 被告逾期未还款情况", "information": f"自{q11_1}至{q11_2}，被告按约定还款，已还款{q11_3}元，逾期但已还款{q11_4}元，共归还本金{q11_5}元，利息{q11_6}元；自{q11_15}起，开始逾期不还，截至{q11_16}，被告欠付借款本金{q11_7}元、利息{q11_8}元、罚息{q11_9}元、复利{q11_10}元、滞纳金{q11_11}元、违约金{q11_12}元、手续费{q11_13}元；明细：{q11_14}"}
        )
    else:
        q11_1 = st.text_area("还款情况", key="overdue_start_date_2", placeholder="请输入还款情况的具体内容")
        thisCase.reasons.append(
            {"type": "5. 被告逾期未还款情况", "information": f"{q11_1}"}
        )

    st.subheader("6. 保证保险合同的履行情况")
    q12_0 = st.radio("填写方式",["模版填写", "自定义填写"],key="q12")
    if q12_0 == "模版填写":
        q12_1 = st_date_input("理赔日期", key="claim_date")
        q12_2 = st.number_input("理赔金额", key="claim_amount_2", placeholder="请输入理赔金额")
        q12_3 = st_date_input("权益转让确认书取得日期", key="assignment_date")
        thisCase.reasons.append(
            {"type": "6. 保证保险合同的履行情况", "information": f"原告于{q12_1}进行了理赔，代被告清偿债务，共赔款{q12_2}元，于{q12_3}取得权益转让确认书"}
        )
    else:
        q12_1 = st.text_area("履行情况", key="claim_amount_2", placeholder="请输入履行情况的具体内容")
        ai_component.ai_optimize_text(q12_1,"q12_1_b")
        thisCase.reasons.append(
            {"type": "6. 保证保险合同的履行情况", "information": f"{q12_1}"}
        )

    st.subheader("7. 追索情况")
    q13_0 = st.radio("填写方式",["模版填写", "自定义填写"],key="q13")
    if q13_0 == "模版填写":
        q13_1 = st_date_input("追索通知日期", key="demand_date",value="today")
        q13_2 = st.number_input("被告已支付保费", key="paid_premium", placeholder="请输入被告已支付保费")
        q13_3 = st.number_input("被告已归还借款", key="repaid_loan", placeholder="请输入被告已归还借款")
        q13_4 = st.number_input("尚欠保费", key="outstanding_premium", placeholder="请输入尚欠保费")
        q13_5 = st.number_input("欠付借款本金", key="outstanding_principal_2", placeholder="请输入欠付借款本金")
        q13_6 = st.number_input("欠付利息", key="outstanding_interest_2", placeholder="请输入欠付利息")
        q13_7 = st.number_input("欠付罚息", key="outstanding_penalty_2", placeholder="请输入欠付罚息")
        q13_8 = st.number_input("欠付复利", key="outstanding_compound_interest_2", placeholder="请输入欠付复利")
        q13_9 = st.number_input("欠付滞纳金", key="outstanding_late_fee_2", placeholder="请输入欠付滞纳金")
        q13_10 = st.number_input("欠付违约金", key="outstanding_penalty_fee_2", placeholder="请输入欠付违约金")
        q13_11 = st.number_input("欠付手续费", key="outstanding_service_fee_2", placeholder="请输入欠付手续费")
        q13_12 = st.text_area("明细", key="demand_details", placeholder="请输入明细")
        thisCase.reasons.append(
            {"type": "7. 追索情况", "information": f"原告于{q13_1}通知被告并向其追索；被告已支付保费{q13_2}元，归还借款{q13_3}元；尚欠保费{q13_4}元，欠付借款本金{q13_5}元、利息{q13_6}元、罚息{q13_7}元、复利{q13_8}元、滞纳金{q13_9}元、违约金{q13_10}元、手续费{q13_11}元；明细：{q13_12}"}
        )
    else:
        q13_1 = st.text_area("追索情况", key="demand_amount_2", placeholder="请输入追索情况的具体内容")
        ai_component.ai_optimize_text(q13_1,"q13_1_b")
        thisCase.reasons.append(
            {"type": "7. 追索情况", "information": f"{q13_1}"}
        )

    st.subheader("8. 其他需要说明的内容")
    q14_1 = st.text_area("其他需要说明的内容", key="other_notes", placeholder="请输入其他需要说明的内容")
    ai_component.ai_optimize_text(q14_1,"q14_1_b")
    thisCase.reasons.append(
        {"type": "8. 其他需要说明的内容", "information": q14_1}
    )

    st.subheader("9. 证据清单")
    q15_1 = st.text_area("证据清单", key="evidence_list", placeholder="请输入证据清单")
    thisCase.reasons.append(
        {"type": "9. 证据清单", "information": q15_1}
    )


class CreditCardCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE
    BaseCaseFormatter.isComplaint = True
    @staticmethod
    def format_case(thisCase):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(thisCase.to_json())
        template_data = super(CreditCardCaseFormatter,
                              CreditCardCaseFormatter).format_case(thisCase)

        template_data.update(
        {
            "reply_matters": thisCase.reply_matters,
            "reasons": thisCase.reasons,
        }
        )
        return template_data


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

# 第三人部分
third_party = ThirdParty()
third_party.show()
thisCase.third_party = third_party

st.markdown("""______""")
st.header("诉讼请求和依据")
claim(thisCase)

st.markdown("""______""")
st.header("约定管辖和诉讼保全")
thisCase.jurisdiction_and_preservation.show()

st.markdown("""______""")
st.header("事实和理由")
fact(thisCase)

if st.button("生成起诉状"):

    try:
        with st.spinner("生成中..."):
            doc_bytes, filename, preview = DocumentGenerator.generate_document(
                "complaint",
                thisCase,
                CreditCardCaseFormatter,
                thisCase.plaintiff.plaintiffs[0].get("name", ""),
                thisCase.defendant.defendants[0].get("name", ""),
            )

        with st.expander("预览"):
            st.markdown(preview, unsafe_allow_html=True)
            
        st.download_button(
            label="下载起诉状",
            data=doc_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        import traceback
        st.error(f"生成文档时出错: {str(e)}\n{str(traceback.print_exc())}")
