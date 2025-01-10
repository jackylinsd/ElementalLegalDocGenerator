import streamlit as st
import json
from page.components.defendant import Respondent
from page.components.header import header
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import logging
import pandas as pd
from datetime import date, datetime

logger = logging.getLogger(__name__)

CASE_TYPE = '融资租赁合同纠纷'

def respondent_details(thisCase: dict):
    # 1. 对支付全部未付租金的诉请有无异议
    st.subheader("1. 对支付全部未付租金的诉请有无异议")
    q1_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q1_options", horizontal=True)
    if q1_options == "无异议":
        q1_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q1_fact = st.text_area("事实和理由", key="q1_fact")
        q1_detail = f'无异议☐\n有异议☑ 事实和理由：{q1_fact}'
    thisCase.replay_matters.append(q1_detail)

    # 2. 对违约金、滞纳金、损害赔偿金有无异议
    st.subheader("2. 对违约金、滞纳金、损害赔偿金有无异议")
    q2_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q2_options", horizontal=True)
    if q2_options == "无异议":
        q2_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q2_fact = st.text_area("事实和理由", key="q2_fact")
        q2_detail = f'无异议☐\n有异议☑ 事实和理由：{q2_fact}'
    thisCase.replay_matters.append(q2_detail)

    # 3. 对确认租赁物归原告所有有无异议
    st.subheader("3. 对确认租赁物归原告所有有无异议")
    q3_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q3_options", horizontal=True)
    if q3_options == "无异议":
        q3_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q3_fact = st.text_area("事实和理由", key="q3_fact")
        q3_detail = f'无异议☐\n有异议☑ 事实和理由：{q3_fact}'
    thisCase.replay_matters.append(q3_detail)

    # 4. 对解除合同有无异议
    st.subheader("4. 对解除合同有无异议")
    q4_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q4_options", horizontal=True)
    if q4_options == "无异议":
        q4_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q4_fact = st.text_area("事实和理由", key="q4_fact")
        q4_detail = f'无异议☐\n有异议☑ 事实和理由：{q4_fact}'
    thisCase.replay_matters.append(q4_detail)

    # 5. 对返还租赁物，并赔偿因解除合同而受到的损失有无异议
    st.subheader("5. 对返还租赁物，并赔偿因解除合同而受到的损失有无异议")
    q5_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q5_options", horizontal=True)
    if q5_options == "无异议":
        q5_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q5_fact = st.text_area("事实和理由", key="q5_fact")
        q5_detail = f'无异议☐\n有异议☑ 事实和理由：{q5_fact}'
    thisCase.replay_matters.append(q5_detail)

    # 6. 对担保权利的诉请有无异议
    st.subheader("6. 对担保权利的诉请有无异议")
    q6_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q6_options", horizontal=True)
    if q6_options == "无异议":
        q6_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q6_fact = st.text_area("事实和理由", key="q6_fact")
        q6_detail = f'无异议☐\n有异议☑ 事实和理由：{q6_fact}'
    thisCase.replay_matters.append(q6_detail)

    # 7. 对实现债权的费用有无异议
    st.subheader("7. 对实现债权的费用有无异议")
    q7_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q7_options", horizontal=True)
    if q7_options == "无异议":
        q7_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q7_fact = st.text_area("事实和理由", key="q7_fact")
        q7_detail = f'无异议☐\n有异议☑ 事实和理由：{q7_fact}'
    thisCase.replay_matters.append(q7_detail)

    # 8. 对其他请求有无异议
    st.subheader("8. 对其他请求有无异议")
    q8_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q8_options", horizontal=True)
    if q8_options == "无异议":
        q8_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q8_fact = st.text_area("事实和理由", key="q8_fact")
        q8_detail = f'无异议☐\n有异议☑ 事实和理由：{q8_fact}'
    thisCase.replay_matters.append(q8_detail)

    # 9. 对标的总额有无异议
    st.subheader("9. 对标的总额有无异议")
    q9_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="q9_options", horizontal=True)
    if q9_options == "无异议":
        q9_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        q9_fact = st.text_area("事实和理由", key="q9_fact")
        q9_detail = f'无异议☐\n有异议☑ 事实和理由：{q9_fact}'
    thisCase.replay_matters.append(q9_detail)

    # 10. 答辩依据
    st.subheader("10. 答辩依据")
    q10_1 = st.text_area("合同约定", key="q10_1")
    q10_2 = st.text_area("法律规定", key="q10_2")
    q10_detail = f'合同约定：{q10_1}\n法律规定：{q10_2}'
    thisCase.replay_matters.append(q10_detail)

