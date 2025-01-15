import streamlit as st
from page.components.complaint import Plaintiff
from page.components.jurisdiction_and_preservation import JurisdictionAndPreservation
from page.components.header import header
from page.components.section import create_text_section, create_radio_section, CommonCasePlaintiff
from page.components.complaint import Defendant, Plaintiff, ThirdParty
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import json
from utils.tools import st_date_input

# 定义案件类型
CASE_TYPE = "民间借贷纠纷"

# 定义诉讼请求和依据的问题
REPLY_QUESTIONS = [
    "本金",
    "利息",
    "是否要求提前还款或解除合同",
    "是否主张担保权利",
    "是否主张实现债权的费用",
    "其他请求",
    "标的总额",
    "请求依据"
]

# 定义事实和理由的问题
REASON_QUESTIONS = [
    "合同签订情况",
    "签订主体",
    "借款金额",
    "借款期限",
    "借款利率",
    "借款提供时间",
    "还款方式",
    "还款情况",
    "是否存在逾期还款",
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
    st.subheader("1. 本金")
    q1_1 = st_date_input("截至日期", key="principal_due_date")
    q1_2 = st.number_input(
        "尚欠本金金额", key="principal_amount", placeholder="请输入尚欠本金金额")
    q1_3 = st.radio("是否为外币", ["否", "是"],
                    key="principal_currency", horizontal=True)
    if q1_3 == "是":
        q1_4 = st.text_input(
            "外币币种", key="principal_currency_type", placeholder="请输入外币币种")
    thisCase.reply_matters.append(
        {"type": "1. 本金", "information": f"截至{q1_1}止，尚欠本金{
            q1_2}元（{q1_4 if q1_3 == '是' else '人民币'}）；"}
    )

    st.subheader("2. 利息")
    q2_1 = st_date_input("截至日期", key="interest_due_date")
    q2_2 = st.number_input(
        "欠利息金额", key="interest_amount", placeholder="请输入欠利息金额")
    q2_3 = st.text_area("计算方式", key="interest_calculation",
                        placeholder="请输入计算方式")
    q2_4 = st.radio("是否请求支付至实际清偿之日止", [
                    "是", "否"], key="interest_until_payment", horizontal=True)
    thisCase.reply_matters.append(
        {"type": "2. 利息", "information": f"截至{q2_1}止，欠利息{q2_2}元；计算方式：{
            q2_3}；\n是否请求支付至实际清偿之日止：{'是☑ 否☐' if q2_4 == '是' else '是☐ 否☑'}"}
    )

    st.subheader("3. 是否要求提前还款或解除合同")
    q3_1 = st.radio("是否要求提前还款或解除合同", ["否", "是"],
                    key="early_repayment", horizontal=True)
    if q3_1 == "是":
        q3_2 = st.radio("方式", ["提前还款（加速到期）", "解除合同"],
                        key="early_repayment_type")
        thisCase.reply_matters.append(
            {"type": "3. 是否要求提前还款或解除合同", "information": f"是☑ {
                '提前还款（加速到期）☑/解除合同☐' if q3_2 == '提前还款（加速到期）' else '提前还款（加速到期）☐/解除合同☑'}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "3. 是否要求提前还款或解除合同", "information": "是☐ 提前还款（加速到期）☐/解除合同☐\n否☑"}
        )

    st.subheader("4. 是否主张担保权利")
    q4_1 = st.radio("是否主张担保权利", ["否", "是"],
                    key="guarantee_rights", horizontal=True)
    if q4_1 == "是":
        q4_2 = st.text_area("内容", key="guarantee_details",
                            placeholder="请输入担保权利内容")
        thisCase.reply_matters.append(
            {"type": "4. 是否主张担保权利", "information": f"是☑ 内容：{q4_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "4. 是否主张担保权利", "information": "是☐ 内容：\n否☑"}
        )

    st.subheader("5. 是否主张实现债权的费用")
    q5_1 = st.radio("是否主张实现债权的费用", ["否", "是"],
                    key="legal_fees", horizontal=True)
    if q5_1 == "是":
        q5_2 = st.text_area("明细", key="legal_fees_details",
                            placeholder="请输入费用明细")
        thisCase.reply_matters.append(
            {"type": "5. 是否主张实现债权的费用", "information": f"是☑ 明细：{q5_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "5. 是否主张实现债权的费用", "information": "是☐ 明细：\n否☑"}
        )

    st.subheader("6. 其他请求")
    q6_1 = st.text_area("其他请求", key="other_requests", placeholder="请输入其他请求")
    thisCase.reply_matters.append(
        {"type": "6. 其他请求", "information": q6_1}
    )

    st.subheader("7. 标的总额")
    q7_1 = st.text_area("标的总额", key="total_amount", placeholder="请输入标的总额")
    thisCase.reply_matters.append(
        {"type": "7. 标的总额", "information": q7_1}
    )

    st.subheader("8. 请求依据")
    q8_1 = st.text_area("合同约定", key="contract_terms", placeholder="请输入合同约定")
    q8_2 = st.text_area("法律规定", key="legal_provisions", placeholder="请输入法律规定")
    thisCase.reply_matters.append(
        {"type": "8. 请求依据", "information": f"合同约定：{q8_1}\n法律规定：{q8_2}"}
    )

# 定义事实和理由部分


def fact(thisCase):
    st.subheader("1. 合同签订情况")
    q9_0 = st.radio("填写方式", ["模版填写", "自定义填写"], key='q9', horizontal=True)
    if q9_0 == "模版填写":
        q9_1 = st.text_input("合同名称", key="contract_name",
                             placeholder="请输入合同名称")
        q9_2 = st.text_input("合同编号", key="contract_number",
                             placeholder="请输入合同编号")
        q9_3 = st_date_input("签订时间", key="contract_date")
        q9_4 = st.text_input(
            "签订地点", key="contract_location", placeholder="请输入签订地点")
        thisCase.reasons.append(
            {"type": "1. 合同签订情况", "information": f"合同名称：{
                q9_1}\n合同编号：{q9_2}\n签订时间：{q9_3}\n签订地点：{q9_4}"}
        )
    else:
        q9_t = st.text_area("签订情况", key="contract_details",
                            placeholder="名称、编号、签订时间、地点等")
        thisCase.reasons.append(
            {"type": "1. 合同签订情况", "information": q9_t}
        )

    st.subheader("2. 签订主体")
    q10_1 = st.text_input("贷款人", key="lender", placeholder="请输入贷款人")
    q10_2 = st.text_input("借款人", key="borrower", placeholder="请输入借款人")
    thisCase.reasons.append(
        {"type": "2. 签订主体", "information": f"贷款人：{q10_1}\n借款人：{q10_2}"}
    )

    st.subheader("3. 借款金额")
    q11_1 = st.number_input(
        "约定借款金额", key="agreed_amount", placeholder="请输入约定借款金额")
    q11_2 = st.number_input(
        "实际提供金额", key="actual_amount", placeholder="请输入实际提供金额")
    thisCase.reasons.append(
        {"type": "3. 借款金额", "information": f"约定借款金额：{q11_1}元\n实际提供金额：{q11_2}元"}
    )

    st.subheader("4. 借款期限")
    q12_1 = st.radio("是否到期", ["是", "否"], key="loan_due", horizontal=True)
    q12_2 = st_date_input("约定期限开始日期", key="loan_start_date")
    q12_3 = st_date_input("约定期限结束日期", key="loan_end_date")
    thisCase.reasons.append(
        {"type": "4. 借款期限", "information": f"是否到期：{
            '是☑ 否☐' if q12_1 == '是' else '是☐ 否☑'}\n约定期限：{q12_2}至{q12_3}"}
    )

    st.subheader("5. 借款利率")
    q13_1 = st.number_input(
        "利率（%/年）", key="interest_rate", placeholder="请输入利率")
    q13_2 = st.text_input(
        "合同条款", key="interest_rate_clause", placeholder="请输入合同条款")
    thisCase.reasons.append(
        {"type": "5. 借款利率", "information": f"利率{
            '☑：' + str(q13_1) if q13_1 != 0 else '☐：'}%/年（合同条款：{q13_2}）"}
    )

    st.subheader("6. 借款提供时间")
    q14_1 = st_date_input("提供时间", key="loan_disbursement_date")
    q14_2 = st.number_input(
        "提供金额", key="disbursement_amount", placeholder="请输入提供金额")
    thisCase.reasons.append(
        {"type": "6. 借款提供时间", "information": f"{q14_1}，提供{q14_2}元"}
    )

    st.subheader("7. 还款方式")
    q15_list = ["等额本息", "等额本金", "到期一次性还本付息", "按月计息、到期一次性还本",
        "按季计息、到期一次性还本", "按年计息、到期一次性还本", "其他"]
    q15_1 = st.radio("还款方式", q15_list, key="repayment_method", horizontal=True)
    if q15_1 == '其他':
        q15_2 = st.text_input(
            "其他还款方式", key="other_repayment_method", placeholder="请输入其他还款方式")
    q15_r = ''
    for i in q15_list[:-1]:
        if q15_1 == i:
            q15_r += f'{i}☑\n'
        else:
            q15_r += f'{i}☐\n'
    q15_r += f'{"其他☑：" + q15_2 if q15_1 == '其他' else '其他☐'}'
    thisCase.reasons.append(
        {"type": "7. 还款方式", "information": f"{q15_r}"}
    )

    st.subheader("8. 还款情况")
    q16_1 = st.number_input(
        "已还本金", key="repaid_principal", placeholder="请输入已还本金")
    q16_2 = st.number_input(
        "已还利息", key="repaid_interest", placeholder="请输入已还利息")
    q16_3 = st_date_input("还息至日期", key="interest_paid_until")
    thisCase.reasons.append(
        {"type": "8. 还款情况", "information": f"已还本金：{
            q16_1}元\n已还利息：{q16_2}元，还息至{q16_3}"}
    )

    st.subheader("9. 是否存在逾期还款")
    q17_1 = st.radio("是否存在逾期还款", ["否", "是"],
                     key="overdue_repayment", horizontal=True)
    if q17_1 == "是":
        q17_2 = st_date_input("逾期开始时间", key="overdue_date")
        thisCase.reasons.append(
            {"type": "9. 是否存在逾期还款", "information": f"是☑ 逾期时间：{q17_2}至今已逾期\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "9. 是否存在逾期还款", "information": f"是☐ 逾期时间：\n否☑"}
        )

    st.subheader("10. 是否签订物的担保（抵押、质押）合同")
    q18_1 = st.radio("是否签订物的担保合同", ["否", "是"],
                     key="collateral_contract", horizontal=True)
    if q18_1 == "是":
        q18_2 = st_date_input("签订时间", key="collateral_contract_date")
        thisCase.reasons.append(
            {"type": "10. 是否签订物的担保（抵押、质押）合同", "information": f"是☑ 签订时间：{q18_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "10. 是否签订物的担保（抵押、质押）合同", "information": f"是☐ 签订时间：\n否☑"}
        )

    st.subheader("11. 担保人、担保物")
    q19_1 = st.text_input("担保人", key="guarantor", placeholder="请输入担保人")
    q19_2 = st.text_input("担保物", key="collateral", placeholder="请输入担保物")
    thisCase.reasons.append(
        {"type": "11. 担保人、担保物", "information": f"担保人：{q19_1}\n担保物：{q19_2}"}
    )

    st.subheader("12. 是否最高额担保（抵押、质押）")
    q20_1 = st.radio("是否最高额担保", ["否", "是"],
                     key="maximum_guarantee", horizontal=True)
    if q20_1 == "是":
        q20_2 = st_date_input("担保债权的确定时间", key="guarantee_determination_date")
        q20_3 = st.number_input(
            "担保额度", key="guarantee_amount", placeholder="请输入担保额度")
        thisCase.reasons.append(
            {"type": "12. 是否最高额担保（抵押、质押）", "information": f"是☑ 担保债权的确定时间：{
                q20_2}\n担保额度：{q20_3}元\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "12. 是否最高额担保（抵押、质押）", "information": f"是☐ 担保债权的确定时间：\n担保额度：\n否☑"}
        )

    st.subheader("13. 是否办理抵押、质押登记")
    q21_1 = st.radio(
        "是否办理抵押、质押登记", ["否", "是"], key="collateral_registration", horizontal=True)
    if q21_1 == "是":
        q21_2 = st.radio("登记类型", ["正式登记", "预告登记"],
                         key="registration_type", horizontal=True)
        thisCase.reasons.append(
            {"type": "13. 是否办理抵押、质押登记", "information": f"是☑ 登记类型：{
                '正式登记☑ 预告登记☐' if q21_2 == '正式登记' else '正式登记☐ 预告登记☑'}"}
        )
    else:
        thisCase.reasons.append(
            {"type": "13. 是否办理抵押、质押登记", "information": f"是☐ 登记类型：正式登记☐ 预告登记☐\n否☑"}
        )

    st.subheader("14. 是否签订保证合同")
    q22_1 = st.radio("是否签订保证合同", ["否", "是"],
                     key="guarantee_contract", horizontal=True)
    if q22_1 == "是":
        q22_2 = st_date_input("签订时间", key="guarantee_contract_date")
        q22_3 = st.text_input(
            "保证人", key="guarantee_person", placeholder="请输入保证人")
        q22_4 = st.text_area(
            "主要内容", key="guarantee_content", placeholder="请输入主要内容")
        thisCase.reasons.append(
            {"type": "14. 是否签订保证合同", "information": f"是☑ 签订时间：{
                q22_2}\n保证人：{q22_3}\n主要内容：{q22_4}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "14. 是否签订保证合同", "information": f"是☐ 签订时间：\n保证人：\n主要内容：\n否☑"}
        )

    st.subheader("15. 保证方式")
    q23_1 = st.radio("保证方式", ["无", "一般保证", "连带责任保证"],
                     key="guarantee_type", horizontal=True)
    if q23_1 == '无':
        thisCase.reasons.append(
        {"type": "15. 保证方式", "information": f"保证方式：一般保证☐\n连带责任保证☐"}
    )
    else:
        thisCase.reasons.append(
        {"type": "15. 保证方式", "information": f"保证方式：{'一般保证☑\n连带责任保证☐' if q23_1 == '一般保证' else '一般保证☐\n连带责任保证☑'}"}
    )

    st.subheader("16. 其他担保方式")
    q24_1 = st.radio("是否存在其他担保方式", ["否", "是"], key="other_guarantee", horizontal=True)
    if q24_1 == "是":
        q24_2 = st.text_input("担保形式", key="other_guarantee_form", placeholder="请输入担保形式")
        q24_3 = st_date_input("签订时间", key="other_guarantee_date")
        thisCase.reasons.append(
            {"type": "16. 其他担保方式", "information": f"是☑ 担保形式：{q24_2}；签订时间：{q24_3}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "16. 其他担保方式", "information": f"是☐ 担保形式：\n签订时间：\n否☑"}
        )

    st.subheader("17. 其他需要说明的内容（可另附页）")
    q25_1 = st.text_area("其他需要说明的内容", key="other_information", placeholder="请输入其他需要说明的内容")
    thisCase.reasons.append(
        {"type": "17. 其他需要说明的内容（可另附页）", "information": q25_1}
    )

    st.subheader("18.证据清单（可另附页）")
    q26_1 = st.text_area("证据清单",key="list", placeholder="证据清单，可另附页")
    thisCase.reasons.append({
        "type": "18.证据清单（可另附页）", "information": q26_1
    })

# 定义数据格式化器
class PrivateLendingCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(thisCase):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(thisCase.to_json())
        template_data = super(PrivateLendingCaseFormatter,
                              PrivateLendingCaseFormatter).format_case(thisCase)

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
                PrivateLendingCaseFormatter,
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