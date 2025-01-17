import streamlit as st
from page.components.complaint import Plaintiff
from page.components.header import header
from page.components.ai_ui import AIComponent
from page.components.section import  CommonCasePlaintiff
from page.components.complaint import Defendant, Plaintiff, ThirdParty
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import json
from utils.tools import st_date_input

# 定义案件类型
CASE_TYPE = "融资租赁合同纠纷"

ai_component = AIComponent(CASE_TYPE)

# 定义诉讼请求和依据的问题
REPLY_QUESTIONS = [
    "支付全部未付租金",
    "违约金、滞纳金、损害赔偿金",
    "是否确认租赁物归原告所有",
    "请求解除合同",
    "返还租赁物，并赔偿因解除合同而受到的损失",
    "是否主张担保权利",
    "是否主张实现债权的费用",
    "其他请求",
    "标的总额",
    "请求依据"
]

# 定义事实和理由的问题
REASON_QUESTIONS = [
    "合同的签订情况",
    "签订主体",
    "租赁物情况",
    "合同约定的租金及支付方式",
    "合同约定的租赁期限、费用",
    "到期后租赁物归属",
    "合同约定的违约责任",
    "是否约定加速到期条款",
    "是否约定回收租赁物条件",
    "是否约定解除合同条件",
    "租赁物交付时间",
    "租赁物情况",
    "租金支付情况",
    "逾期未付租金情况",
    "是否签订物的担保（抵押、质押）合同",
    "担保人、担保物",
    "是否最高额担保（抵押、质押）",
    "是否办理抵押、质押登记",
    "是否签订保证合同",
    "保证方式",
    "其他担保方式",
    "其他需要说明的内容"
]

# 初始化案件对象
thisCase = CommonCasePlaintiff()

