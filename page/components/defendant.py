import streamlit as st
from utils.type import *

class Respondent:
    def __init__(self, case_type):
        if case_type not in CASE_CATEGORIES:
            raise ValueError("Invalid case type")
        self.case_type = case_type
        self.respondents = []  # 保持列表结构，但只存储一个答辩人
        self.agents = []  # 存储所有委托诉讼代理人信息
        self.delivery_info = {}  # 存储送达地址信息
        self.electronic_delivery_info = {}  # 存储电子送达信息

    def _respondent_people_info(self):
        """生成自然人答辩人的输入组件"""
        st.subheader("答辩人（自然人）") if self.case_type not in CASE_COMPLAINT_RESPONDENTS_NO_NP else st.subheader("答辩人")

        respondent = {
            "name": st.text_input("姓名", key="respondent_people_name", placeholder="请输入答辩人姓名"),
            "gender": st.radio("性别", ["男", "女"], key="respondent_people_gender", horizontal=True),
            "dob": st.date_input("出生日期", key="respondent_people_dob"),
            "nationality": st.text_input("民族", key="respondent_people_nationality", placeholder="请输入民族"),
            "employer": st.text_input("工作单位", key="respondent_people_employer", placeholder="请输入工作单位"),
            "position": st.text_input("职务", key="respondent_people_position", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key="respondent_people_phone", placeholder="请输入联系电话"),
            "address": st.text_input("住所地（户籍所在地）", key="respondent_people_address", placeholder="请输入户籍所在地"),
            "residence": st.text_input("经常居住地", key="respondent_people_residence", placeholder="请输入经常居住地"),
        }
        self.respondents = [respondent]  # 直接替换列表内容

    def _respondent_company_info(self):
        """生成法人/非法人组织答辩人的输入组件"""
        st.subheader("答辩人（法人、非法人组织）")

        respondent = {
            "name": st.text_input("名称", key="respondent_company_name", placeholder="请输入答辩人名称"),
            "address": st.text_input("住所地（主要办事机构所在地）", key="respondent_company_address", placeholder="请输入主要办事机构所在地"),
            "registered_address": st.text_input("注册地/登记地", key="respondent_company_registered_address", placeholder="请输入注册地/登记地"),
            "legal_representative": st.text_input("法定代表人/主要负责人", key="respondent_company_legal_representative", placeholder="请输入法定代表人/主要负责人"),
            "position": st.text_input("职务", key="respondent_company_position", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key="respondent_company_phone", placeholder="请输入联系电话"),
            "unified_code": st.text_input("统一社会信用代码", key="respondent_company_unified_code", placeholder="请输入统一社会信用代码"),
            "type": st.selectbox("类型", ["有限责任公司", "股份有限公司", "上市公司", "其他企业法人", "事业单位", "社会团体", "基金会", "社会服务机构", "机关法人", "农村集体经济组织法人", "城镇农村的合作经济组织法人", "基层群众性自治组织法人", "个人独资企业", "合伙企业", "不具有法人资格的专业服务机构"], key="respondent_company_type"),
            "ownership": st.radio("所有制", ["民营", "国有(控股)", "国有(参股)"], key="respondent_company_ownership", horizontal=True),
        }
        self.respondents = [respondent]  # 直接替换列表内容

    def _representative(self):
        """生成委托诉讼代理人的输入组件"""
        st.subheader("委托诉讼代理人")
        has_agent = st.checkbox("是否有委托诉讼代理人", key="has_agent")
        if has_agent:
            num_agents = st.number_input("委托诉讼代理人数量", min_value=1, max_value=2, value=1, step=1)

            for i in range(num_agents):
                st.subheader(f"委托诉讼代理人 {i + 1}")
                agent = {
                    "name": st.text_input(f"姓名", key=f"agent_name_{i}"),
                    "employer": st.text_input(f"单位", key=f"agent_employer_{i}"),
                    "position": st.text_input(f"职务", key=f"agent_position_{i}"),
                    "phone": st.text_input(f"联系电话", key=f"agent_phone_{i}"),
                    "authority": st.radio(f"代理权限", ["一般授权", "特别授权"], key=f"agent_authority_{i}", horizontal=True),
                }
                self.agents.append(agent)

    def _service_address(self):
        """生成送达地址的输入组件"""
        st.subheader("送达地址（所填信息除书面特别声明更改外，适用于案件一审、二审、再审所有后续程序）及收件人、电话")
        self.delivery_info['address'] = st.text_input("地址", key="delivery_address", placeholder="请输入送达地址")
        self.delivery_info['recipient'] = st.text_input("收件人", key="recipient", placeholder="请输入收件人姓名")
        self.delivery_info['recipient_phone'] = st.text_input("电话", key="recipient_phone", placeholder="请输入收件人电话")

    def _e_service(self):
        """生成电子送达的输入组件"""
        st.subheader("是否接受电子送达")
        accept_electronic_delivery = st.checkbox("是否接受电子送达", key="accept_electronic_delivery")
        if accept_electronic_delivery:
            self.electronic_delivery_info['SMS'] = st.text_input("短信", key="delivery_methods_SMS")
            self.electronic_delivery_info['wechat'] = st.text_input("微信", key="delivery_methods_wechat")
            self.electronic_delivery_info['fax'] = st.text_input("传真", key="delivery_methods_fax")
            self.electronic_delivery_info['email'] = st.text_input("邮箱", key="delivery_methods_email")
            self.electronic_delivery_info['other'] = st.text_input("其他", key="delivery_methods_other")

    def show(self):
        """显示答辩人信息输入组件"""
        if self.case_type in CASE_COMPLAINT_RESPONDENTS_NO_NP:
            self._respondent_people_info()
        elif self.case_type in CASE_COMPLAINT_RESPONDENTS_COMPANY:
            self._respondent_company_info()
        elif self.case_type in CASE_COMPLAINT_RESPONDENTS_BOTH:
            respondent_type = st.radio("答辩人类型", ["自然人", "法人/非法人组织"], key="respondent_type", horizontal=True)
            if respondent_type == "自然人":
                self._respondent_people_info()
            else:
                self._respondent_company_info()

        self._representative()
        self._service_address()
        self._e_service()

    def get_respondents(self):
        """获取所有答辩人信息"""
        return self.respondents

    def get_agents(self):
        """获取所有委托诉讼代理人信息"""
        return self.agents

    def get_delivery_info(self):
        """获取送达地址信息"""
        return self.delivery_info

    def get_electronic_delivery_info(self):
        """获取电子送达信息"""
        return self.electronic_delivery_info