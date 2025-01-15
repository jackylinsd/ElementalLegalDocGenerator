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
CASE_TYPE = "物业服务合同纠纷"

# 定义诉讼请求和依据的问题
REPLY_QUESTIONS = [
    "物业费",
    "违约金",
    "其他请求",
    "标的总额",
    "请求依据"
]

# 定义事实和理由的问题
REASON_QUESTIONS = [
    "物业服务合同或前期物业服务合同签订情况",
    "签订主体",
    "物业项目情况",
    "约定的物业费标准",
    "约定的物业服务期限",
    "约定的物业费支付方式",
    "约定的逾期支付物业费违约金标准",
    "被告欠付物业费数额及计算方式",
    "被告应付违约金数额及计算方式",
    "催缴情况",
    "其他需要说明的内容",
    "证据清单"
]

# 初始化案件对象
thisCase = CommonCasePlaintiff()

# 定义诉讼请求和依据部分


def claim(thisCase):
    st.subheader("1. 物业费")
    q1_1 = st_date_input("截至日期", key="property_fee_due_date")
    q1_2 = st.number_input(
        "尚欠物业费金额", key="property_fee_amount", placeholder="请输入尚欠物业费金额")
    thisCase.reply_matters.append(
        {"type": "1. 物业费", "information": f"截至{q1_1}止，尚欠物业费{q1_2}元"}
    )

    st.subheader("2. 违约金")
    q2_1 = st_date_input("截至日期", key="penalty_due_date")
    q2_2 = st.number_input("违约金", key="penalty_amount", placeholder="请输入违约金")
    q2_3 = st.radio("是否请求支付至实际清偿之日止", ["是", "否"],
                    key="penalty_until_payment", horizontal=True)
    thisCase.reply_matters.append(
        {"type": "2. 违约金", "information": f"截至{q2_1}止，欠逾期物业费的违约金{
            q2_2}元\n是否请求支付至实际清偿之日止：{'是☑ 否☐' if q2_1 == '是' else '是☐ 否☑'}"}
    )

    st.subheader("3. 其他请求")
    q3_1 = st.text_area("其他请求", key="other_requests", placeholder="请输入其他请求")
    thisCase.reply_matters.append(
        {"type": "3. 其他请求", "information": q3_1}
    )

    st.subheader("4. 标的总额")
    q4_1 = st.text_area("标的总额", key="total_amount", placeholder="请输入标的总额")
    thisCase.reply_matters.append(
        {"type": "4. 标的总额", "information": q4_1}
    )

    st.subheader("5. 请求依据")
    q5_1 = st.text_area("合同约定", key="contract_terms", placeholder="请输入合同约定")
    q5_2 = st.text_area("法律规定", key="legal_provisions", placeholder="请输入法律规定")
    thisCase.reply_matters.append(
        {"type": "5. 请求依据", "information": f"合同约定：{q5_1}\n法律规定：{q5_2}"}
    )

# 定义事实和理由部分


