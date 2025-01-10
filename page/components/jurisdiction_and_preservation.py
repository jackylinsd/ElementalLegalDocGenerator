import streamlit as st

class JurisdictionAndPreservation:
    def __init__(self):
        self.arbitration_agreement = None  # 仲裁/法院管辖约定
        self.arbitration_details = None    # 合同条款及内容
        self.pre_preservation = None       # 诉前保全
        self.pre_preservation_court = None # 诉前保全法院
        self.pre_preservation_time = None  # 诉前保全时间
        self.litigation_preservation = None  # 诉讼保全
        self.litigation_preservation_request = None  # 诉讼保全申请内容

    def show(self):
        st.subheader("仲裁/法院管辖约定")
        self.arbitration_agreement = st.radio(
            "有无仲裁、法院管辖约定", ["无", "有"], key="arbitration_agreement")
        if self.arbitration_agreement == "有":
            self.arbitration_details = st.text_area(
                "合同条款及内容", key="arbitration_details", placeholder="请输入合同条款及内容")
        else:
            self.arbitration_details = ""

        # 诉前保全
        st.subheader("诉前保全")
        self.pre_preservation = st.radio(
            "是否申请诉前保全", ["否", "是"], key="pre_preservation")
        if self.pre_preservation == "是":
            self.pre_preservation_court = st.text_input(
                "诉前保全法院", key="pre_preservation_court", placeholder="请输入诉前保全法院")
            self.pre_preservation_time = st.date_input(
                "诉前保全时间", key="pre_preservation_time")
        else:
            self.pre_preservation_court = ""
            self.pre_preservation_time = ""

        # 诉讼保全
        st.subheader("诉讼保全")
        self.litigation_preservation = st.radio(
            "是否申请诉讼保全", ["否", "是"], key="litigation_preservation")
        if self.litigation_preservation == "是":
            self.litigation_preservation_request = st.text_area(
                "诉讼保全申请内容", key="litigation_preservation_request", placeholder="请输入诉讼保全申请内容")
        else:
            self.litigation_preservation_request = ""