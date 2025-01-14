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
CASE_TYPE = "机动车交通事故责任纠纷"

# 定义诉讼请求和依据的问题
REPLY_QUESTIONS = [
    "医疗费",
    "护理费",
    "营养费",
    "住院伙食补助费",
    "误工费",
    "交通费",
    "残疾赔偿金",
    "残疾辅助器具费",
    "死亡赔偿金、丧葬费",
    "精神损害赔偿金",
    "其他费用"
]

# 定义事实和理由的问题
REASON_QUESTIONS = [
    "交通事故发生情况",
    "交通事故责任认定",
    "机动车投保情况",
    "其他情况及法律依据",
    "证据清单"
]

# 初始化案件对象
thisCase = CommonCasePlaintiff()

Y_N = ["有☑ 无☐", "有☐ 无☑"]

# 定义诉讼请求和依据部分
def claim(thisCase):
    st.subheader("1. 医疗费")
    q1_1 = st_date_input("住院/门诊时间", key="medical_period")
    q1_2 = st.text_input("医院名称", key="hospital_name", placeholder="请输入医院名称")
    q1_3 = st.number_input("医疗费金额", key="medical_cost", placeholder="请输入医疗费金额")
    q1_4 = st.radio("是否有医疗费发票、清单、病例资料", ["有", "无"], key="medical_documents", horizontal=True)
    thisCase.reply_matters.append(
        {"type": "1. 医疗费", "information": f"{q1_1}期间在{q1_2}住院（门诊）治疗，累计发生医疗费{q1_3}元；医疗费发票、清单、病例资料：{Y_N[1] if q1_4 else Y_N[1]}"}
    )

    st.subheader("2. 护理费")
    q2_1 = st.number_input("护理天数", key="nursing_days", placeholder="请输入护理天数",step=0.5,format="%0.1f")
    q2_2 = st.number_input("护理费金额", key="nursing_cost", placeholder="请输入护理费金额")
    q2_3 = st.radio("是否有住院证明、医嘱等", ["有", "无"], key="nursing_documents", horizontal=True)
    thisCase.reply_matters.append(
        {"type": "2. 护理费", "information": f"住院护理{q2_1}天，支付护理费{q2_2}元；住院证明、医嘱等：{Y_N[0] if q2_3 else Y_N[1]}"}
    )

    st.subheader("3. 营养费")
    q3_1 = st.number_input("营养费金额", key="nutrition_cost", placeholder="请输入营养费金额")
    q3_2 = st.radio("是否有病例资料", ["有", "无"], key="nutrition_documents", horizontal=True)
    thisCase.reply_matters.append(
        {"type": "3. 营养费", "information": f"营养费{q3_1}元；病例资料：{Y_N[0] if  q3_2 else Y_N[1]}"}
    )

    st.subheader("4. 住院伙食补助费")
    q4_1 = st.number_input("住院伙食补助费金额", key="meal_cost", placeholder="请输入住院伙食补助费金额")
    q4_2 = st.radio("是否有病例资料", ["有", "无"], key="meal_documents", horizontal=True)
    thisCase.reply_matters.append(
        {"type": "4. 住院伙食补助费", "information": f"住院伙食补助费{q4_1}元；病例资料：{Y_N[0] if  q4_2 else Y_N[1]}"}
    )

    st.subheader("5. 误工费")
    q5_1 = st_date_input("误工时间(开始)", key="lost_work_period_start")
    q5_2 = st_date_input("误工时间(结束)", key="lost_work_period_end")
    q5_3 = st.number_input("误工费金额", key="lost_work_cost", placeholder="请输入误工费金额")
    thisCase.reply_matters.append(
        {"type": "5. 误工费", "information": f"{q5_1}至{q5_2}期间误工费{q5_3}元"}
    )

    st.subheader("6. 交通费")
    q6_1 = st.number_input("交通费金额", key="transport_cost", placeholder="请输入交通费金额")
    q6_2 = st.radio("是否有交通费凭证", ["有", "无"], key="transport_documents", horizontal=True)
    thisCase.reply_matters.append(
        {"type": "6. 交通费", "information": f"交通费{q6_1}元；交通费凭证：{Y_N[0] if q6_2 else Y_N[1]}"}
    )

    st.subheader("7. 残疾赔偿金")
    q7_1 = st.number_input("残疾赔偿金金额", key="disability_cost", placeholder="请输入残疾赔偿金金额")
    thisCase.reply_matters.append(
        {"type": "7. 残疾赔偿金", "information": f"残疾赔偿金{q7_1}元"}
    )

    st.subheader("8. 残疾辅助器具费")
    q8_1 = st.number_input("残疾辅助器具费金额", key="assistance_cost", placeholder="请输入残疾辅助器具费金额")
    thisCase.reply_matters.append(
        {"type": "8. 残疾辅助器具费", "information": f"残疾辅助器具费{q8_1}元"}
    )

    st.subheader("9. 死亡赔偿金、丧葬费")
    q9_1 = st.number_input("死亡赔偿金金额", key="death_cost", placeholder="请输入死亡赔偿金金额")
    q9_2 = st.number_input("丧葬费金额", key="funeral_cost", placeholder="请输入丧葬费金额")
    thisCase.reply_matters.append(
        {"type": "9. 死亡赔偿金、丧葬费", "information": f"死亡赔偿金{q9_1}元，丧葬费{q9_2}元"}
    )

    st.subheader("10. 精神损害赔偿金")
    q10_1 = st.number_input("精神损害赔偿金金额", key="mental_cost", placeholder="请输入精神损害赔偿金金额")
    thisCase.reply_matters.append(
        {"type": "10. 精神损害赔偿金", "information": f"精神损害赔偿金{q10_1}元"}
    )

    st.subheader("11. 其他费用")
    q11_1 = st.text_area("其他费用", key="other_cost", placeholder="请输入其他费用")
    thisCase.reply_matters.append(
        {"type": "11. 其他费用", "information": q11_1}
    )


