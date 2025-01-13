import streamlit as st
import json
from datetime import date
import pandas as pd
from page.components.jurisdiction_and_preservation import JurisdictionAndPreservation


class CommonCasePlaintiff:
    """案件信息类
    plaintiff: 原告信息
    defendant: 被告信息
    third_party: 第三人信息
    jurisdiction_and_preservation: 约定管辖和诉讼保全信息
    reply_matters: 诉讼请求和依据
    reasons: 事由
    """


    def __init__(self):
        self.plaintiff = None
        self.defendant = None
        self.third_party = None
        self.jurisdiction_and_preservation = JurisdictionAndPreservation()
        self.reply_matters = []
        self.reasons = []

    def to_json(self):
        """序列化对象到JSON"""

        def default_serializer(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            elif isinstance(obj, pd.DataFrame):
                return obj.to_dict(orient="records")
            elif hasattr(obj, "__dict__"):
                return obj.__dict__
            return str(obj)

        return json.dumps(self.__dict__, default=default_serializer, indent=4)





class CommonCaseRespondent:
    """案件信息类"""

    def __init__(self):
        self.respondent = None
        self.reply_matters = []
        self.reasons = []

    def to_json(self):
        """序列化对象到JSON"""

        def default_serializer(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            elif isinstance(obj, pd.DataFrame):
                return obj.to_dict(orient="records")
            elif hasattr(obj, "__dict__"):
                return obj.__dict__
            return str(obj)

        return json.dumps(self.__dict__, default=default_serializer, indent=4)


def create_radio_section(title, key_prefix, target_list, options=["无", "有"]):
    """通用的单选项创建函数"""
    st.subheader(title)
    option = st.radio(
        "",
        options,
        key=f"{key_prefix}_options",
        horizontal=True,
        label_visibility="collapsed",
    )

    if option == options[0]:
        detail = f"{options[0]}☑\n{options[1]}☐ 事实和理由："
    else:
        fact = st.text_area("事实和理由", key=f"{key_prefix}_fact")
        detail = f"{options[0]}☐\n{options[1]}☑ 事实和理由：{fact}"

    target_list.append(detail)


def create_text_section(title, key, target_list):
    """通用的文本输入部分创建函数"""
    st.subheader(title)
    content = st.text_area("", key=key)
    target_list.append(content)
