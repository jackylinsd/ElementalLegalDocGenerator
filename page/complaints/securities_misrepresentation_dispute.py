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
CASE_TYPE = "证券虚假陈述责任纠纷"

# 定义诉讼请求和依据的问题
REPLY_QUESTIONS = [
    "赔偿因虚假陈述导致的损失",
    "是否主张连带责任",
    "是否主张实现债权的费用",
    "其他请求",
    "标的总额",
    "请求依据"
]

# 定义事实和理由的问题
REASON_QUESTIONS = [
    "被告存在虚假陈述行为的情况",
    "有无监管部门的认定、处罚",
    "原告交易情况",
    "虚假陈述的重大性",
    "虚假陈述与原告交易行为之间的因果关系",
    "虚假陈述与原告损失之间的因果关系",
    "原告损失情况",
    "请求发行人的控股股东、实际控制人、董监高、相关责任人员承担连带责任的情况",
    "请求保荐机构、承销机构、律师事务所、会计师事务所等其他机构及其相关责任人员承担连带责任的情况",
    "其他需要说明的内容",
    "证据清单"
]

# 初始化案件对象
thisCase = CommonCasePlaintiff()

# 定义诉讼请求和依据部分
def claim(thisCase):
    st.subheader("1. 赔偿因虚假陈述导致的损失")
    q1_1 = st.number_input("投资差额损失", key="investment_loss", placeholder="请输入投资差额损失", min_value=0.0, step=0.01, format="%.2f")
    q1_2 = st.number_input("佣金损失", key="commission_loss", placeholder="请输入佣金损失", min_value=0.0, step=0.01, format="%.2f")
    q1_3 = st.number_input("印花税损失", key="stamp_duty_loss", placeholder="请输入印花税损失", min_value=0.0, step=0.01, format="%.2f")
    q1_4 = st.checkbox('是否为外币')
    if q1_4:
        q1_5 = st.text_input("外币币种", key="currency_type", placeholder="请输入外币币种")
    thisCase.reply_matters.append(
        {"type": "1. 赔偿因虚假陈述导致的损失", "information": f"投资差额损失{q1_1:.2f}元、佣金损失{q1_2:.2f}元、印花税损失{q1_3:.2f}元（{'人民币，下同；如外币需特别注明' if not q1_4 else q1_5})"}
    )

    st.subheader("2. 是否主张连带责任")
    q2_1 = st.radio("是否主张连带责任", ["是", "否"], key="joint_liability", horizontal=True)
    if q2_1 == "是":
        q2_2 = st.text_area("责任主体及责任范围", key="liability_details", placeholder="请输入责任主体及责任范围")
        thisCase.reply_matters.append(
            {"type": "2. 是否主张连带责任", "information": f"是☑ 责任主体及责任范围：{q2_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "2. 是否主张连带责任", "information": "是☐ 责任主体及责任范围：\n否☑"}
        )

    st.subheader("3. 是否主张实现债权的费用")
    q3_1 = st.radio("是否主张实现债权的费用", ["是", "否"], key="legal_fees", horizontal=True)
    if q3_1 == "是":
        q3_2 = st.text_area("费用明细", key="legal_fees_details", placeholder="请输入费用明细")
        thisCase.reply_matters.append(
            {"type": "3. 是否主张实现债权的费用", "information": f"是☑ 费用明细：{q3_2}\n否☐"}
        )
    else:
        thisCase.reply_matters.append(
            {"type": "3. 是否主张实现债权的费用", "information": "是☐ 费用明细：\n否☑"}
        )

    st.subheader("4. 其他请求")
    q4_1 = st.text_area("其他请求", key="other_requests", placeholder="请输入其他请求")
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

# 定义事实和理由部分
def fact(thisCase):
    st.subheader("1. 被告存在虚假陈述行为的情况")
    q7_1 = st.text_area("具体虚假陈述行为", key="misrepresentation_details", placeholder="请输入具体虚假陈述行为")
    q7_2 = st_date_input("虚假陈述行为实施日", key="misrepresentation_implementation_date")
    q7_3 = st_date_input("虚假陈述行为揭露日", key="misrepresentation_disclosure_date")
    q7_4 = st_date_input("虚假陈述行为更正日", key="misrepresentation_correction_date")
    q7_5 = st_date_input("虚假陈述基准日", key="misrepresentation_base_date")
    thisCase.reasons.append(
        {"type": "1. 被告存在虚假陈述行为的情况", "information": f"具体虚假陈述行为：{q7_1}\n虚假陈述行为实施日：{q7_2}\n虚假陈述行为揭露日：{q7_3}\n虚假陈述行为更正日：{q7_4}\n虚假陈述基准日：{q7_5}"}
    )

    st.subheader("2. 有无监管部门的认定、处罚")
    q8_1 = st.radio("有无监管部门的认定、处罚", ["否", "是"], key="regulatory_action", horizontal=True)
    if q8_1 == "有":
        q8_2 = st.text_area("具体情况", key="regulatory_details", placeholder="请输入具体情况")
        thisCase.reasons.append(
            {"type": "2. 有无监管部门的认定、处罚", "information": f"有☑ 具体情况：{q8_2}\n无☐"}
        )
    else:
        thisCase.reasons.append(
            {"type": "2. 有无监管部门的认定、处罚", "information": "有☐ 具体情况：\n无☑"}
        )

    st.subheader("3. 原告交易情况")
    q9_1 = st.text_area("买入情况（日期、数量、单价）", key="buy_details", placeholder="请输入买入情况（日期、数量、单价）")
    q9_2 = st.text_area("卖出情况（日期、数量、单价）", key="sell_details", placeholder="请输入卖出情况（日期、数量、单价）")
    thisCase.reasons.append(
        {"type": "3. 原告交易情况", "information": f"买入情况：{q9_1}\n卖出情况：{q9_2}"}
    )

    st.subheader("4. 虚假陈述的重大性")
    q10_1 = st.text_area("虚假陈述的重大性", key="misrepresentation_significance", placeholder="请输入虚假陈述的重大性")
    thisCase.reasons.append(
        {"type": "4. 虚假陈述的重大性", "information": q10_1}
    )

    st.subheader("5. 虚假陈述与原告交易行为之间的因果关系")
    q11_1 = st.text_area("虚假陈述与原告交易行为之间的因果关系", key="causation_trading", placeholder="请输入虚假陈述与原告交易行为之间的因果关系")
    thisCase.reasons.append(
        {"type": "5. 虚假陈述与原告交易行为之间的因果关系", "information": q11_1}
    )

    st.subheader("6. 虚假陈述与原告损失之间的因果关系")
    q12_1 = st.text_area("虚假陈述与原告损失之间的因果关系", key="causation_loss", placeholder="请输入虚假陈述与原告损失之间的因果关系")
    thisCase.reasons.append(
        {"type": "6. 虚假陈述与原告损失之间的因果关系", "information": q12_1}
    )

    st.subheader("7. 原告损失情况")
    q13_1 = st.number_input("因虚假陈述所造成的投资差额损失", key="investment_loss_reason", placeholder="请输入投资差额损失", min_value=0.0, step=0.01, format="%.2f")
    q13_2 = st.number_input("佣金和印花税损失", key="commission_stamp_duty_loss", placeholder="请输入佣金和印花税损失", min_value=0.0, step=0.01, format="%.2f")
    q13_3 = st.text_area("其他损失", key="other_losses", placeholder="请输入其他损失")
    q13_4 = st.text_area("明细", key="loss_details", placeholder="请输入明细")
    thisCase.reasons.append(
        {"type": "7. 原告损失情况", "information": f"因虚假陈述所造成的投资差额损失：{q13_1:.2f}元\n佣金和印花税损失：{q13_2:.2f}元\n其他损失：{q13_3}\n明细：{q13_4}"}
    )

    st.subheader("8. 请求发行人的控股股东、实际控制人、董监高、相关责任人员承担连带责任的情况")
    q14_1 = st.text_area("请求发行人的控股股东、实际控制人、董监高、相关责任人员承担连带责任的情况", key="issuer_liability", placeholder="请输入相关情况")
    thisCase.reasons.append(
        {"type": "8. 请求发行人的控股股东、实际控制人、董监高、相关责任人员承担连带责任的情况", "information": q14_1}
    )

    st.subheader("9. 请求保荐机构、承销机构、律师事务所、会计师事务所等其他机构及其相关责任人员承担连带责任的情况")
    q15_1 = st.text_area("请求保荐机构、承销机构、律师事务所、会计师事务所等其他机构及其相关责任人员承担连带责任的情况", key="other_entities_liability", placeholder="请输入相关情况")
    thisCase.reasons.append(
        {"type": "9. 请求保荐机构、承销机构、律师事务所、会计师事务所等其他机构及其相关责任人员承担连带责任的情况", "information": q15_1}
    )

    st.subheader("10. 其他需要说明的内容")
    q16_1 = st.text_area("其他需要说明的内容", key="other_information", placeholder="请输入其他需要说明的内容")
    thisCase.reasons.append(
        {"type": "10. 其他需要说明的内容", "information": q16_1}
    )

    st.subheader("11. 证据清单（可另附页）")
    q17_1 = st.text_area("证据清单（可另附页）", key="evidence_list", placeholder="请输入证据清单（可另附页）")
    thisCase.reasons.append(
        {"type": "11. 证据清单（可另附页）", "information": q17_1}
    )

# 定义数据格式化器
class MisrepresentationCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(thisCase):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(thisCase.to_json())
        template_data = super(MisrepresentationCaseFormatter,
                              MisrepresentationCaseFormatter).format_case(thisCase)

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
                MisrepresentationCaseFormatter,
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