def fact_reason(thisCase: dict):
    # 1. 对合同签订情况有无异议
    st.subheader("1. 对合同签订情况有无异议")
    f1_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f1_options", horizontal=True)
    if f1_options == "无异议":
        f1_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f1_fact = st.text_area("事实和理由", key="f1_fact")
        f1_detail = f'无异议☐\n有异议☑ 事实和理由：{f1_fact}'
    thisCase.reasons.append(f1_detail)

    # 2. 对签订主体有无异议
    st.subheader("2. 对签订主体有无异议")
    f2_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f2_options", horizontal=True)
    if f2_options == "无异议":
        f2_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f2_fact = st.text_area("事实和理由", key="f2_fact")
        f2_detail = f'无异议☐\n有异议☑ 事实和理由：{f2_fact}'
    thisCase.reasons.append(f2_detail)

    # 3. 对租赁物情况有无异议
    st.subheader("3. 对租赁物情况有无异议")
    f3_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f3_options", horizontal=True)
    if f3_options == "无异议":
        f3_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f3_fact = st.text_area("事实和理由", key="f3_fact")
        f3_detail = f'无异议☐\n有异议☑ 事实和理由：{f3_fact}'
    thisCase.reasons.append(f3_detail)

    # 4. 对合同约定的租金及支付方式有无异议
    st.subheader("4. 对合同约定的租金及支付方式有无异议")
    f4_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f4_options", horizontal=True)
    if f4_options == "无异议":
        f4_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f4_fact = st.text_area("事实和理由", key="f4_fact")
        f4_detail = f'无异议☐\n有异议☑ 事实和理由：{f4_fact}'
    thisCase.reasons.append(f4_detail)

    # 5. 对合同约定的租赁期限、费用有无异议
    st.subheader("5. 对合同约定的租赁期限、费用有无异议")
    f5_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f5_options", horizontal=True)
    if f5_options == "无异议":
        f5_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f5_fact = st.text_area("事实和理由", key="f5_fact")
        f5_detail = f'无异议☐\n有异议☑ 事实和理由：{f5_fact}'
    thisCase.reasons.append(f5_detail)

    # 6. 对到期后租赁物归属有无异议
    st.subheader("6. 对到期后租赁物归属有无异议")
    f6_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f6_options", horizontal=True)
    if f6_options == "无异议":
        f6_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f6_fact = st.text_area("事实和理由", key="f6_fact")
        f6_detail = f'无异议☐\n有异议☑ 事实和理由：{f6_fact}'
    thisCase.reasons.append(f6_detail)

    # 7. 对合同约定的违约责任有无异议
    st.subheader("7. 对合同约定的违约责任有无异议")
    f7_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f7_options", horizontal=True)
    if f7_options == "无异议":
        f7_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f7_fact = st.text_area("事实和理由", key="f7_fact")
        f7_detail = f'无异议☐\n有异议☑ 事实和理由：{f7_fact}'
    thisCase.reasons.append(f7_detail)

    # 8. 对是否约定加速到期条款有无异议
    st.subheader("8. 对是否约定加速到期条款有无异议")
    f8_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f8_options", horizontal=True)
    if f8_options == "无异议":
        f8_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f8_fact = st.text_area("事实和理由", key="f8_fact")
        f8_detail = f'无异议☐\n有异议☑ 事实和理由：{f8_fact}'
    thisCase.reasons.append(f8_detail)

    # 9. 对是否约定回收租赁物条件有无异议
    st.subheader("9. 对是否约定回收租赁物条件有无异议")
    f9_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f9_options", horizontal=True)
    if f9_options == "无异议":
        f9_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f9_fact = st.text_area("事实和理由", key="f9_fact")
        f9_detail = f'无异议☐\n有异议☑ 事实和理由：{f9_fact}'
    thisCase.reasons.append(f9_detail)

    # 10. 对是否约定解除合同条件有无异议
    st.subheader("10. 对是否约定解除合同条件有无异议")
    f10_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f10_options", horizontal=True)
    if f10_options == "无异议":
        f10_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f10_fact = st.text_area("事实和理由", key="f10_fact")
        f10_detail = f'无异议☐\n有异议☑ 事实和理由：{f10_fact}'
    thisCase.reasons.append(f10_detail)

    # 11. 对租赁物交付时间有无异议
    st.subheader("11. 对租赁物交付时间有无异议")
    f11_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f11_options", horizontal=True)
    if f11_options == "无异议":
        f11_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f11_fact = st.text_area("事实和理由", key="f11_fact")
        f11_detail = f'无异议☐\n有异议☑ 事实和理由：{f11_fact}'
    thisCase.reasons.append(f11_detail)

    # 12. 对租赁物情况有无异议
    st.subheader("12. 对租赁物情况有无异议")
    f12_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f12_options", horizontal=True)
    if f12_options == "无异议":
        f12_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f12_fact = st.text_area("事实和理由", key="f12_fact")
        f12_detail = f'无异议☐\n有异议☑ 事实和理由：{f12_fact}'
    thisCase.reasons.append(f12_detail)

    # 13. 对租金支付情况有无异议
    st.subheader("13. 对租金支付情况有无异议")
    f13_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f13_options", horizontal=True)
    if f13_options == "无异议":
        f13_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f13_fact = st.text_area("事实和理由", key="f13_fact")
        f13_detail = f'无异议☐\n有异议☑ 事实和理由：{f13_fact}'
    thisCase.reasons.append(f13_detail)

    # 14. 对逾期未付租金情况有无异议
    st.subheader("14. 对逾期未付租金情况有无异议")
    f14_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f14_options", horizontal=True)
    if f14_options == "无异议":
        f14_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f14_fact = st.text_area("事实和理由", key="f14_fact")
        f14_detail = f'无异议☐\n有异议☑ 事实和理由：{f14_fact}'
    thisCase.reasons.append(f14_detail)

    # 15. 对是否签订物的担保合同有无异议
    st.subheader("15. 对是否签订物的担保合同有无异议")
    f15_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f15_options", horizontal=True)
    if f15_options == "无异议":
        f15_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f15_fact = st.text_area("事实和理由", key="f15_fact")
        f15_detail = f'无异议☐\n有异议☑ 事实和理由：{f15_fact}'
    thisCase.reasons.append(f15_detail)

    # 16. 对担保人、担保物有无异议
    st.subheader("16. 对担保人、担保物有无异议")
    f16_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f16_options", horizontal=True)
    if f16_options == "无异议":
        f16_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f16_fact = st.text_area("事实和理由", key="f16_fact")
        f16_detail = f'无异议☐\n有异议☑ 事实和理由：{f16_fact}'
    thisCase.reasons.append(f16_detail)

    # 17. 对最高额抵押担保有无异议
    st.subheader("17. 对最高额抵押担保有无异议")
    f17_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f17_options", horizontal=True)
    if f17_options == "无异议":
        f17_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f17_fact = st.text_area("事实和理由", key="f17_fact")
        f17_detail = f'无异议☐\n有异议☑ 事实和理由：{f17_fact}'
    thisCase.reasons.append(f17_detail)

    # 18. 对是否办理抵押/质押登记有无异议
    st.subheader("18. 对是否办理抵押/质押登记有无异议")
    f18_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f18_options", horizontal=True)
    if f18_options == "无异议":
        f18_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f18_fact = st.text_area("事实和理由", key="f18_fact")
        f18_detail = f'无异议☐\n有异议☑ 事实和理由：{f18_fact}'
    thisCase.reasons.append(f18_detail)

    # 19. 对是否签订保证合同有无异议
    st.subheader("19. 对是否签订保证合同有无异议")
    f19_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f19_options", horizontal=True)
    if f19_options == "无异议":
        f19_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f19_fact = st.text_area("事实和理由", key="f19_fact")
        f19_detail = f'无异议☐\n有异议☑ 事实和理由：{f19_fact}'
    thisCase.reasons.append(f19_detail)

    # 20. 对保证方式有无异议
    st.subheader("20. 对保证方式有无异议")
    f20_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f20_options", horizontal=True)
    if f20_options == "无异议":
        f20_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f20_fact = st.text_area("事实和理由", key="f20_fact")
        f20_detail = f'无异议☐\n有异议☑ 事实和理由：{f20_fact}'
    thisCase.reasons.append(f20_detail)

    # 21. 对其他担保方式有无异议
    st.subheader("21. 对其他担保方式有无异议")
    f21_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无异议", "有异议"], key="f21_options", horizontal=True)
    if f21_options == "无异议":
        f21_detail = f'无异议☑\n有异议☐ 事实和理由：'
    else:
        f21_fact = st.text_area("事实和理由", key="f21_fact")
        f21_detail = f'无异议☐\n有异议☑ 事实和理由：{f21_fact}'
    thisCase.reasons.append(f21_detail)

    # 22. 有无其他免责/减责事由
    st.subheader("22. 有无其他免责/减责事由")
    f22_options = st.radio(
        label='No label', label_visibility='collapsed', options=["无", "有"], key="f22_options", horizontal=True)
    if f22_options == "无":
        f22_detail = f'无☑\n有☐ 事实和理由：'
    else:
        f22_fact = st.text_area("事实和理由", key="f22_fact")
        f22_detail = f'无☐\n有☑ 事实和理由：{f22_fact}'
    thisCase.reasons.append(f22_detail)

    # 23. 其他需要说明的内容
    st.subheader("23. 其他需要说明的内容")
    f23_content = st.text_area("其他内容", key="f23_content")
    thisCase.reasons.append(f23_content)

    # 24. 证据清单
    st.subheader("24. 证据清单")
    f24_content = st.text_area("证据清单", key="f24_content")
    thisCase.reasons.append(f24_content)

class FinancialLeaseCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE
    BaseCaseFormatter.isComplete = False

    @staticmethod
    def format_case(case):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(case.to_json())

        # 调用父类的通用格式化方法
        template_data = super(FinancialLeaseCaseFormatter,
                              FinancialLeaseCaseFormatter).format_case(case)

        # 添加案件的自定义部分
        template_data.update({
            "reply_matters": FinancialLeaseCaseFormatter._format_reply_matters(case_data)
        })
        template_data.update({"reasons": FinancialLeaseCaseFormatter._format_reasons(case_data)})

        return template_data

    @staticmethod
    def _format_reply_matters(case_data):
        """Format reply matters from the case data"""
        reply_matters = case_data.get('replay_matters', [])

        matter_types = [
            "1. 对支付全部未付租金的诉请有无异议",
            "2. 对违约金、滞纳金、损害赔偿金有无异议",
            "3. 对确认租赁物归原告所有有无异议",
            "4. 对解除合同有无异议",
            "5. 对返还租赁物，并赔偿因解除合同而受到的损失有无异议",
            "6. 对担保权利的诉请有无异议",
            "7. 对实现债权的费用有无异议",
            "8. 对其他请求有无异议",
            "9. 对标的总额有无异议",
            "10. 答辩依据"
        ]

        formatted_matters = []

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
        reasons = case_data.get('reasons', [])

        reason_types = [
            "1. 对合同签订情况有无异议",
            "2. 对签订主体有无异议",
            "3. 对租赁物情况有无异议",
            "4. 对合同约定的租金及支付方式有无异议",
            "5. 对合同约定的租赁期限、费用有无异议",
            "6. 对到期后租赁物归属有无异议",
            "7. 对合同约定的违约责任有无异议",
            "8. 对是否约定加速到期条款有无异议",
            "9. 对是否约定回收租赁物条件有无异议",
            "10. 对是否约定解除合同条件有无异议",
            "11. 对租赁物交付时间有无异议",
            "12. 对租赁物情况有无异议",
            "13. 对租金支付情况有无异议",
            "14. 对逾期未付租金情况有无异议",
            "15. 对是否签订物的担保合同有无异议",
            "16. 对担保人、担保物有无异议",
            "17. 对最高额抵押担保有无异议",
            "18. 对是否办理抵押/质押登记有无异议",
            "19. 对是否签订保证合同有无异议",
            "20. 对保证方式有无异议",
            "21. 对其他担保方式有无异议",
            "22. 有无其他免责/减责事由",
            "23. 其他需要说明的内容（可另附页）",
            "24. 证据清单（可另附页）"
        ]

        formatted_reasons = []

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

