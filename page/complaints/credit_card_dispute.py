import streamlit as st
from page.components.complaint import Plaintiff
from page.components.ai_ui import AIComponent
from page.components.header import header
from page.components.section import CommonCasePlaintiff
from page.components.complaint import Defendant, Plaintiff, ThirdParty
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import json
from utils.tools import st_date_input


# 定义案件类型
CASE_TYPE = "银行信用卡纠纷"

ai_component = AIComponent(CASE_TYPE)

# 定义诉讼请求和依据的问题
REPLY_QUESTIONS = [
    "透文本金",
    "利息、罚息、复利、滞纳金、违约金、手续费等",
    "是否主张担保权利",
    "是否主张实现债权的费用",
    "其他请求",
    "标的总额",
    "请求依据"
]

# 定义事实和理由的问题
REASON_QUESTIONS = [
    "信用卡办理情况",
    "信用卡合约的主要约定",
    "是否对被告就信用卡合约主要条款进行提示注意、说明",
    "被告已还款金额",
    "被告逾期未还款金额",
    "是否向被告进行通知和催收",
    "是否签订物的担保（抵押、质押）合同",
    "担保人、担保物",
    "是否最高额担保（抵押、质押）",
    "是否办理抵押、质押登记",
    "是否签订保证合同",
    "保证方式",
    "其他担保方式",
    "其他需要说明的内容",
    "证据清单"
]

# 初始化案件对象
thisCase = CommonCasePlaintiff()

# 定义诉讼请求和依据部分


