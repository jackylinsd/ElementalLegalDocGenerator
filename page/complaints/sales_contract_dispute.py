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
CASE_TYPE = "买卖合同纠纷"

ai_component = AIComponent(case_type=CASE_TYPE)

# 定义诉讼请求和依据的问题
REPLY_QUESTIONS = [
    "给付价款（元）",
    "迟延给付价款的利息（违约金）",
    "赔偿因卖方违约所受的损失",
    "是否对标的物的瑕疵承担责任",
    "要求继续履行或是解除合同",
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
    "买卖标的物情况",
    "合同约定的价格及支付方式",
    "合同约定的交货时间、地点、方式、风险承担、安装、调试、验收",
    "合同约定的质量标准及检验方式、质量异议期限",
    "合同约定的违约金（定金）",
    "价款支付及标的物交付情况",
    "是否存在迟延履行",
    "是否催促过履行",
    "买卖合同标的物有无质量争议",
    "标的物质量规格或履行方式是否存在不符合约定的情况",
    "是否曾就标的物质量问题进行协商",
    "被告应当支付的利息、违约金、赔偿金",
    "是否签订物的担保（抵押、质押）合同",
    "担保人、担保物",
    "是否最高额担保（抵押、质押）",
    "是否办理抵押、质押登记",
    "是否签订保证合同",
    "保证方式",
    "其他担保方式"
]

# 初始化案件对象
thisCase = CommonCasePlaintiff()