# 定义事实和理由部分
def fact(thisCase):
    st.subheader("1. 交通事故发生情况")
    q12_1 = st.text_area("事故发生情况", key="accident_details", placeholder="请输入事故发生情况")
    thisCase.reasons.append(
        {"type": "1. 交通事故发生情况", "information": q12_1}
    )

    st.subheader("2. 交通事故责任认定")
    q13_1 = st.text_area("责任认定情况", key="responsibility_details", placeholder="请输入责任认定情况")
    thisCase.reasons.append(
        {"type": "2. 交通事故责任认定", "information": q13_1}
    )

    st.subheader("3. 机动车投保情况")
    q14_1 = st.text_area("投保情况", key="insurance_details", placeholder="请输入机动车投保情况")
    thisCase.reasons.append(
        {"type": "3. 机动车投保情况", "information": q14_1}
    )

    st.subheader("4. 其他情况及法律依据")
    q15_1 = st.text_area("其他情况及法律依据", key="other_details", placeholder="请输入其他情况及法律依据")
    thisCase.reasons.append(
        {"type": "4. 其他情况及法律依据", "information": q15_1}
    )

    st.subheader("5. 证据清单")
    q16_1 = st.text_area("证据清单", key="evidence_list", placeholder="请输入证据清单")
    thisCase.reasons.append(
        {"type": "5. 证据清单", "information": q16_1}
    )

class TrafficAccidentCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(thisCase):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(thisCase.to_json())
        template_data = super(TrafficAccidentCaseFormatter,
                              TrafficAccidentCaseFormatter).format_case(thisCase)

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
st.header("事实和理由")
fact(thisCase)

# 生成起诉状
if st.button("生成起诉状"):
    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "complaint_2p",
                thisCase,
                TrafficAccidentCaseFormatter,
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