import streamlit as st
import json
from page.components.defendant import Respondent
from page.components.header import header
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import logging
import pandas as pd
from datetime import date, datetime

logger = logging.getLogger(__name__)

CASE_TYPE = '银行信用卡纠纷'


def respondent_details(thisCase: dict):
    # 1. 对透支本金有无异议
    st.subheader("1. 对透支本金有无异议")
    q1_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="q1_options", horizontal=True)
    if q1_options == "确认":
        q1_detail = f'确认☑\n异议☐  内容：'
    else:
        q1_fact = st.text_area("内容", key="q1_fact")
        q1_detail = f'确认☐\n异议☑ 内容：{q1_fact}'
    thisCase.replay_matters.append(q1_detail)

    # 2. 对利息、罚息、复利、滞纳金、违约金、手续费等有无异议
    st.subheader("2. 对利息、罚息、复利、滞纳金、违约金、手续费等有无异议")
    q2_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="q2_options", horizontal=True)
    if q2_options == "确认":
        q2_detail = f'确认☑\n异议☐  内容：'
    else:
        q2_fact = st.text_area("内容", key="q2_fact")
        q2_detail = f'确认☐\n异议☑ 内容：{q2_fact}'
    thisCase.replay_matters.append(q2_detail)

    # 3. 对担保权利诉请有无异议
    st.subheader("3. 对担保权利诉请有无异议")
    q3_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="q3_options", horizontal=True)
    if q3_options == "确认":
        q3_detail = f'确认☑\n异议☐  内容：'
    else:
        q3_fact = st.text_area("内容", key="q3_fact")
        q3_detail = f'确认☐\n异议☑ 内容：{q3_fact}'
    thisCase.replay_matters.append(q3_detail)

    # 4. 对实现债权的费用有无异议
    st.subheader("4. 对实现债权的费用有无异议")
    q4_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["无", "有"], key="q4_options", horizontal=True)
    if q4_options == "无":
        q4_detail = f'无☑\n有☐ 事实和理由：'
    else:
        q4_fact = st.text_area("事实和理由", key="q4_fact")
        q4_detail = f'无☐\n有☑ 事实和理由：{q4_fact}'
    thisCase.replay_matters.append(q4_detail)

    # 5. 对其他请求有无异议
    st.subheader("5. 对其他请求有无异议")
    q5_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["无", "有"], key="q5_options", horizontal=True)
    if q5_options == "无":
        q5_detail = f'无☑\n有☐ 事实和理由：'
    else:
        q5_fact = st.text_area("事实和理由", key="q5_fact")
        q5_detail = f'无☐\n有☑ 事实和理由：{q5_fact}'
    thisCase.replay_matters.append(q5_detail)

    # 6. 对标的总额有无异议
    st.subheader("6. 对标的总额有无异议")
    q6_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["无", "有"], key="q6_options", horizontal=True)
    if q6_options == "无":
        q6_detail = f'无☑\n有☐ 事实和理由：'
    else:
        q6_fact = st.text_area("事实和理由", key="q6_fact")
        q6_detail = f'无☐\n有☑ 事实和理由：{q6_fact}'
    thisCase.replay_matters.append(q6_detail)

    # 7. 答辩依据
    st.subheader("7. 答辩依据")
    q7_1 = st.text_area("合同约定", key="q7_1")
    q7_2 = st.text_area("法律规定", key="q7_2")
    q7_detail = f'合同约定：{q7_1}\n法律规定：{q7_2}'
    thisCase.replay_matters.append(q7_detail)


