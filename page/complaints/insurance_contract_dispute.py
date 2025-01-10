import streamlit as st
from page.components.complaint import Plaintiff
from page.components.jurisdiction_and_preservation import JurisdictionAndPreservation
from page.components.header import header

CASE_TYPE = "保证保险合同纠纷"

def claim():
    # 1. 理赔款
    st.subheader("1. 理赔款")
    claim_amount = st.number_input("支付理赔款（人民币，下同；如外币需特别注明）", key="claim_amount", min_value=0.0, format="%.2f")

    # 2. 保险费、违约金等
    st.subheader("2. 保险费、违约金等")
    insurance_debt_date = st.date_input("截至日期", key="insurance_debt_date")
    insurance_debt_amount = st.number_input("欠保险费、违约金等共计（元）", key="insurance_debt_amount", min_value=0.0, format="%.2f")
    insurance_details = st.text_area("明细", key="insurance_details", placeholder="请输入保险费、违约金等的明细")

    # 3. 是否主张实现债权的费用
    st.subheader("3. 是否主张实现债权的费用")
    claim_legal_fees = st.radio("是否主张实现债权的费用", [ "否","是"], key="claim_legal_fees")
    if claim_legal_fees == "是":
        legal_fees_details = st.text_area("费用明细", key="legal_fees_details", placeholder="请输入实现债权的费用明细")
    else:
        legal_fees_details = "无"

    # 4. 其他请求
    st.subheader("4. 其他请求")
    other_requests = st.text_area("其他请求", key="other_requests", placeholder="请输入其他请求的具体内容")

    # 5. 标的总额
    st.subheader("5. 标的总额")
    total_amount = st.number_input("标的总额（元）", key="total_amount", min_value=0.0, format="%.2f")

    # 6. 请求依据
    st.subheader("6. 请求依据")
    contract_basis = st.text_area("合同约定", key="contract_basis", placeholder="请输入合同约定的具体内容")
    legal_basis = st.text_area("法律规定", key="legal_basis", placeholder="请输入法律规定的具体内容")