class FinancialLeaseCaseRespondent:
    def __init__(self):
        self.respondent = None
        self.case_num = None
        self.replay_matters = []
        self.reasons = []

    def to_json(self):
        def default_serializer(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            elif hasattr(obj, '__dict__'):
                return obj.__dict__
            elif isinstance(obj, pd.DataFrame):
                return obj.to_dict(orient='records')
            else:
                return str(obj)

        return json.dumps(self.__dict__, default=default_serializer, indent=4)

thisCase = FinancialLeaseCaseRespondent()

header(CASE_TYPE, "答辩状")

st.markdown("""______""")
st.subheader('案号')
thisCase.case_num = st.text_input(
    '请输入案号：', '', placeholder='示例：(2025)粤01民终0001号')
st.header("当事人信息")
respondent = Respondent(CASE_TYPE)
respondent.show()
thisCase.respondent = respondent
st.markdown("""______""")
st.header("答辩事项和依据（对原告诉讼请求的确认或者异议）")
respondent_details(thisCase)
st.header("事实和理由（对起诉状事实与理由的确认或者异议）")
fact_reason(thisCase)

if st.button("生成答辩状"):
    st.write("案件信息（JSON 格式）:")
    st.json(thisCase.to_json())
    print(thisCase.to_json())

    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "defense",
                thisCase,
                FinancialLeaseCaseFormatter,
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