def fact_reason(thisCase: dict):
    # 1. 对信用卡办理情况有无异议
    st.subheader("1. 对信用卡办理情况有无异议")
    f1_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="f1_options", horizontal=True)
    if f1_options == "确认":
        f1_detail = f'确认☑\n异议☐ 事实和理由：'
    else:
        f1_fact = st.text_area("事实和理由", key="f1_fact")
        f1_detail = f'确认☐\n异议☑ 事实和理由：{f1_fact}'
    thisCase.reasons.append(f1_detail)

    # 2. 对信用卡合约的主要约定有无异议
    st.subheader("2. 对信用卡合约的主要约定有无异议")
    f2_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="f2_options", horizontal=True)
    if f2_options == "确认":
        f2_detail = f'确认☑\n异议☐ 事实和理由：'
    else:
        f2_fact = st.text_area("事实和理由", key="f2_fact")
        f2_detail = f'确认☐\n异议☑ 事实和理由：{f2_fact}'
    thisCase.reasons.append(f2_detail)

    # 3. 对原告对被告就信用卡合约主要条款进行提示注意、说明的情况有无异议
    st.subheader("3. 对原告对被告就信用卡合约主要条款进行提示注意、说明的情况有无异议")
    f3_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="f3_options", horizontal=True)
    if f3_options == "确认":
        f3_detail = f'确认☑\n异议☐ 事实和理由：'
    else:
        f3_fact = st.text_area("事实和理由", key="f3_fact")
        f3_detail = f'确认☐\n异议☑ 事实和理由：{f3_fact}'
    thisCase.reasons.append(f3_detail)

    # 4. 对被告已还款金额有无异议
    st.subheader("4. 对被告已还款金额有无异议")
    f4_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="f4_options", horizontal=True)
    if f4_options == "确认":
        f4_detail = f'确认☑\n异议☐ 事实和理由：'
    else:
        f4_fact = st.text_area("事实和理由", key="f4_fact")
        f4_detail = f'确认☐\n异议☑ 事实和理由：{f4_fact}'
    thisCase.reasons.append(f4_detail)

    # 5. 对被告逾期未还款金额有无异议
    st.subheader("5. 对被告逾期未还款金额有无异议")
    f5_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="f5_options", horizontal=True)
    if f5_options == "确认":
        f5_detail = f'确认☑\n异议☐ 事实和理由：'
    else:
        f5_fact = st.text_area("事实和理由", key="f5_fact")
        f5_detail = f'确认☐\n异议☑ 事实和理由：{f5_fact}'
    thisCase.reasons.append(f5_detail)

    # 6. 对是否向被告进行通知和催收有无异议
    st.subheader("6. 对是否向被告进行通知和催收有无异议")
    f6_options = st.radio(
        label='No label',label_visibility = 'collapsed',  options=["确认", "异议"], key="f6_options", horizontal=True)
    if f6_options == "确认":
        f6_detail = f'确认☑\n异议☐ 事实和理由：'
    else:
        f6_fact = st.text_area("事实和理由", key="f6_fact")
        f6_detail = f'确认☐\n异议☑ 事实和理由：{f6_fact}'
    thisCase.reasons.append(f6_detail)

    # 7-14. 对担保相关问题
    for i in range(7, 15):
        question_texts = {
            7: "对是否签订物的担保合同有无异议",
            8: "对担保人、担保物有无异议",
            9: "对最高额抵押担保有无异议",
            10: "对是否办理抵押/质押登记有无异议",
            11: "对是否签订保证合同有无异议",
            12: "对保证方式有无异议",
            13: "对其他担保方式有无异议",
            14: "有无其他免责/减责事由"
        }

        st.subheader(f"{i}. {question_texts[i]}")
        option_var = st.radio(label='No label',label_visibility = 'collapsed',  options=["无", "有"], key=f"f{
                              i}_options", horizontal=True)
        if option_var == "无":
            detail = f'无☑\n有☐ 事实和理由：'
        else:
            fact = st.text_area("事实和理由", key=f"f{i}_fact")
            detail = f'无☐\n有☑ 事实和理由：{fact}'
        thisCase.reasons.append(detail)

    # 15. 其他需要说明的内容
    st.subheader("15. 其他需要说明的内容")
    f15_content = st.text_area("其他内容", key="f15_content")
    thisCase.reasons.append(f15_content)

    # 16. 证据清单
    st.subheader("16. 证据清单")
    f16_content = st.text_area("证据清单", key="f16_content")
    thisCase.reasons.append(f16_content)


class CreditCardCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE
    BaseCaseFormatter.isComplete = False

    @staticmethod
    def format_case(case):
        """将案件对象转换为适合文档模板的格式"""
        # try:
        case_data = json.loads(case.to_json())

        # 调用父类的通用格式化方法
        template_data = super(CreditCardCaseFormatter,
                                CreditCardCaseFormatter).format_case(case)

        # 添加案件的自定义部分
        template_data.update({
            "reply_matters": CreditCardCaseFormatter._format_reply_matters(case_data)
        })
        template_data.update({"reasons": CreditCardCaseFormatter._format_reasons(case_data)})

        return template_data

        # except Exception as e:
        #     logger.error(f"格式化案件数据时出错: {str(e)}")
        #     raise ValueError(f"格式化案件数据失败: {str(e)}")

    @staticmethod
    def _format_reply_matters(case_data):
        """Format reply matters from the case data"""
        # Get the reply matters array from case data
        reply_matters = case_data.get('replay_matters', [])

        # The indices correspond to the questions in respondent_details
        matter_types = [
            "1. 对透支本金有无异议",
            "2. 对利息、罚息、复利、滞纳金、违约金、手续费等有无异议",
            "3. 对担保权利诉请有无异议",
            "4. 对实现债权的费用有无异议",
            "5. 对其他请求有无异议",
            "6. 对标的总额有无异议",
            "7. 答辩依据"
        ]

        formatted_matters = []

        # Format each reply matter with its corresponding type
        for i, matter_type in enumerate(matter_types):
            if i < len(reply_matters):
                formatted_matters.append({
                    "type": matter_type,
                    "information": reply_matters[i]
                })
            else:
                formatted_matters.append({
                    "type": matter_type,
                    "information": ""
                })

        return formatted_matters

    @staticmethod
    def _format_reasons(case_data):
        """Format reasons from the case data"""
        # Get the reasons array from case data
        reasons = case_data.get('reasons', [])

        # The indices correspond to the questions in the image
        reason_types = [
            "1. 对信用卡办理情况有无异议",
            "2. 对信用卡合约的主要约定有无异议",
            "3. 对原告对被告就信用卡合约主要条款进行提示注意、说明的情况有无异议",
            "4. 对被告已还款金额有无异议",
            "5. 对被告逾期未还款金额有无异议",
            "6. 对是否向被告进行通知和催收有无异议",
            "7. 对是否签订物的担保合同有无异议",
            "8. 对担保人、担保物有无异议",
            "9. 对最高额抵押担保有无异议",
            "10. 对是否办理抵押/质押登记有无异议",
            "11. 对是否签订保证合同有无异议",
            "12. 对保证方式有无异议",
            "13. 对其他担保方式有无异议",
            "14. 有无其他免责/减责事由",
            "15. 其他需要说明的内容（可另附页）",
            "16. 证据清单（可另附页）"
        ]

        formatted_reasons = []

        # Format each reason with its corresponding type
        for i, reason_type in enumerate(reason_types):
            if i < len(reasons):
                formatted_reasons.append({
                    "type": reason_type,
                    "information": reasons[i]
                })
            else:
                formatted_reasons.append({
                    "type": reason_type,
                    "information": ""
                })

        return formatted_reasons


class CreditCardCaseRespondent:
    def __init__(self):
        self.respondent = None
        self.case_num = None
        self.replay_matters = []
        self.reasons = []

    def to_json(self):
        # 自定义序列化函数
        def default_serializer(obj):
            if isinstance(obj, date):  # 处理 datetime.date 对象
                return obj.isoformat()
            elif hasattr(obj, '__dict__'):  # 处理普通对象
                return obj.__dict__
            elif isinstance(obj, pd.DataFrame):  # 处理 DataFrame 对象
                return obj.to_dict(orient='records')
            else:
                return str(obj)  # 其他情况转换为字符串

        # 使用自定义的序列化函数
        return json.dumps(self.__dict__, default=default_serializer, indent=4)


thisCase = CreditCardCaseRespondent()


header(CASE_TYPE, "答辩状")

st.markdown("""______""")
st.subheader('案号')
thisCase.case_num = st.text_input(
    '请输入案号：', '', placeholder='示例：(2025)粤01民终0001号')
st.header("当事人信息")
# 答辩人部分
respondent = Respondent(CASE_TYPE)
respondent.show()
thisCase.respondent = respondent
st.markdown("""______""")
st.header("答辩事项和依据（对原告诉讼请求的确认或者异议）")
respondent_details(thisCase)
st.header("事实和理由（对起诉状事实与理由的确认或者异议）")
fact_reason(thisCase)

if st.button("生成答辩状"):
    # 输出 JSON 格式的案件信息
    st.write("案件信息（JSON 格式）:")
    st.json(thisCase.to_json())
    print(thisCase.to_json())

    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "defense",
                thisCase,
                CreditCardCaseFormatter,
                thisCase.respondent.respondents[0]["name"],
            )

        st.download_button(
            label="下载答辩状",
            data=doc_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"生成文档时出错: {str(e)}")