def fact():
    # 1. 保证保险合同的签订情况
    st.subheader("1. 保证保险合同的签订情况")
    contract_name = st.text_input("合同名称", key="contract_name", placeholder="请输入合同名称")
    contract_parties = st.text_input("合同主体", key="contract_parties", placeholder="请输入合同主体")
    contract_date = st.date_input("签订时间", key="contract_date")
    contract_location = st.text_input("签订地点", key="contract_location", placeholder="请输入签订地点")
    insurance_amount = st.number_input("保证保险金额", key="insurance_amount", min_value=0.0, format="%.2f")
    premium_amount = st.number_input("保费金额", key="premium_amount", min_value=0.0, format="%.2f")
    insurance_period = st.text_input("保险期间", key="insurance_period", placeholder="请输入保险期间")

    # 2. 保证保险合同的主要约定
    st.subheader("2. 保证保险合同的主要约定")
    premium_payment_method = st.text_area("保险费缴纳方式", key="premium_payment_method", placeholder="请输入保险费缴纳方式")
    claim_conditions = st.text_area("理赔条件", key="claim_conditions", placeholder="请输入理赔条件")
    claim_recovery = st.text_area("理赔款项和未付保费的追索", key="claim_recovery", placeholder="请输入理赔款项和未付保费的追索")
    default_reasons = st.text_area("违约事由及违约责任", key="default_reasons", placeholder="请输入违约事由及违约责任")
    special_agreements = st.text_area("特别约定", key="special_agreements", placeholder="请输入特别约定")
    other_agreements = st.text_area("其他", key="other_agreements", placeholder="请输入其他约定")

    # 3. 是否对被告就保证保险合同主要条款进行提示注意、说明
    st.subheader("3. 是否对被告就保证保险合同主要条款进行提示注意、说明")
    notice_provided = st.radio("是否对被告进行提示说明", [ "否","是"], key="notice_provided")
    if notice_provided == "是":
        notice_details = st.text_area("提示说明的具体方式以及时间地点", key="notice_details", placeholder="请输入提示说明的具体方式以及时间地点")
    else:
        notice_details = "无"

    # 4. 被告借款合同的主要约定
    st.subheader("4. 被告借款合同的主要约定")
    loan_amount = st.number_input("借款金额", key="loan_amount", min_value=0.0, format="%.2f")
    loan_period = st.text_input("借款期限", key="loan_period", placeholder="请输入借款期限")
    loan_purpose = st.text_input("借款用途", key="loan_purpose", placeholder="请输入借款用途")
    interest_rate = st.text_input("利息标准", key="interest_rate", placeholder="请输入利息标准")
    repayment_method = st.text_input("还款方式", key="repayment_method", placeholder="请输入还款方式")
    guarantee = st.text_input("担保", key="guarantee", placeholder="请输入担保")
    default_liability = st.text_input("违约责任", key="default_liability", placeholder="请输入违约责任")
    termination_conditions = st.text_input("解除条件", key="termination_conditions", placeholder="请输入解除条件")
    jurisdiction_agreement = st.text_input("管辖约定", key="jurisdiction_agreement", placeholder="请输入管辖约定")

    # 5. 被告逾期未还款情况
    st.subheader("5. 被告逾期未还款情况")
    col1, col2 = st.columns(2)
    with col1:
        repayment_start_date = st.date_input("自", key="repayment_start_date")
    with col2:
        repayment_end_date = st.date_input("至", key="repayment_end_date")
    repaid_amount = st.number_input("被告按约定还款，已还款金额", key="repaid_amount", min_value=0.0, format="%.2f")
    overdue_repayment = st.number_input("逾期但已还款金额", key="overdue_repayment", min_value=0.0, format="%.2f")
    repaid_principal = st.number_input("共归还本金", key="repaid_principal", min_value=0.0, format="%.2f")
    repaid_interest = st.number_input("共归还利息", key="repaid_interest", min_value=0.0, format="%.2f")
    col3, col4 = st.columns(2)
    with col3:
        overdue_start_date = st.date_input("自年月日起，开始逾期不还", key="overdue_start_date")
    with col4:
        overdue_end_date = st.date_input("截至年月日", key="overdue_end_date")
    outstanding_principal = st.number_input("被告欠付借款本金", key="outstanding_principal", min_value=0.0, format="%.2f")
    outstanding_interest = st.number_input("欠付利息", key="outstanding_interest", min_value=0.0, format="%.2f")
    penalty_interest = st.number_input("罚息", key="penalty_interest", min_value=0.0, format="%.2f")
    compound_interest = st.number_input("复利", key="compound_interest", min_value=0.0, format="%.2f")
    late_fees = st.number_input("滞纳金", key="late_fees", min_value=0.0, format="%.2f")
    default_fees = st.number_input("违约金", key="default_fees", min_value=0.0, format="%.2f")
    service_fees = st.number_input("手续费", key="service_fees", min_value=0.0, format="%.2f")
    overdue_details = st.text_area("明细", key="overdue_details", placeholder="请输入逾期未还款的明细")

    # 6. 保证保险合同的履行情况
    st.subheader("6. 保证保险合同的履行情况")
    claim_date = st.date_input("原告于年月日进行了理赔", key="claim_date")
    satisfaction_of_debt = st.number_input("代被告清偿债务，共赔款元", key="satisfaction_of_debt", min_value=0.0, format="%.2f")
    rights_transfer_date = st.date_input("于年月日取得权益转让确认书", key="rights_transfer_date")

    # 7. 追索情况
    st.subheader("7. 追索情况")
    recovery_notice_date = st.date_input("原告于年月日通知被告并向其追索", key="recovery_notice_date")
    paid_premium = st.number_input("被告已支付保费元", key="paid_premium", min_value=0.0, format="%.2f")
    repaid_loan = st.number_input("归还借款元", key="repaid_loan", min_value=0.0, format="%.2f")
    outstanding_premium = st.number_input("尚欠保费元", key="outstanding_premium", min_value=0.0, format="%.2f")
    outstanding_loan_principal = st.number_input("欠付借款本金元", key="outstanding_loan_principal", min_value=0.0, format="%.2f")
    outstanding_loan_interest = st.number_input("欠付利息元", key="outstanding_loan_interest", min_value=0.0, format="%.2f")
    outstanding_penalty_interest = st.number_input("欠付罚息元", key="outstanding_penalty_interest", min_value=0.0, format="%.2f")
    outstanding_compound_interest = st.number_input("欠付复利元", key="outstanding_compound_interest", min_value=0.0, format="%.2f")
    outstanding_late_fees = st.number_input("欠付滞纳金元", key="outstanding_late_fees", min_value=0.0, format="%.2f")
    outstanding_default_fees = st.number_input("欠付违约金元", key="outstanding_default_fees", min_value=0.0, format="%.2f")
    outstanding_service_fees = st.number_input("欠付手续费元", key="outstanding_service_fees", min_value=0.0, format="%.2f")
    recovery_details = st.text_area("明细", key="recovery_details", placeholder="请输入追索情况的明细")

    # 8. 其他需要说明的内容
    st.subheader("8. 其他需要说明的内容")
    other_notes = st.text_area("其他需要说明的内容（可另附页）", key="other_notes", placeholder="请输入其他需要说明的内容")

    # 9. 证据清单（可另附页）
    st.subheader("9. 证据清单（可另附页）")
    evidence_list = st.text_area("证据清单（可另附页）", key="evidence_list", placeholder="请输入证据清单")







header(CASE_TYPE)

st.header("当事人信息")
Plaintiff("保证保险合同纠纷").show()
st.header("诉讼请求和依据")
claim()
st.header("约定管辖和诉讼保全")
JurisdictionAndPreservation()
st.header("事实与理由")
fact()

if st.button("生成起诉状",type='primary'):
    pass