# 定义诉讼请求和依据部分
def claim(thisCase):
    st.subheader("身份")
    q0 = st.radio('在买卖合同中的身份',['买家','卖家'],key='identity',horizontal=True)
    if q0 == '买家':
        st.subheader("1. 给付价款（元）")
        q1_1 = st.number_input("给付价款（元）", key="payment_amount", placeholder="请输入给付价款金额（人民币）")
        q1_2 = st.checkbox('是否为外币')
        if q1_2 == True:
            q1_3 = st.text_input("外币币种", key="payment_currency",
                                 placeholder="请输入外币币种")
        thisCase.reply_matters.append(
            {"type": "1. 给付价款（元）", "information": f"{q1_1}元({'人民币，下同；如外币需特别注明' if not q1_2 else q1_3})"}
        )

        st.subheader("2. 迟延给付价款的利息（违约金）")
        q2_1 = st_date_input("截至日期", key="interest_due_date")
        q2_2 = st.number_input("迟延给付价款的利息", key="interest_amount", placeholder="请输入迟延给付价款的利息")
        q2_3 = st.number_input("违约金", key="penalty_amount", placeholder="请输入违约金")
        q2_4 = st.text_input("逾期利息、违约金计算基数", key="interest_base", placeholder="请输入逾期利息、违约金计算基数")
        q2_5 = st.text_input("计算标准", key="interest_standard", placeholder="请输入计算标准")
        q2_6 = st.radio("是否请求支付至实际清偿之日止", ["否", "是"], key="interest_until_payment", horizontal=True)
        thisCase.reply_matters.append(
            {"type": "2. 迟延给付价款的利息（违约金）", "information": f"截至{q2_1}止，迟延给付价款的利息{q2_2}元、违约金{q2_3}元，自{q2_1}之后的逾期利息、违约金，以{q2_4}元为基数按照{q2_5}标准计算；是否请求支付至实际清偿之日止：{'是☑ 否☐' if q2_6 == '是' else '是☐ 否☑'}"}
        )

        thisCase.reply_matters.append({"type": "3. 赔偿因卖方违约所受的损失", "information": f"支付赔偿金 元\n违约类型：迟延履行☐   不履行☐  其他☐\n具体情形： \n损失计算依据："})
        thisCase.reply_matters.append({"type": "4. 是否对标的物的瑕疵承担责任", "information": "是☐ 责任方式：修理☐ 重作☐ 更换☐ 退货☐ 减少价款或者报酬☐ 其他☐：\n否☐"})

    if q0 == '卖家':
        thisCase.reply_matters.append(
                    {"type": "1. 给付价款（元）", "information": " 元"}
                )
        thisCase.reply_matters.append(
                    {"type": "2. 迟延给付价款的利息（违约金）", "information": f"截至  年 月 日止，迟延给付价款的利息  元、违约金  元，自  年 月 日之后的逾期利息、违约金，以  元为基数按照  标准计算；是否请求支付至实际清偿之日止：是☐ 否☐"}
                )

        st.subheader("3. 赔偿因卖方违约所受的损失")
        q3_1 = st.number_input("赔偿金", key="compensation_amount", placeholder="请输入赔偿金")
        q3_2 = st.radio("违约类型", ["迟延履行", "不履行", "其他"], key="breach_type", horizontal=True)   
        q3_3 = st.text_area("具体情形", key="breach_details", placeholder="请输入具体情形")
        q3_4 = st.text_area("损失计算依据", key="loss_calculation", placeholder="请输入损失计算依据")
        q3_2_t = ''
        for i in ["迟延履行", "不履行", "其他"]:
            if q3_2 == i:
                q3_2_t += f"{i}☑  "
            else:
                q3_2_t += f"{i}☐  "
        thisCase.reply_matters.append(
            {"type": "3. 赔偿因卖方违约所受的损失", "information": f"支付赔偿金{q3_1}元；\n违约类型：{q3_2_t}；\n具体情形：{q3_3}；\n损失计算依据：{q3_4}"}
        )

        st.subheader("4. 是否对标的物的瑕疵承担责任")
        q4_1 = st.radio("是否对标的物的瑕疵承担责任", ["否", "是"], key="defect_responsibility", horizontal=True)
        if q4_1 == "是":
            q4_2 = st.radio("责任方式", ["修理", "重作", "更换", "退货", "减少价款或者报酬", "其他"], key="defect_action", horizontal=True)
            if q4_2 == "其他":
                q4_3 = st.text_area("其他责任方式", key="other_defect_action", placeholder="请输入其他责任方式")
            q4_2_t = ''
            for i in ["修理", "重作", "更换", "退货", "减少价款或者报酬"]:
                if q4_2 == i:
                    q4_2_t += f"{i}☑  "
                else:
                    q4_2_t += f"{i}☐  "
            thisCase.reply_matters.append(
                {"type": "4. 是否对标的物的瑕疵承担责任", "information": f"是☑ 责任方式：{q4_2} {'其他☑：' + q4_3 if q4_2 == '其他' else '其他☐：'}\n否☐"}
            )
        else:
            thisCase.reply_matters.append(
                {"type": "4. 是否对标的物的瑕疵承担责任", "information": "是☐ 责任方式：修理☐ 重作☐ 更换☐ 退货☐ 减少价款或者报酬☐ 其他☐：\n否☑"}
            )

    st.subheader("5. 要求继续履行或是解除合同")
    q5_1 = st.radio("要求继续履行或是解除合同", ["继续履行", "解除合同", "确认合同已解除"], key="contract_action", horizontal=True)
    if q5_1 == "继续履行":
        q5_2 = st.text_input("多少日内履行完毕", key="fulfillment_period", placeholder="日数")
        q5_3 = st.radio("履行义务", ["付款", "供货"], key="fulfillment_obligation", horizontal=True)
        thisCase.reply_matters.append(
            {"type": "5. 要求继续履行或是解除合同", "information": f"继续履行☑ {q5_2}日内履行完毕{'付款☑ 供货☐' if q5_3=='付款' else '付款☐ 供货☑'}义务\n判令解除合同☐\n确认合同已于 年 月 日解除☐"}
        )
    elif q5_1 == "解除合同":
        q5_4 = st_date_input("解除合同日期", key="contract_termination_date")
        thisCase.reply_matters.append(
            {"type": "5. 要求继续履行或是解除合同", "information": f"继续履行☐     日内履行完毕付款☐供货☐义务\n判令解除合同☑\n确认合同已于{q5_4}解除☐"}
        )
    else:
        q5_5 = st_date_input("合同解除日期", key="contract_termination_date_confirmed")
        thisCase.reply_matters.append(
            {"type": "5. 要求继续履行或是解除合同", "information": f"继续履行☐     日内履行完毕付款☐供货☐义务\n判令解除合同☐\n确认合同已于{q5_5}解除☑"}
        )

    st.subheader("6. 是否主张担保权利")
    q6_1 = st.radio("是否主张担保权利", ["否", "是"], key="guarantee_rights", horizontal=True)
    if q6_1 == "是":
        q6_2 = st.text_area("内容", key="guarantee_details", placeholder="请输入担保权利内容")
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
    q11_0 = st.radio("填写方式",['模版填写','自定义填写'],key='q11',horizontal=True)
    if q11_0 == "模版填写":
        q11_1 = st.text_input("合同名称", key="contract_name", placeholder="请输入合同名称")
        q11_2 = st.text_input("合同编号", key="contract_number", placeholder="请输入合同编号")
        q11_3 = st_date_input("签订时间", key="contract_date")
        q11_4 = st.text_input("签订地点", key="contract_location", placeholder="请输入签订地点")
        thisCase.reasons.append(
            {"type": "1. 合同的签订情况", "information": f"合同名称：{q11_1}\n合同编号：{q11_2}\n签订时间：{q11_3}\n签订地点：{q11_4}"}
        )
    else:
        q11_t = st.text_area("签订情况", key="contract_info", placeholder="合同主体、签订时间、地点、合同名称等")
        ai_component.ai_optimize_text(q11_t,"q11_t_b")
        thisCase.reasons.append(
            {"type": "1. 合同的签订情况", "information": q11_t}
        )

    st.subheader("2. 签订主体")
    q12_1 = st.text_input("出卖人（卖方）", key="seller", placeholder="请输入出卖人（卖方）")
    q12_2 = st.text_input("买受人（买方）", key="buyer", placeholder="请输入买受人（买方）")
    thisCase.reasons.append(
        {"type": "2. 签订主体", "information": f"出卖人（卖方）：{q12_1}\n买受人（买方）：{q12_2}"}
    )

    st.subheader("3. 买卖标的物情况")
    q13_0 = st.radio("填写方式",['模版填写','自定义填写'],key='q13',horizontal=True)
    if q13_0 == "模版填写":
        q13_1 = st.text_input("标的物名称", key="item_name", placeholder="请输入标的物名称")
        q13_2 = st.text_input("规格", key="item_specification", placeholder="请输入规格")
        q13_3 = st.text_input("质量", key="item_quality", placeholder="请输入质量")
        q13_4 = st.number_input("数量", key="item_quantity", placeholder="请输入数量")
        q13_5 = st.number_input("单价", key="item_unit_price", placeholder="请输入单价")
        q13_6 = st.number_input("总价", key="item_total_price", placeholder="请输入总价")
        thisCase.reasons.append(
            {"type": "3. 买卖标的物情况", "information": f"标的物名称：{q13_1}\n规格：{q13_2}\n质量：{q13_3}\n数量：{q13_4}\n单价：{q13_5}元；总价：{q13_6}元"}
        )
    else:
        q13_t = st.text_area("标的物情况", key="item_info", placeholder="标的物名称、规格、质量、数量、单价、总价等")
        ai_component.ai_optimize_text(q13_t,"q13_t_b")
        thisCase.reasons.append(
            {"type": "3. 买卖标的物情况", "information": q13_t}
        )

    st.subheader("4. 合同约定的价格及支付方式")
    q14_1 = st.number_input("单价", key="price", placeholder="请输入合同约定的单价")
    q14_2 = st.number_input("总价", key="total_price", placeholder="请输入合同约定的总价")
    q14_3 = st.radio("支付方式", ["现金", "转账", "票据", "其他"], key="payment_method", horizontal=True)
    if q14_3 == "票据":
        q14_3_t = st.text_input("票据类型", key="bill_type", placeholder="请输入票据类型")
    if q14_3 == "其他":
        q14_3_o = st.text_input("其他支付方式", key="other_payment_method", placeholder="请输入其他支付方式")
    q14_4 = st.radio("支付方式", ["一次性", "分期"], key="payment_type", horizontal=True)
    if q14_4 == "分期":
        q14_4_2 = st.text_input("分期方式", key="installment_method", placeholder="请输入分期方式")
    
    q14_t_1 = ''
    for i in ["现金", "转账", "票据", "其他"]:
        if i == q14_3:
            q14_t_1 += f"{i}☑"
            if i == "票据":
                q14_t_1 += f"{q14_3_t}"
            elif i == "其他":
                q14_t_1 += f"其他：{q14_3_o}\n"
        else:
            q14_t_1 += f"{i}☐"
    
    thisCase.reasons.append(
        {"type": "4. 合同约定的价格及支付方式", "information": f"单价：{q14_1} 总价：{q14_2}\n以{q14_t_1}方式\n{'一次性☑ 分期☐ 支付' if q14_4 == '一次性' else '一次性☐ 分期☐ 支付'}\n分期方式：{q14_4_2 if q14_4 == '分期' else ''}"}
    )

    st.subheader("5. 合同约定的交货时间、地点、方式、风险承担、安装、调试、验收")
    q15_1 = st.text_area("交货时间、地点、方式、风险承担、安装、调试、验收", key="delivery_details", placeholder="请输入交货时间、地点、方式、风险承担、安装、调试、验收")
    ai_component.ai_optimize_text(q15_1,"q15_1_b")
    thisCase.reasons.append(
        {"type": "5. 合同约定的交货时间、地点、方式、风险承担、安装、调试、验收", "information": q15_1}
    )

    st.subheader("6. 合同约定的质量标准及检验方式、质量异议期限")
    q16_1 = st.text_area("质量标准及检验方式、质量异议期限", key="quality_standards", placeholder="请输入质量标准及检验方式、质量异议期限")
    ai_component.ai_optimize_text(q16_1,"q16_1_b")
    thisCase.reasons.append(
        {"type": "6. 合同约定的质量标准及检验方式、质量异议期限", "information": q16_1}
    )

    st.subheader("7. 合同约定的违约金（定金）")
    q17_1 = st.number_input("违约金", key="penalty_amount_reason", placeholder="请输入违约金")
    q17_2 = st.text_input("合同条款", key="penalty_clause", placeholder="请输入合同条款")
    q17_3 = st.number_input("定金", key="deposit_amount", placeholder="请输入定金")
    q17_4 = st.text_input("合同条款", key="deposit_clause", placeholder="请输入合同条款")
    q17_5 = st.number_input("迟延履行违约金", key="late_penalty_amount", placeholder="请输入迟延履行违约金")
    q17_6 = st.text_input("合同条款", key="late_penalty_clause", placeholder="请输入合同条款")
    thisCase.reasons.append(
        {
            "type": "7. 合同约定的违约金（定金）",
            "information": (
                f"违约金{'☑：' + str(q17_1) if q17_1 != 0 else '☐：'}元（合同条款：{q17_2}）；\n"
                f"定金{'☑：' + str(q17_3) if q17_3 != 0 else '☐：'}元（合同条款：{q17_4}）；\n"
                f"迟延履行违约金{'☑：' + str(q17_5) if q17_5 != 0 else '☐：'}元/日（合同条款：{q17_6}）"
            )
        }
    )

    st.subheader("8. 价款支付及标的物交付情况")
    q18_1 = st.number_input("按期支付价款", key="paid_on_time", placeholder="请输入按期支付价款（金额）")
    q18_2 = st.number_input("逾期付款", key="overdue_payment", placeholder="请输入逾期付款（金额）")
    q18_3 = st.number_input("逾期未付款", key="unpaid_amount", placeholder="请输入逾期未付款（金额）")
    q18_4 = st.number_input("按期交付标的物", key="delivered_on_time", placeholder="请输入按期交付标的物(件数)")
    q18_5 = st.number_input("逾期交付", key="overdue_delivery", placeholder="请输入逾期交付(件数)")
    q18_6 = st.number_input("逾期未交付", key="undelivered_amount", placeholder="请输入逾期未交付(件数)")
    thisCase.reasons.append(
        {"type": "8. 价款支付及标的物交付情况", "information": f"按期支付价款：{q18_1}元，逾期付款：{q18_2}元，逾期未付款：{q18_3}元；\n按期交付标的物：{q18_4}件，逾期交付：{q18_5}件，逾期未交付：{q18_6}件"}
    )

    st.subheader("9. 是否存在迟延履行")
    q19_1 = st.radio("是否存在迟延履行", ["否", "是"], key="late_performance", horizontal=True)
    if q19_1 == "是":
        q19_2 = st.text_input("迟延时间", key="late_performance_time", placeholder="请输入迟延时间")
        q19_3 = st.radio("迟延类型", ["逾期付款", "逾期交货"], key="late_performance_type", horizontal=True)
        thisCase.reasons.append(
            {"type": "9. 是否存在迟延履行", "information": f"是☑ 迟延时间：{q19_2}；迟延类型：{"逾期付款☑ 逾期交货☐" if q19_3 == '逾期付款' else '逾期付款☐ 逾期交货☑'}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "9. 是否存在迟延履行", "information": "是☐ 迟延时间：逾期付款☐ 逾期交货☐\n否☑"}
        )

    st.subheader("10. 是否催促过履行")
    q20_1 = st.radio("是否催促过履行", ["否", "是"], key="urged_performance", horizontal=True)
    if q20_1 == "是":
        q20_2 = st_date_input("催促日期", key="urged_date")
        q20_3 = st.text_input("催促方式", key="urged_method", placeholder="请输入催促方式")
        thisCase.reasons.append(
            {"type": "10. 是否催促过履行", "information": f"是☑ 催促情况：于{q20_2}通过{q20_3}方式催促\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "10. 是否催促过履行", "information": "是☐ 催促情况：于 年 月 日通过 方式催促\n否☑"}
        )

    st.subheader("11. 买卖合同标的物有无质量争议")
    q21_1 = st.radio("买卖合同标的物有无质量争议", ["无", "有"], key="quality_dispute", horizontal=True)
    if q21_1 == "有":
        q21_2 = st.text_area("具体情况", key="quality_dispute_details", placeholder="请输入具体情况")
        ai_component.ai_optimize_text(q21_2,"q21_2_b")
        thisCase.reasons.append(
            {"type": "11. 买卖合同标的物有无质量争议", "information": f"有☑ 具体情况：{q21_2}\n无☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "11. 买卖合同标的物有无质量争议", "information": "有☐ 具体情况：\n无☑"}
        )

    st.subheader("12. 标的物质量规格或履行方式是否存在不符合约定的情况")
    q22_1 = st.radio("标的物质量规格或履行方式是否存在不符合约定的情况", ["否", "是"], key="non_conformance", horizontal=True)
    if q22_1 == "是":
        q22_2 = st.text_area("具体情况", key="non_conformance_details", placeholder="请输入具体情况")
        ai_component.ai_optimize_text(q22_2,"q22_2_b")
        thisCase.reasons.append(
            {"type": "12. 标的物质量规格或履行方式是否存在不符合约定的情况", "information": f"是☑ 具体情况：{q22_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "12. 标的物质量规格或履行方式是否存在不符合约定的情况", "information": "是☐ 具体情况：\n否☑"}
        )

    st.subheader("13. 是否曾就标的物质量问题进行协商")
    q23_1 = st.radio("是否曾就标的物质量问题进行协商", ["否", "是"], key="quality_negotiation", horizontal=True)
    if q23_1 == "是":
        q23_2 = st.text_area("具体情况", key="quality_negotiation_details", placeholder="请输入具体情况")
        ai_component.ai_optimize_text(q23_2,"q23_2_b")
        thisCase.reasons.append(
            {"type": "13. 是否曾就标的物质量问题进行协商", "information": f"是☑ 具体情况：{q23_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "13. 是否曾就标的物质量问题进行协商", "information": "是☐ 具体情况：\n否☑"}
        )

    st.subheader("14. 被告应当支付的利息、违约金、赔偿金")
    q24_1 = st.number_input("利息", key="interest_amount_reason", placeholder="请输入利息")
    q24_2 = st.number_input("违约金", key="penalty_amount_reason_2", placeholder="请输入违约金")
    q24_3 = st.number_input("赔偿金", key="compensation_amount_reason", placeholder="请输入赔偿金")
    q24_4 = st.number_input("总计",key='total_amount_reason', placeholder="请输入总金额")
    q24_5 = st.text_area("计算方式", key="calculation_method", placeholder="请输入计算方式")
    thisCase.reasons.append(
        {
            "type": "14. 被告应当支付的利息、违约金、赔偿金",
            "information": (
                f"利息{'☑：' + str(q24_1) if q24_1 != 0 else '☐：'}元；\n"
                f"违约金{'☑：' + str(q24_2) if q24_2 != 0 else '☐：'}元；\n"
                f"赔偿金{'☑：' + str(q24_3) if q24_3 != 0 else '☐：'}元；\n"
                f"总计{str(q24_4)}；\n"
                f"计算方式：{q24_5}"
            )
        }
    )

    st.subheader("15. 是否签订物的担保（抵押、质押）合同")
    q25_1 = st.radio("是否签订物的担保（抵押、质押）合同", ["否", "是"], key="collateral_contract", horizontal=True)
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
    q27_1 = st.radio("是否最高额担保（抵押、质押）", ["否", "是"], key="maximum_guarantee", horizontal=True)
    if q27_1 == "是":
        q27_2 = st_date_input("担保债权的确定时间", key="guarantee_determination_date")
        q27_3 = st.number_input("担保额度", key="guarantee_amount", placeholder="请输入担保额度")
        thisCase.reasons.append(
            {"type": "17. 是否最高额担保（抵押、质押）", "information": f"是☑ 担保债权的确定时间：{q27_2} 担保额度：{q27_3}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "17. 是否最高额担保（抵押、质押）", "information": "是☐ 担保债权的确定时间： 担保额度：\n否☑"}
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
            {"type": "19. 是否签订保证合同", "information": "是☐ 签订时间： 保证人： 主要内容：\n否☑"}
        )

    st.subheader("20. 保证方式")
    q30_1 = st.radio("保证方式", ["无","一般保证", "连带责任保证"], key="guarantee_type", horizontal=True)
    if q30_1 == "无":
        thisCase.reasons.append(
            {"type": "20. 保证方式", "information": "保证方式：一般保证☐\n连带责任保证☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "20. 保证方式", "information": f"保证方式：{'一般保证☑ 连带责任保证☐' if q30_1 == '一般保证' else '一般保证☐ 连带责任保证☑'}"}
        )

    st.subheader("21. 其他担保方式")
    q31_1 = st.radio("是否存在其他担保方式", ["否", "是"], key="other_guarantee", horizontal=True)
    if q31_1 == "是":
        q31_2 = st.text_input("担保形式", key="other_guarantee_form", placeholder="请输入担保形式")
        thisCase.reasons.append(
            {"type": "21. 其他担保方式", "information": f"是☑ 担保形式：{q31_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "21. 其他担保方式", "information": "是☐ 担保形式：\n否☑"}
        )
    
    st.subheader("22. 其他需要说明的内容（可另附页）")
    q32 = st.text_area("其他内容", key="other_guarantee_content")
    ai_component.ai_optimize_text(q32,"q32_b")
    thisCase.reasons.append(
        {"type": "22. 其他需要说明的内容（可另附页）", "information": f"{q32}"}
    )

    st.subheader("23.证据清单（可另附页）")
    q33 = st.text_area("证据清单（可另附页）", key="evidence_list")
    thisCase.reasons.append(
        {"type": "23.证据清单（可另附页）", "information": f"{q33}"}
    )

# 定义数据格式化器
class SalesContractCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(thisCase):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(thisCase.to_json())
        template_data = super(SalesContractCaseFormatter,
                              SalesContractCaseFormatter).format_case(thisCase)

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
                SalesContractCaseFormatter,
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