def fact(thisCase):
    st.subheader("1. 物业服务合同或前期物业服务合同签订情况")
    q6_0 = st.radio("填写方式", ["模版填写", "自定义填写"],
                    key="contract_info_type", horizontal=True)
    if q6_0 == "模版填写":
        q6_1 = st.text_input("合同名称", key="contract_name",
                             placeholder="请输入合同名称")
        q6_2 = st.text_input("合同编号", key="contract_number",
                             placeholder="请输入合同编号")
        q6_3 = st_date_input("签订时间", key="contract_date")
        q6_4 = st.text_input(
            "签订地点", key="contract_location", placeholder="请输入签订地点")
        thisCase.reasons.append(
            {"type": "1. 物业服务合同或前期物业服务合同签订情况", "information": f"合同名称：{
                q6_1}\n合同编号：{q6_2}\n签订时间：{q6_3}\n签订地点：{q6_4}"}
        )
    else:
        q6_t = st.text_area("合同签订情况", key="contract_info",
                            placeholder="合同主体、签订时间、地点、合同名称等")
        thisCase.reasons.append(
            {"type": "1. 物业服务合同或前期物业服务合同签订情况", "information": q6_t}
        )

    st.subheader("2. 签订主体")
    q7_1 = st.text_input("业主/建设单位", key="owner", placeholder="请输入业主/建设单位")
    q7_2 = st.text_input(
        "物业服务人", key="property_service_provider", placeholder="请输入物业服务人")
    thisCase.reasons.append(
        {"type": "2. 签订主体", "information": f"业主/建设单位：{q7_1}\n物业服务人：{q7_2}"}
    )

    st.subheader("3. 物业项目情况")
    q8_1 = st.text_input("坐落位置", key="property_location",
                         placeholder="请输入坐落位置")
    q8_2 = st.number_input("面积", key="property_area", placeholder="请输入面积")
    q8_2_1 = st.text_input("单位", key="property_area_unit",
                           placeholder="请输入面积单位", value="平方米")
    q8_3 = st.text_input("所有权人", key="property_owner", placeholder="请输入所有权人")
    thisCase.reasons.append(
        {"type": "3. 物业项目情况", "information": f"坐落位置：{
            q8_1}\n面积：{q8_2}{q8_2_1}\n所有权人：{q8_3}"}
    )

    st.subheader("4. 约定的物业费标准")
    q9_1 = st.text_input(
        "物业费标准", key="property_fee_standard", placeholder="请输入物业费标准")
    thisCase.reasons.append(
        {"type": "4. 约定的物业费标准", "information": q9_1}
    )

    st.subheader("5. 约定的物业服务期限")
    q10_1 = st_date_input("服务期限开始日期", key="service_start_date")
    q10_2 = st_date_input("服务期限结束日期", key="service_end_date")
    thisCase.reasons.append(
        {"type": "5. 约定的物业服务期限", "information": f"服务期限：{q10_1}至{q10_2}"}
    )

    st.subheader("6. 约定的物业费支付方式")
    q11_1 = st.text_input(
        "物业费支付方式", key="property_fee_payment_method", placeholder="请输入物业费支付方式")
    thisCase.reasons.append(
        {"type": "6. 约定的物业费支付方式", "information": q11_1}
    )

    st.subheader("7. 约定的逾期支付物业费违约金标准")
    q12_1 = st.text_input("违约金标准", key="penalty_standard",
                          placeholder="请输入违约金标准")
    thisCase.reasons.append(
        {"type": "7. 约定的逾期支付物业费违约金标准", "information": q12_1}
    )

    st.subheader("8. 被告欠付物业费数额及计算方式")
    q13_1 = st.number_input(
        "欠付物业费数额", key="unpaid_property_fee", placeholder="请输入欠付物业费数额")
    q13_2 = st.text_area("具体计算方式", key="calculation_method",
                         placeholder="请输入具体计算方式")
    thisCase.reasons.append(
        {"type": "8. 被告欠付物业费数额及计算方式", "information": f"欠付物业费数额：{q13_1}元；具体计算方式：{q13_2}"}
    )

    st.subheader("9. 被告应付违约金数额及计算方式")
    q14_1 = st.number_input("应付违约金数额", key="penalty_amount_2",
                            placeholder="请输入应付违约金数额", format="%0.2f", step=0.01, min_value=0.00)
    q14_2 = st.text_area(
        "具体计算方式", key="penalty_calculation", placeholder="请输入具体计算方式")
    thisCase.reasons.append(
        {"type": "9. 被告应付违约金数额及计算方式", "information": f"应付违约金数额：{q14_1}元；具体计算方式：{q14_2}"}
    )

    st.subheader("10. 催缴情况")
    q15_1 = st.text_area("催缴情况", key="collection_details",
                         placeholder="请输入催缴情况")
    thisCase.reasons.append(
        {"type": "10. 催缴情况", "information": q15_1}
    )

    st.subheader("11. 其他需要说明的内容")
    q16_1 = st.text_area("其他需要说明的内容", key="other_information",
                         placeholder="请输入其他需要说明的内容")
    thisCase.reasons.append(
        {"type": "11. 其他需要说明的内容", "information": q16_1}
    )

    st.subheader("12. 证据清单（可另附页）")
    q17_1 = st.text_area("证据清单（可另附页）", key="evidence_list",
                         placeholder="请输入证据清单（可另附页）")
    thisCase.reasons.append(
        {"type": "12. 证据清单（可另附页）", "information": q17_1}
    )

# 定义数据格式化器


class PropertyServiceCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(thisCase):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(thisCase.to_json())
        template_data = super(PropertyServiceCaseFormatter,
                              PropertyServiceCaseFormatter).format_case(thisCase)

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
                PropertyServiceCaseFormatter,
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