# 定义诉讼请求和依据部分
def claim(thisCase):
    st.subheader("主张")
    q0 = st.radio('原告在本次诉讼中的主张', ['支付全部未付租金', '解除合同'], key='identity', horizontal=True)

    if q0 == '支付全部未付租金':
        st.subheader("1. 支付全部未付租金")
        q1_1 = st.number_input("到期未付租金", key="due_rent", placeholder="请输入到期未付租金")
        q1_2 = st.number_input("未到期租金", key="undue_rent", placeholder="请输入未到期租金")
        q1_3 = st.number_input("留购价款", key="purchase_price", placeholder="请输入留购价款")
        q1_4 = st.checkbox('是否为外币')
        if q1_4:
            q1_5 = st.text_input("外币币种", key="currency_type", placeholder="请输入外币币种")
        q1_5 = st.text_input("明细",key='q1_details', placeholder="请输入其他还需说明的明细")
        thisCase.reply_matters.append(
            {"type": "1. 支付全部未付租金", "information": f"到期未付租金{q1_1}元、未到期租金{q1_2}元、留购价款{q1_3}元（{'人民币，下同；如外币需特别注明' if not q1_4 else q1_5})\n明细：{q1_5}"}
        )

        st.subheader("2. 违约金、滞纳金、损害赔偿金")
        q2_1 = st_date_input("截至日期", key="penalty_due_date")
        q2_2 = st.number_input("违约金", key="penalty_amount", placeholder="请输入违约金")
        q2_3 = st.number_input("滞纳金", key="late_fee", placeholder="请输入滞纳金")
        q2_4 = st.number_input("损害赔偿金", key="damages", placeholder="请输入损害赔偿金")
        q2_5 = st.text_input("计算基数", key="penalty_base", placeholder="请输入计算基数")
        q2_6 = st.text_input("计算标准", key="penalty_standard", placeholder="请输入计算标准")
        q2_7 = st.text_input("明细",key='q2_details', placeholder="请输入其他还需说明的明细")
        thisCase.reply_matters.append(
            {"type": "2. 违约金、滞纳金、损害赔偿金", "information": f"截至{q2_1}止，违约金{q2_2}元，滞纳金{q2_3}元，损害赔偿金{q2_4}元；自{q2_1}之后的违约金、滞纳金、损害赔偿金，以{q2_5}元为基数按照{q2_6}标准计算至全部款项实际付清之日。\n明细：{q2_7}"}
        )

        st.subheader("3. 是否确认租赁物归原告所有")
        q3_1 = st.radio("是否确认租赁物归原告所有", ["否", "是"], key="confirm_ownership", horizontal=True)
        thisCase.reply_matters.append(
            {"type": "3. 是否确认租赁物归原告所有", "information": f"是☑\n否☐" if q3_1 == "是" else "是☐\n否☑"}
        )

        thisCase.reply_matters.append(
            {"type": "4. 请求解除合同", "information": "判令解除融资租赁合同☐\n确认融资租赁合同已解除☐"}
        )
        thisCase.reply_matters.append(
            {"type": "5. 返还租赁物，并赔偿因解除合同而受到的损失", "information": "支付全部未付租金  元，到期未付租金  元、未到期租金  元、留购价款  元；截至  年  月  日止，违约金  元，滞纳金  元，损害赔偿金  元；自  之后的违约金、滞纳金、损害赔偿金，以  元为基数按照  标准计算至全部款项实际付清之日"}
        )
    
    if q0 == '解除合同':
        thisCase.reply_matters.append(
            {"type": "1. 支付全部未付租金", "information": "到期未付租金 元、未到期租金 元、留购价款 元（人民币，下同；如外币需特别注明）"}
        )
        thisCase.reply_matters.append(
            {"type": "2. 违约金、滞纳金、损害赔偿金", "information": "截至  年  月  日止，违约金  元，滞纳金  元，损害赔偿金  元；自  之后的违约金、滞纳金、损害赔偿金，以  元为基数按照  标准计算至全部款项实际付清之日。\n明细："}
        )
        thisCase.reply_matters.append(
            {"type": "3. 是否确认租赁物归原告所有", "information": "是☐\n否☐"}
        )

        st.subheader("4. 请求解除合同")
        q4_1 = st.radio("请求解除合同", ["判令解除融资租赁合同", "确认融资租赁合同已解除"], key="terminate_contract", horizontal=True)
        if q4_1 == "判令解除融资租赁合同":
            thisCase.reply_matters.append(
                {"type": "4. 请求解除合同", "information": "判令解除融资租赁合同☑\n确认融资租赁合同已解除☐"}
            )
        else:
            q4_2 = st_date_input("合同解除日期", key="contract_termination_date")
            thisCase.reply_matters.append(
                {"type": "4. 请求解除合同", "information": f"判令解除融资租赁合同☐\n确认融资租赁合同已于{q4_2}解除☑"}
            )

        st.subheader("5. 返还租赁物，并赔偿因解除合同而受到的损失")
        q5_1 = st.number_input("支付全部未付租金", key="total_unpaid_rent", placeholder="请输入支付全部未付租金")
        q5_2 = st.number_input("到期未付租金", key="due_unpaid_rent", placeholder="请输入到期未付租金")
        q5_3 = st.number_input("未到期租金", key="undue_unpaid_rent", placeholder="请输入未到期租金")
        q5_4 = st.number_input("留购价款（如约定）", key="purchase_price_loss", placeholder="请输入留购价款")
        q5_5 = st_date_input("截至日期", key="loss_due_date")
        q5_6 = st.number_input("违约金", key="penalty_amount_loss", placeholder="请输入违约金")
        q5_7 = st.number_input("滞纳金", key="late_fee_loss", placeholder="请输入滞纳金")
        q5_8 = st.number_input("损害赔偿金", key="damages_loss", placeholder="请输入损害赔偿金")
        q5_9 = st.text_input("计算基数", key="loss_base", placeholder="请输入计算基数")
        q5_10 = st.text_input("计算标准", key="loss_standard", placeholder="请输入计算标准")
        thisCase.reply_matters.append(
            {"type": "5. 返还租赁物，并赔偿因解除合同而受到的损失", "information": f"支付全部未付租金{q5_1}元，到期未付租金{q5_2}元、未到期租金{q5_3}元、留购价款{q5_4}元；截至{q5_5}止，违约金{q5_6}元，滞纳金{q5_7}元，损害赔偿金{q5_8}元；自{q5_5}之后的违约金、滞纳金、损害赔偿金，以{q5_9}元为基数按照{q5_10}标准计算至全部款项实际付清之日"}
        )





    # 共同项
    st.subheader("6. 是否主张担保权利")
    q6_1 = st.radio("是否主张担保权利", ["否", "是"], key="guarantee_rights", horizontal=True)
    if q6_1 == "是":
        q6_2 = st.text_area("内容", key="guarantee_details", placeholder="请输入担保权利内容")
        ai_component.ai_optimize_text(q6_2,"q6_2_b")
        thisCase.reply_matters.append(
            {"type": "6. 是否主张担保权利", "information": f"是☑ 内容：{q6_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "6. 是否主张担保权利", "information": "是☐ 内容：\n否☑"}
        )

    st.subheader("7. 是否主张实现债权的费用")
    q7_1 = st.radio("是否主张实现债权的费用", ["否", "是"], key="legal_fees", horizontal=True)
    if q7_1 == "是":
        q7_2 = st.text_area("费用明细", key="legal_fees_details", placeholder="请输入费用明细")
        ai_component.ai_optimize_text(q7_2,"q7_2_b")
        thisCase.reply_matters.append(
            {"type": "7. 是否主张实现债权的费用", "information": f"是☑ 费用明细：{q7_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "7. 是否主张实现债权的费用", "information": "是☐ 费用明细：\n否☑"}
        )

    st.subheader("8. 其他请求")
    q8_1 = st.text_area("其他请求", key="other_requests", placeholder="请输入其他请求")
    ai_component.ai_optimize_text(q8_1,"q8_1_b")
    thisCase.reply_matters.append(
        {"type": "8. 其他请求", "information": q8_1}
    )

    st.subheader("9. 标的总额")
    q9_1 = st.text_area("标的总额", key="total_amount", placeholder="请输入标的总额")
    ai_component.ai_optimize_text(q9_1,"q9_1_b")
    thisCase.reply_matters.append(
        {"type": "9. 标的总额", "information": q9_1}
    )

    st.subheader("10. 请求依据")
    q10_1 = st.text_area("合同约定", key="contract_terms", placeholder="请输入合同约定")
    q10_2 = st.text_area("法律规定", key="legal_provisions", placeholder="请输入法律规定")
    thisCase.reply_matters.append(
        {"type": "10. 请求依据", "information": f"合同约定：{q10_1}\n法律规定：{q10_2}"}
    )

# 定义事实和理由部分
def fact(thisCase):
    st.subheader("1. 合同的签订情况")
    q11_0 = st.radio("填写方式",['模版填写','自定义填写'],key="contract_signing_info",horizontal=True)
    if q11_0 == '模版填写':
        q11_1 = st.text_input("合同名称", key="contract_name", placeholder="请输入合同名称")
        q11_2 = st.text_input("合同编号", key="contract_number", placeholder="请输入合同编号")
        q11_3 = st_date_input("签订时间", key="contract_date")
        q11_4 = st.text_input("签订地点", key="contract_location", placeholder="请输入签订地点")
        thisCase.reasons.append(
            {"type": "1. 合同的签订情况", "information": f"合同名称：{q11_1}\n合同编号：{q11_2}\n签订时间：{q11_3}\n签订地点：{q11_4}"}
        )
    else:
        q11_t= st.text_area("签订情况", key="contract_info", placeholder="合同主体、签订时间、地点、合同名称等")
        ai_component.ai_optimize_text(q11_t,"q11_t_b")
        thisCase.reasons.append(
            {"type": "1. 合同的签订情况", "information": q11_t}
        )

    st.subheader("2. 签订主体")
    q12_1 = st.text_input("出租人", key="lessor", placeholder="请输入出租人")
    q12_2 = st.text_input("承租人", key="lessee", placeholder="请输入承租人")
    thisCase.reasons.append(
        {"type": "2. 签订主体", "information": f"出租人（卖方）：{q12_1}\n承租人（买方）：{q12_2}"}
    )

    st.subheader("3. 租赁物情况")
    q13_0 = st.radio("填写方式",['模版填写','自定义填写'],key="rental_info",horizontal=True)
    if q13_0 == '模版填写':
        q13_1 = st.text_input("租赁物名称", key="item_name", placeholder="请输入租赁物名称")
        q13_2 = st.text_input("规格", key="item_specification", placeholder="请输入规格")
        q13_3 = st.text_input("质量", key="item_quality", placeholder="请输入质量")
        q13_4 = st.number_input("数量", key="item_quantity", placeholder="请输入数量")
        thisCase.reasons.append(
            {"type": "3. 租赁物情况", "information": f"租赁物名称：{q13_1}\n规格：{q13_2}\n质量：{q13_3}\n数量：{q13_4}"}
        )
    else:
        q13_t = st.text_area("租赁物情况", key="item_info", placeholder="租赁物名称、规格、质量、数量等")
        ai_component.ai_optimize_text(q13_t,"q13_t_b")
        thisCase.reasons.append(
            {"type": "3. 租赁物情况", "information": q13_t}
        )

    st.subheader("4. 合同约定的租金及支付方式")
    q14_1 = st.number_input("租金", key="rent_amount", placeholder="请输入租金")
    q14_2 = st.radio("支付方式", ["现金", "转账", "票据", "其他"], key="payment_method", horizontal=True)
    if q14_2 == "票据":
        q14_3 = st.text_input("票据类型", key="bill_type", placeholder="请输入票据类型")
    if q14_2 == "其他":
        q14_3_o = st.text_input("其他支付方式", key="other_payment_method", placeholder="请输入其他支付方式")
    q14_4 = st.radio("支付方式", ["一次性", "分期"], key="payment_type", horizontal=True)
    if q14_4 == "分期":
        q14_5 = st.text_input("分期方式", key="installment_method", placeholder="请输入分期方式")

    q14_t_1 = ''
    for i in ["现金", "转账", "票据", "其他"]:
        if i == q14_2:
            q14_t_1 += f"{i}☑"
            if i == "票据":
                q14_t_1 += f"{q14_3}"
            elif i == "其他":
                q14_t_1 += f"其他：{q14_3_o}\n"
        else:
            q14_t_1 += f"{i}☐"

    thisCase.reasons.append(
        {"type": "4. 合同约定的租金及支付方式", "information": f"租金：{q14_1}元\n以{q14_t_1}方式\n{'一次性☑ 分期☐ 支付' if q14_4 == '一次性' else '一次性☐ 分期☑ 支付'}\n分期方式：{q14_5 if q14_4 == '分期' else ''}"}
    )

    st.subheader("5. 合同约定的租赁期限、费用")
    q15_1 = st_date_input("租赁期间开始日期", key="lease_start_date")
    q15_2 = st_date_input("租赁期间结束日期", key="lease_end_date")
    q15_3 = st.text_input("除租金外产生的费用", key="additional_fees", placeholder="请输入除租金外产生的费用")
    q15_4 = st.text_input("租赁费用承担方", key="lease_fee_bearer", placeholder="请输入租赁费用承担方")
    thisCase.reasons.append(
        {"type": "5. 合同约定的租赁期限、费用", "information": f"租赁期间自{q15_1}起至{q15_2}止\n除租金外产生的{q15_3}费用，由{q15_4}承担"}
    )

    st.subheader("6. 到期后租赁物归属")
    q16_1 = st.radio("到期后租赁物归属", ["归承租人所有", "归出租人所有"], key="ownership_after_lease", horizontal=True)
    if q16_1 == "归承租人所有":
        q16_2 = st.number_input("留购价款", key="purchase_price_ownership", placeholder="请输入留购价款")
        thisCase.reasons.append(
            {"type": "6. 到期后租赁物归属", "information": f"归承租人所有☑\n归出租人所有☐\n留购价款：{q16_2}元"}
        )
    else:
        thisCase.reasons.append(
            {"type": "6. 到期后租赁物归属", "information": f"归承租人所有☐\n归出租人所有☑\n留购价款："}
        )

    st.subheader("7. 合同约定的违约责任")
    q17_1 = st.text_area("违约责任", key="breach_terms", placeholder="请输入违约责任")
    ai_component.ai_optimize_text(q17_1,"q17_1_b")
    thisCase.reasons.append(
        {"type": "7. 合同约定的违约责任", "information": q17_1}
    )

    st.subheader("8. 是否约定加速到期条款")
    q18_1 = st.radio("是否约定加速到期条款", ["否", "是"], key="acceleration_clause", horizontal=True)
    if q18_1 == "是":
        q18_2 = st.text_area("具体内容", key="acceleration_details", placeholder="请输入具体内容")
        ai_component.ai_optimize_text(q18_2,"q18_2_b")
        thisCase.reasons.append(
            {"type": "8. 是否约定加速到期条款", "information": f"是☑ 具体内容：{q18_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "8. 是否约定加速到期条款", "information": "是☐ 具体内容：\n否☑"}
        )

    st.subheader("9. 是否约定回收租赁物条件")
    q19_1 = st.radio("是否约定回收租赁物条件", ["否", "是"], key="recovery_conditions", horizontal=True)
    if q19_1 == "是":
        q19_2 = st.text_area("具体内容", key="recovery_details", placeholder="请输入具体内容")
        ai_component.ai_optimize_text(q19_2,"q19_2_b")
        thisCase.reasons.append(
            {"type": "9. 是否约定回收租赁物条件", "information": f"是☑ 具体内容：{q19_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "9. 是否约定回收租赁物条件", "information": "是☐ 具体内容：\n否☑"}
        )

    st.subheader("10. 是否约定解除合同条件")
    q20_1 = st.radio("是否约定解除合同条件", ["否", "是"], key="termination_conditions", horizontal=True)
    if q20_1 == "是":
        q20_2 = st.text_area("具体内容", key="termination_details", placeholder="请输入具体内容")
        ai_component.ai_optimize_text(q20_2,"q20_2_b")
        thisCase.reasons.append(
            {"type": "10. 是否约定解除合同条件", "information": f"是☑ 具体内容：{q20_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "10. 是否约定解除合同条件", "information": "是☐ 具体内容：\n否☑"}
        )

    st.subheader("11. 租赁物交付时间")
    q21_1 = st_date_input("租赁物交付时间", key="delivery_date")
    thisCase.reasons.append(
        {"type": "11. 租赁物交付时间", "information": f"于{q21_1}交付租赁物"}
    )

    st.subheader("12. 租赁物情况")
    q22_1 = st.radio("质量是否符合约定或使用目的", ["否", "是"], key="quality_conformance", horizontal=True)
    if q22_1 == "否":
        q22_2 = st.text_area("具体情况", key="quality_issues", placeholder="请输入具体情况")
        ai_component.ai_optimize_text(q22_2,"q22_2_b")
        thisCase.reasons.append(
            {"type": "12. 租赁物情况", "information": f"质量符合约定或者承租人的使用目的☐\n存在瑕疵☑ 具体情况：{q22_2}"}
        )
    else:
        thisCase.reasons.append(
            {"type": "12. 租赁物情况", "information": f"质量符合约定或者承租人的使用目的☑\n存在瑕疵☐ 具体情况："}
        )

    st.subheader("13. 租金支付情况")
    q23_1 = st_date_input("租金支付开始日期", key="rent_payment_start_date")
    q23_2 = st_date_input("租金支付结束日期", key="rent_payment_end_date")
    q23_3 = st.number_input("已付租金", key="paid_rent", placeholder="请输入已付租金")
    q23_4 = st.number_input("逾期但已支付租金", key="overdue_paid_rent", placeholder="请输入逾期但已支付租金")
    q24_5 = st.text_input("明细",key="rent_payment_details", placeholder="请输入其他需说明的明细")
    thisCase.reasons.append(
        {"type": "13. 租金支付情况", "information": f"自{q23_1}至{q23_2}，按约定缴纳租金，已付租金{q23_3}元，逾期但已支付租金{q23_4}元\n明细：{q24_5}"}
    )

    st.subheader("14. 逾期未付租金情况")
    q24_1 = st_date_input("开始欠付租金日期", key="overdue_start_date")
    q24_2 = st_date_input("截至日期", key="overdue_end_date")
    q24_3 = st.number_input("欠付租金", key="overdue_rent", placeholder="请输入欠付租金")
    q24_4 = st.number_input("违约金", key="overdue_penalty", placeholder="请输入违约金")
    q24_5 = st.number_input("滞纳金", key="overdue_late_fee", placeholder="请输入滞纳金")
    q24_6 = st.number_input("损害赔偿金", key="overdue_damages", placeholder="请输入损害赔偿金")
    q24_7 = st.text_area("明细", key="overdue_details", placeholder="请输入明细")
    thisCase.reasons.append(
        {"type": "14. 逾期未付租金情况", "information": f"自{q24_1}起，开始欠付租金，截至{q24_2}，欠付租金{q24_3}元、违约金{q24_4}元，滞纳金{q24_5}元，损害赔偿金{q24_6}元，共计{q24_3 + q24_4 + q24_5 + q24_6}元；\n明细：{q24_7}"}
    )

    st.subheader("15. 是否签订物的担保（抵押、质押）合同")
    q25_1 = st.radio("是否签订物的担保合同", ["否", "是"], key="collateral_contract", horizontal=True)
    if q25_1 == "是":
        q25_2 = st_date_input("签订时间", key="collateral_contract_date")
        thisCase.reasons.append(
            {"type": "15. 是否签订物的担保（抵押、质押）合同", "information": f"是☑ 签订时间：{q25_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "15. 是否签订物的担保（抵押、质押）合同", "information": "是☐ 签订时间：\n否☑"}
        )

    st.subheader("16. 担保人、担保物")
    q26_1 = st.text_input("担保人", key="guarantor", placeholder="请输入担保人")
    q26_2 = st.text_input("担保物", key="collateral", placeholder="请输入担保物")
    thisCase.reasons.append(
        {"type": "16. 担保人、担保物", "information": f"担保人：{q26_1}\n担保物：{q26_2}"}
    )

    st.subheader("17. 是否最高额担保（抵押、质押）")
    q27_1 = st.radio("是否最高额担保", ["否", "是"], key="maximum_guarantee", horizontal=True)
    if q27_1 == "是":
        q27_2 = st_date_input("担保债权的确定时间", key="guarantee_determination_date")
        q27_3 = st.number_input("担保额度", key="guarantee_amount", placeholder="请输入担保额度")
        thisCase.reasons.append(
            {"type": "17. 是否最高额担保（抵押、质押）", "information": f"是☑ 担保债权的确定时间：{q27_2}\n担保额度：{q27_3}元\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "17. 是否最高额担保（抵押、质押）", "information": "是☐ 担保债权的确定时间：\n担保额度：\n否☑"}
        )

    st.subheader("18. 是否办理抵押、质押登记")
    q28_1 = st.radio("是否办理抵押、质押登记", ["否", "是"], key="collateral_registration", horizontal=True)
    if q28_1 == "是":
        q28_2 = st.radio("登记类型", ["正式登记", "预告登记"], key="registration_type", horizontal=True)
        thisCase.reasons.append(
            {"type": "18. 是否办理抵押、质押登记", "information": f"是☑ 登记类型：{'正式登记☑ 预告登记☐' if q28_2 == '正式登记' else '正式登记☐ 预告登记☑'}"}
        )
    else:
        thisCase.reasons.append(
            {"type": "18. 是否办理抵押、质押登记", "information": "是☐ 登记类型：正式登记☐ 预告登记☐\n否☑"}
        )

    st.subheader("19. 是否签订保证合同")
    q29_1 = st.radio("是否签订保证合同", ["否", "是"], key="guarantee_contract", horizontal=True)
    if q29_1 == "是":
        q29_2 = st_date_input("签订时间", key="guarantee_contract_date")
        q29_3 = st.text_input("保证人", key="guarantee_person", placeholder="请输入保证人")
        q29_4 = st.text_area("主要内容", key="guarantee_content", placeholder="请输入主要内容")
        thisCase.reasons.append(
            {"type": "19. 是否签订保证合同", "information": f"是☑ 签订时间：{q29_2}\n保证人：{q29_3}\n主要内容：{q29_4}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "19. 是否签订保证合同", "information": "是☐ 签订时间：\n保证人：\n主要内容：\n否☑"}
        )

    st.subheader("20. 保证方式")
    q30_1 = st.radio("保证方式", ["一般保证", "连带责任保证"], key="guarantee_type", horizontal=True)
    thisCase.reasons.append(
        {"type": "20. 保证方式", "information": f"保证方式：{'一般保证☑\n连带责任保证☐' if q30_1 == '一般保证' else '一般保证☐\n连带责任保证☑'}"}
    )

    st.subheader("21. 其他担保方式")
    q31_1 = st.radio("是否存在其他担保方式", ["否", "是"], key="other_guarantee", horizontal=True)
    if q31_1 == "是":
        q31_2 = st.text_input("担保形式", key="other_guarantee_form", placeholder="请输入担保形式")
        q31_3 = st_date_input("签订时间", key="other_guarantee_date")
        thisCase.reasons.append(
            {"type": "21. 其他担保方式", "information": f"是☑ 担保形式：{q31_2}；签订时间：{q31_3}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "21. 其他担保方式", "information": "是☐ 担保形式：\n签订时间：\n否☑"}
        )

    st.subheader("22. 其他需要说明的内容（可另附页）")
    q32_1 = st.text_area("其他需要说明的内容", key="other_information", placeholder="请输入其他需要说明的内容")
    ai_component.ai_optimize_text(q32_1,"q32_1_b")
    thisCase.reasons.append(
        {"type": "22. 其他需要说明的内容（可另附页）", "information": q32_1}
    )

    st.subheader("23.证据清单（可另附页）")
    q33_1 = st.text_area("证据清单（可另附页）", key="evidence_list", placeholder="请输入证据清单")
    thisCase.reasons.append(
        {"type": "23. 证据清单（可另附页）", "information": q33_1}
    )

# 定义数据格式化器
class FinancialLeaseCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(thisCase):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(thisCase.to_json())
        template_data = super(FinancialLeaseCaseFormatter,
                              FinancialLeaseCaseFormatter).format_case(thisCase)

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

# 生成起诉状
if st.button("生成起诉状"):
    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "complaint",
                thisCase,
                FinancialLeaseCaseFormatter,
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