def claim(thisCase):
    st.subheader("1. 透文本金")
    q1_1 = st_date_input("截至日期", key="principal_due_date")
    q1_2 = st.number_input("尚欠本金金额", key="principal_amount",
                           placeholder="请输入尚欠本金金额", min_value=0.0, step=0.01, format="%.2f")
    q1_3 = st.radio("是否为外币", ["否", "是"],
                    key="principal_currency", horizontal=True)
    q1_4 = ''
    if q1_3 == "是":
        q1_4 = st.text_input(
            "外币币种", key="principal_currency_type", placeholder="请输入外币币种")
    thisCase.reply_matters.append(
        {"type": "1. 透文本金", "information": f"截至{q1_1}止，尚欠本金{
            q1_2:.2f}元（{'人民币，下同；如为外币需特别注明' if not q1_3 else q1_4})"}
    )

    st.subheader("2. 利息、罚息、复利、滞纳金、违约金、手续费等")
    q2_1 = st_date_input("截至日期", key="interest_due_date")
    q2_2 = st.number_input("欠利息、罚息、复利、滞纳金、违约金、手续费等金额", key="interest_amount",
                           placeholder="请输入欠利息、罚息、复利、滞纳金、违约金、手续费等金额", min_value=0.0, step=0.01, format="%.2f")
    q2_3 = st.text_area("明细", key="interest_details", placeholder="请输入明细")
    thisCase.reply_matters.append(
        {"type": "2. 利息、罚息、复利、滞纳金、违约金、手续费等", "information": f"截至{q2_1}止，欠利息、罚息、复利、滞纳金、违约金、手续费等共计{
            q2_2:.2f}元；\n自{q2_1}之后的利息、罚息、复利、滞纳金、违约金以及手续费等各项费用按照信用卡领用协议计算至实际清偿之日止\n明细：{q2_3}"}
    )

    st.subheader("3. 是否主张担保权利")
    q3_1 = st.radio("是否主张担保权利", ["否", "是"],
                    key="guarantee_rights", horizontal=True)
    if q3_1 == "是":
        q3_2 = st.text_area("内容", key="guarantee_details",
                            placeholder="请输入担保权利内容")
        thisCase.reply_matters.append(
            {"type": "3. 是否主张担保权利", "information": f"是☑ 内容：{q3_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "3. 是否主张担保权利", "information": "是☐ 内容：\n否☑"}
        )

    st.subheader("4. 是否主张实现债权的费用")
    q4_1 = st.radio("是否主张实现债权的费用", ["否", "是"],
                    key="legal_fees", horizontal=True)
    if q4_1 == "是":
        q4_2 = st.text_area("费用明细", key="legal_fees_details",
                            placeholder="请输入费用明细")
        thisCase.reply_matters.append(
            {"type": "4. 是否主张实现债权的费用", "information": f"是☑ 费用明细：{q4_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "4. 是否主张实现债权的费用", "information": "是☐ 费用明细：\n否☑"}
        )

    st.subheader("5. 其他请求")
    q5_1 = st.text_area("其他请求", key="other_requests", placeholder="请输入其他请求")
    ai_component.ai_optimize_text(q5_1, "q5_1_b")
    thisCase.reply_matters.append(
        {"type": "5. 其他请求", "information": q5_1}
    )

    st.subheader("6. 标的总额")
    q6_1 = st.text_area("标的总额", key="total_amount", placeholder="请输入标的总额")
    thisCase.reply_matters.append(
        {"type": "6. 标的总额", "information": q6_1}
    )

    st.subheader("7. 请求依据")
    q7_1 = st.text_area("合同约定", key="contract_terms", placeholder="请输入合同约定")
    q7_2 = st.text_area("法律规定", key="legal_provisions", placeholder="请输入法律规定")
    thisCase.reply_matters.append(
        {"type": "7. 请求依据", "information": f"合同约定：{q7_1}\n法律规定：{q7_2}"}
    )

# 定义事实和理由部分


def fact(thisCase):
    st.subheader("1. 信用卡办理情况")
    q8_0 = st.radio("填写方式", ['模版填写', '自定义填写'], key='q8', horizontal=True)
    if q8_0 == "模版填写":
        q8_1 = st.text_input(
            "信用卡卡号", key="credit_card_number", placeholder="请输入信用卡卡号")
        q8_2 = st.text_input("信用卡登记权利人", key="card_holder",
                             placeholder="请输入信用卡登记权利人")
        q8_3 = st_date_input("办卡时间", key="card_issue_date")
        q8_4 = st.text_input("办卡行", key="issuing_bank", placeholder="请输入办卡行")
        thisCase.reasons.append(
            {"type": "1. 信用卡办理情况", "information": f"信用卡卡号：{
                q8_1}\n信用卡登记权利人：{q8_2}\n办卡时间：{q8_3}\n办卡行：{q8_4}"}
        )
    else:
        q8_t = st.text_input("请输入办理情况", key="q8_t",
                             placeholder="信用卡卡号、信用卡登记权利人、办卡时间、办卡行等")
        ai_component.ai_optimize_text(q8_t, "q8_t_b")
        thisCase.reasons.append(
            {"type": "1. 信用卡办理情况", "information": q8_t}
        )

    st.subheader("2. 信用卡合约的主要约定")
    q9_1 = st.number_input("透支金额", key="overdraft_amount",
                           placeholder="请输入透支金额", min_value=0.0, step=0.01, format="%.2f")
    q9_2 = st.text_area("利息、罚息、复利、滞纳金、违约金、手续费等的计算标准", key="interest_calculation",
                        placeholder="请输入利息、罚息、复利、滞纳金、违约金、手续费等的计算标准")
    q9_3 = st.text_area("违约责任", key="breach_terms", placeholder="请输入违约责任")
    q9_4 = st.text_area("解除条件", key="termination_conditions",
                        placeholder="请输入解除条件")
    thisCase.reasons.append(
        {"type": "2. 信用卡合约的主要约定", "information": f"透支金额：{
            q9_1:.2f}元\n利息、罚息、复利、滞纳金、违约金、手续费等的计算标准：{q9_2}\n违约责任：{q9_3}\n解除条件：{q9_4}"}
    )

    st.subheader("3. 是否对被告就信用卡合约主要条款进行提示注意、说明")
    q10_1 = st.radio("是否对被告进行提示说明", ["否", "是"],
                     key="notice_provided", horizontal=True)
    if q10_1 == "是":
        q10_2 = st.text_area(
            "提示说明的具体方式以及时间地点", key="notice_details", placeholder="请输入提示说明的具体方式以及时间地点")
        thisCase.reasons.append(
            {"type": "3. 是否对被告就信用卡合约主要条款进行提示注意、说明",
                "information": f"是☑ 提示说明的具体方式以及时间地点：{q10_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "3. 是否对被告就信用卡合约主要条款进行提示注意、说明",
                "information": "是☐ 提示说明的具体方式以及时间地点：\n否☑"}
        )

    st.subheader("4. 被告已还款金额")
    q11_1 = st.number_input("已还款金额", key="repaid_amount",
                            placeholder="请输入已还款金额", min_value=0.0, step=0.01, format="%.2f")
    thisCase.reasons.append(
        {"type": "4. 被告已还款金额", "information": f"已还款金额：{q11_1:.2f}元"}
    )

    st.subheader("5. 被告逾期未还款金额")
    q12_0 = st_date_input("逾期时间", key="overdue_start_date")
    q12_1 = st_date_input("截至日期", key="overdue_end_date")
    q12_2 = st.number_input("欠付信用卡本金", key="unpaid_principal",
                            placeholder="请输入欠付信用卡本金", min_value=0.0, step=0.01, format="%.2f")
    q12_3 = st.number_input("利息", key="unpaid_interest",
                            placeholder="请输入利息", min_value=0.0, step=0.01, format="%.2f")
    q12_4 = st.number_input("罚息", key="unpaid_penalty",
                            placeholder="请输入罚息", min_value=0.0, step=0.01, format="%.2f")
    q12_5 = st.number_input("复利", key="unpaid_compound_interest",
                            placeholder="请输入复利", min_value=0.0, step=0.01, format="%.2f")
    q12_6 = st.number_input("滞纳金", key="unpaid_late_fee",
                            placeholder="请输入滞纳金", min_value=0.0, step=0.01, format="%.2f")
    q12_7 = st.number_input("违约金", key="unpaid_penalty_fee",
                            placeholder="请输入违约金", min_value=0.0, step=0.01, format="%.2f")
    q12_8 = st.number_input("手续费", key="unpaid_service_fee",
                            placeholder="请输入手续费", min_value=0.0, step=0.01, format="%.2f")
    thisCase.reasons.append(
        {"type": "5. 被告逾期未还款金额", "information": f"逾期时间：{q12_0}\n截至{q12_1}，被告欠付信用卡本金：{q12_2:.2f}元、利息：{
            q12_3:.2f}元、罚息：{q12_4:.2f}元、复利：{q12_5:.2f}元、滞纳金：{q12_6:.2f}元、违约金：{q12_7:.2f}元、手续费：{q12_8:.2f}元"}
    )

    st.subheader("6. 是否向被告进行通知和催收")
    q13_1 = st.radio("是否向被告进行通知和催收", ["否", "是"],
                     key="collection_notice", horizontal=True)
    if q13_1 == "是":
        q13_2 = st.text_area(
            "具体情况", key="collection_details", placeholder="请输入具体情况")
        ai_component.ai_optimize_text(q13_2, "q13_2_b")
        thisCase.reasons.append(
            {"type": "6. 是否向被告进行通知和催收", "information": f"是☑ 具体情况：{q13_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "6. 是否向被告进行通知和催收", "information": "是☐ 具体情况：\n否☑"}
        )

    st.subheader("7. 是否签订物的担保（抵押、质押）合同")
    q14_1 = st.radio("是否签订物的担保合同", ["否", "是"],
                     key="collateral_contract", horizontal=True)
    if q14_1 == "是":
        q14_2 = st_date_input("签订时间", key="collateral_contract_date")
        thisCase.reasons.append(
            {"type": "7. 是否签订物的担保（抵押、质押）合同", "information": f"是☑ 签订时间：{q14_2}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "7. 是否签订物的担保（抵押、质押）合同", "information": "是☐ 签订时间：\n否☑"}
        )

    st.subheader("8. 担保人、担保物")
    q15_1 = st.text_input("担保人", key="guarantor", placeholder="请输入担保人")
    q15_2 = st.text_input("担保物", key="collateral", placeholder="请输入担保物")
    thisCase.reasons.append(
        {"type": "8. 担保人、担保物", "information": f"担保人：{q15_1}\n担保物：{q15_2}"}
    )

    st.subheader("9. 是否最高额担保（抵押、质押）")
    q16_1 = st.radio("是否最高额担保", ["否", "是"],
                     key="maximum_guarantee", horizontal=True)
    if q16_1 == "是":
        q16_2 = st_date_input("担保债权的确定时间", key="guarantee_determination_date")
        q16_3 = st.number_input("担保额度", key="guarantee_amount",
                                placeholder="请输入担保额度", min_value=0.0, step=0.01, format="%.2f")
        thisCase.reasons.append(
            {"type": "9. 是否最高额担保（抵押、质押）", "information": f"是☑\n担保债权的确定时间：{
                q16_2}\n担保额度：{q16_3:.2f}元\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "9. 是否最高额担保（抵押、质押）", "information": "是☐\n担保债权的确定时间：\n担保额度：\n否☑"}
        )

    st.subheader("10. 是否办理抵押、质押登记")
    q17_1 = st.radio(
        "是否办理抵押、质押登记", ["否", "是"], key="collateral_registration", horizontal=True)
    if q17_1 == "是":
        q17_2 = st.radio("登记类型", ["正式登记", "预告登记"],
                         key="registration_type", horizontal=True)
        thisCase.reasons.append(
            {"type": "10. 是否办理抵押、质押登记", "information": f"是☑\n登记类型：{
                '正式登记☑ 预告登记☐' if q17_2 == '正式登记' else '正式登记☐ 预告登记☑'}"}
        )
    else:
        thisCase.reasons.append(
            {"type": "10. 是否办理抵押、质押登记", "information": "是☐\n登记类型：正式登记☐ 预告登记☐\n否☑"}
        )

    st.subheader("11. 是否签订保证合同")
    q18_1 = st.radio("是否签订保证合同", ["否", "是"],
                     key="guarantee_contract", horizontal=True)
    if q18_1 == "是":
        q18_2 = st_date_input("签订时间", key="guarantee_contract_date")
        q18_3 = st.text_input(
            "保证人", key="guarantee_person", placeholder="请输入保证人")
        q18_4 = st.text_area(
            "主要内容", key="guarantee_content", placeholder="请输入主要内容")
        thisCase.reasons.append(
            {"type": "11. 是否签订保证合同", "information": f"是☑\n签订时间：{
                q18_2}\n保证人：{q18_3}\n主要内容：{q18_4}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "11. 是否签订保证合同", "information": "是☐\n签订时间：\n保证人：\n主要内容：\n否☑"}
        )

    st.subheader("12. 保证方式")
    q19_1 = st.radio("保证方式", ["无", "一般保证", "连带责任保证"],
                     key="guarantee_type", horizontal=True)
    if q19_1 == "无":
        thisCase.reasons.append(
            {"type": "12. 保证方式", "information": "一般保证☐\n连带责任保证☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "12. 保证方式", "information": f"{
                '一般保证☑\n连带责任保证☐' if q19_1 == '一般保证' else '一般保证☐\n连带责任保证☑'}"}
        )

    st.subheader("13. 其他担保方式")
    q20_1 = st.radio("是否存在其他担保方式", ["否", "是"],
                     key="other_guarantee", horizontal=True)
    if q20_1 == "是":
        q20_2 = st.text_input(
            "担保形式", key="other_guarantee_form", placeholder="请输入担保形式")
        q20_3 = st_date_input("签订时间", key="other_guarantee_date")
        thisCase.reasons.append(
            {"type": "13. 其他担保方式", "information": f"是☑ 担保形式：{q20_2}；签订时间：{q20_3}\n否☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "13. 其他担保方式", "information": "是☐ 担保形式：\n签订时间：\n否☑"}
        )

    st.subheader("14. 其他需要说明的内容（可另附页）")
    q21_1 = st.text_area("其他需要说明的内容", key="other_information",
                         placeholder="请输入其他需要说明的内容")
    ai_component.ai_optimize_text(q21_1, "q21_1_b")
    thisCase.reasons.append(
        {"type": "14. 其他需要说明的内容（可另附页）", "information": q21_1}
    )

    st.subheader("15. 证据清单（可另附页）")
    q22_1 = st.text_area("证据清单（可另附页）", key="evidence_list",
                         placeholder="请输入证据清单（可另附页）")
    thisCase.reasons.append(
        {"type": "15. 证据清单（可另附页）", "information": q22_1}
    )

# 定义数据格式化器


class CreditCardCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

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
        st.error(f"生成文档时出错: {str(e)}")
