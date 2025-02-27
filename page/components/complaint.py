# pages/components/complaint.py
import streamlit as st
from utils.type import *
from utils.tools import st_date_input

class Plaintiff:
    def __init__(self, case_type):
        if case_type not in CASE_CATEGORIES:
            raise ValueError("Invalid case type")
        self.case_type = case_type
        self.plaintiffs = []  # 存储所有原告的信息
        self.agents = []  # 存储所有委托诉讼代理人信息
        self.delivery_info = {}  # 存储送达地址信息
        self.electronic_delivery_info = {}  # 存储电子送达信息

    def _plaintiff_people_info(self, index, total_plaintiffs):
        """生成单个自然人原告的输入组件"""
        if total_plaintiffs == 1:
            st.subheader("原告（自然人）") if self.case_type not in CASE_COMPLAINT_PLAINTIFFS_NO_NP else st.subheader("原告")
        else:
            st.subheader(f"原告 {index + 1}（自然人）") if self.case_type not in CASE_COMPLAINT_PLAINTIFFS_NO_NP else st.subheader(f"原告  {index + 1}")

        plaintiff = {
            "name": st.text_input("姓名", key=f"plaintiff_people_name_{index}", placeholder="请输入原告姓名"),
            "gender": st.radio("性别", ["男", "女"], key=f"plaintiff_people_gender_{index}", horizontal=True),
            "dob": st_date_input("出生日期", key=f"plaintiff_people_dob_{index}", value='1949-01-01',min_value='1900-01-01',max_value='today'),
            "nationality": st.text_input("民族", key=f"plaintiff_people_nationality_{index}", placeholder="请输入民族"),
            "employer": st.text_input("工作单位", key=f"plaintiff_people_employer_{index}", placeholder="请输入工作单位"),
            "position": st.text_input("职务", key=f"plaintiff_people_position_{index}", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key=f"plaintiff_people_phone_{index}", placeholder="请输入联系电话"),
            "address": st.text_input("住所地（户籍所在地）", key=f"plaintiff_people_address_{index}", placeholder="请输入户籍所在地"),
            "residence": st.text_input("经常居住地", key=f"plaintiff_people_residence_{index}", placeholder="请输入经常居住地"),
        }
        self.plaintiffs.append(plaintiff)

    def _plaintiff_company_info(self, index, total_plaintiffs):
        """生成单个法人/非法人组织原告的输入组件"""
        if total_plaintiffs == 1:
            st.subheader("原告（法人、非法人组织）")
        else:
            st.subheader(f"原告 {index + 1}（法人、非法人组织）")

        plaintiff = {
            "name": st.text_input("名称", key=f"plaintiff_company_name_{index}", placeholder="请输入原告名称"),
            "address": st.text_input("住所地（主要办事机构所在地）", key=f"plaintiff_company_address_{index}", placeholder="请输入主要办事机构所在地"),
            "registered_address": st.text_input("注册地/登记地", key=f"plaintiff_company_registered_address_{index}", placeholder="请输入注册地/登记地"),
            "legal_representative": st.text_input("法定代表人/主要负责人", key=f"plaintiff_company_legal_representative_{index}", placeholder="请输入法定代表人/主要负责人"),
            "position": st.text_input("职务", key=f"plaintiff_company_position_{index}", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key=f"plaintiff_company_phone_{index}", placeholder="请输入联系电话"),
            "unified_code": st.text_input("统一社会信用代码", key=f"plaintiff_company_unified_code_{index}", placeholder="请输入统一社会信用代码"),
            "type": st.selectbox("类型", ["有限责任公司", "股份有限公司", "上市公司", "其他企业法人", "事业单位", "社会团体", "基金会", "社会服务机构", "机关法人", "农村集体经济组织法人", "城镇农村的合作经济组织法人", "基层群众性自治组织法人", "个人独资企业", "合伙企业", "不具有法人资格的专业服务机构"], key=f"plaintiff_company_type_{index}"),
            "ownership": st.radio("所有制", ["民营", "国有(控股)", "国有(参股)"], key=f"plaintiff_company_ownership_{index}", horizontal=True),
        }
        self.plaintiffs.append(plaintiff)

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
        """根据案件类型生成输入组件"""
        num_plaintiffs = st.number_input("原告数量", min_value=1, max_value=10, value=1, step=1, key="num_plaintiffs")

        for i in range(num_plaintiffs):
            if self.case_type in CASE_COMPLAINT_PLAINTIFFS_NO_NP:
                self._plaintiff_people_info(i, num_plaintiffs)
            elif self.case_type in CASE_COMPLAINT_PLAINTIFFS_COMPANY:
                self._plaintiff_company_info(i, num_plaintiffs)
            elif self.case_type in CASE_COMPLAINT_PLAINTIFFS_BOTH:
                plaintiff_type = st.radio(f"原告 {i + 1} 类型", ["自然人", "法人/非法人组织"], key=f"plaintiff_type_{i}", horizontal=True)
                if plaintiff_type == "自然人":
                    self._plaintiff_people_info(i, num_plaintiffs)
                else:
                    self._plaintiff_company_info(i, num_plaintiffs)

        self._representative()
        self._service_address()
        self._e_service()

    def get_plaintiffs(self):
        """获取所有原告信息"""
        return self.plaintiffs

    def get_agents(self):
        """获取所有委托诉讼代理人信息"""
        return self.agents

    def get_delivery_info(self):
        """获取送达地址信息"""
        return self.delivery_info

    def get_electronic_delivery_info(self):
        """获取电子送达信息"""
        return self.electronic_delivery_info
    

class Defendant:
    def __init__(self, case_type):
        if case_type not in CASE_CATEGORIES:
            raise ValueError("Invalid case type")
        self.case_type = case_type
        self.defendants = []  # 存储所有被告的信息

    def _defendant_people_info(self, index, total_defendants):
        """生成单个自然人被告的输入组件"""
        if total_defendants == 1:
            st.subheader("被告（自然人）") if self.case_type not in CASE_COMPLAINT_DEFENDANT_NO_NP else st.subheader("被告")
        else:
            st.subheader(f"被告 {index + 1}（自然人）") if self.case_type not in CASE_COMPLAINT_DEFENDANT_NO_NP else st.subheader(f"被告 {index + 1}")

        defendant = {
            "name": st.text_input("姓名", key=f"defendant_people_name_{index}", placeholder="请输入被告姓名"),
            "gender": st.radio("性别", ["男", "女"], key=f"defendant_people_gender_{index}", horizontal=True),
            "dob": st_date_input("出生日期", key=f"defendant_people_dob_{index}", value='1949-01-01',min_value='1900-01-01',max_value='today'),
            "nationality": st.text_input("民族", key=f"defendant_people_nationality_{index}", placeholder="请输入民族"),
            "employer": st.text_input("工作单位", key=f"defendant_people_employer_{index}", placeholder="请输入工作单位"),
            "position": st.text_input("职务", key=f"defendant_people_position_{index}", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key=f"defendant_people_phone_{index}", placeholder="请输入联系电话"),
            "address": st.text_input("住所地（户籍所在地）", key=f"defendant_people_address_{index}", placeholder="请输入户籍所在地"),
            "residence": st.text_input("经常居住地", key=f"defendant_people_residence_{index}", placeholder="请输入经常居住地"),
        }
        self.defendants.append(defendant)

    def _defendant_company_info(self, index, total_defendants):
        """生成单个法人/非法人组织被告的输入组件"""
        if total_defendants == 1:
            st.subheader("被告（法人、非法人组织）") if self.case_type not in CASE_SPECIAL_DEFENDANT_COMPANY_TYPE else st.subheader(CASE_SPECIAL_DEFENDANT_COMPANY_TYPE[self.case_type])
        else:
            st.subheader(f"被告 {index + 1}（法人、非法人组织）") if self.case_type not in CASE_SPECIAL_DEFENDANT_COMPANY_TYPE else st.subheader(CASE_SPECIAL_DEFENDANT_COMPANY_TYPE[self.case_type])

        defendant = {
            "name": st.text_input("名称", key=f"defendant_company_name_{index}", placeholder="请输入被告名称"),
            "address": st.text_input("住所地（主要办事机构所在地）", key=f"defendant_company_address_{index}", placeholder="请输入主要办事机构所在地"),
            "registered_address": st.text_input("注册地/登记地", key=f"defendant_company_registered_address_{index}", placeholder="请输入注册地/登记地"),
            "legal_representative": st.text_input("法定代表人/主要负责人", key=f"defendant_company_legal_representative_{index}", placeholder="请输入法定代表人/主要负责人"),
            "position": st.text_input("职务", key=f"defendant_company_position_{index}", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key=f"defendant_company_phone_{index}", placeholder="请输入联系电话"),
            "unified_code": st.text_input("统一社会信用代码", key=f"defendant_company_unified_code_{index}", placeholder="请输入统一社会信用代码"),
            "type": st.selectbox("类型", ["有限责任公司", "股份有限公司", "上市公司", "其他企业法人", "事业单位", "社会团体", "基金会", "社会服务机构", "机关法人", "农村集体经济组织法人", "城镇农村的合作经济组织法人", "基层群众性自治组织法人", "个人独资企业", "合伙企业", "不具有法人资格的专业服务机构"], key=f"defendant_company_type_{index}"),
            "ownership": st.radio("所有制", ["民营", "国有(控股)", "国有(参股)"], key=f"defendant_company_ownership_{index}", horizontal=True),
        }
        self.defendants.append(defendant)

    def show(self):
        """生成被告的输入组件"""
        num_defendants = st.number_input("被告数量", min_value=1, max_value=10, value=1, step=1, key="num_defendants")
        for i in range(num_defendants):
            if self.case_type in CASE_COMPLAINT_DEFENDANT_NO_NP:
                self._defendant_people_info(i, num_defendants)
            # elif self.case_type in CASE_SPECIAL_DEFENDANT_COMPANY_TYPE:
            #     self._defendant_company_info(i, num_defendants)
            else:
                defendant_type = st.radio(f"被告 {i + 1} 类型", ["自然人", "法人/非法人组织"], key=f"defendant_type_{i}", horizontal=True)
                if defendant_type == "自然人":
                    self._defendant_people_info(i, num_defendants)
                else:
                    self._defendant_company_info(i, num_defendants)

    def get_defendants(self):
        """获取所有被告信息"""
        return self.defendants

class ThirdParty:
    def __init__(self):
        self.third_parties = []  # 存储所有第三人的信息

    def _third_party_people_info(self, index, total_third_parties):
        """生成单个自然人第三人的输入组件"""
        if total_third_parties == 1:
            st.subheader("第三人（自然人）")
        else:
            st.subheader(f"第三人 {index + 1}（自然人）")

        third_party = {
            "name": st.text_input("姓名", key=f"third_party_people_name_{index}", placeholder="请输入第三人姓名"),
            "gender": st.radio("性别", ["男", "女"], key=f"third_party_people_gender_{index}", horizontal=True),
            "dob": st_date_input("出生日期", key=f"third_party_people_dob_{index}", value='1949-01-01',min_value='1900-01-01',max_value='today'),
            "nationality": st.text_input("民族", key=f"third_party_people_nationality_{index}", placeholder="请输入民族"),
            "employer": st.text_input("工作单位", key=f"third_party_people_employer_{index}", placeholder="请输入工作单位"),
            "position": st.text_input("职务", key=f"third_party_people_position_{index}", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key=f"third_party_people_phone_{index}", placeholder="请输入联系电话"),
            "address": st.text_input("住所地（户籍所在地）", key=f"third_party_people_address_{index}", placeholder="请输入户籍所在地"),
            "residence": st.text_input("经常居住地", key=f"third_party_people_residence_{index}", placeholder="请输入经常居住地"),
        }
        self.third_parties.append(third_party)

    def _third_party_company_info(self, index, total_third_parties):
        """生成单个法人/非法人组织第三人的输入组件"""
        if total_third_parties == 1:
            st.subheader("第三人（法人、非法人组织）")
        else:
            st.subheader(f"第三人 {index + 1}（法人、非法人组织）")

        third_party = {
            "name": st.text_input("名称", key=f"third_party_company_name_{index}", placeholder="请输入第三人名称"),
            "address": st.text_input("住所地（主要办事机构所在地）", key=f"third_party_company_address_{index}", placeholder="请输入主要办事机构所在地"),
            "registered_address": st.text_input("注册地/登记地", key=f"third_party_company_registered_address_{index}", placeholder="请输入注册地/登记地"),
            "legal_representative": st.text_input("法定代表人/主要负责人", key=f"third_party_company_legal_representative_{index}", placeholder="请输入法定代表人/主要负责人"),
            "position": st.text_input("职务", key=f"third_party_company_position_{index}", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key=f"third_party_company_phone_{index}", placeholder="请输入联系电话"),
            "unified_code": st.text_input("统一社会信用代码", key=f"third_party_company_unified_code_{index}", placeholder="请输入统一社会信用代码"),
            "type": st.selectbox("类型", ["有限责任公司", "股份有限公司", "上市公司", "其他企业法人", "事业单位", "社会团体", "基金会", "社会服务机构", "机关法人", "农村集体经济组织法人", "城镇农村的合作经济组织法人", "基层群众性自治组织法人", "个人独资企业", "合伙企业", "不具有法人资格的专业服务机构"], key=f"third_party_company_type_{index}"),
            "ownership": st.radio("所有制", ["民营", "国有(控股)", "国有(参股)"], key=f"third_party_company_ownership_{index}", horizontal=True),
        }
        self.third_parties.append(third_party)

    def show(self):
        """生成第三人的输入组件"""
        num_third_parties = st.number_input("第三人数量", min_value=1, max_value=10, value=1, step=1, key="num_third_parties")

        for i in range(num_third_parties):
            third_party_type = st.radio(f"第三人 {i + 1} 类型", ["自然人", "法人/非法人组织"], key=f"third_party_type_{i}", horizontal=True)
            if third_party_type == "自然人":
                self._third_party_people_info(i, num_third_parties)
            else:
                self._third_party_company_info(i, num_third_parties)

    def get_third_parties(self):
        """获取所有第三人信息"""
        return self.third_parties
    def __init__(self):
        self.third_parties = []  # 存储所有第三人的信息

    def _third_party_people_info(self, index, total_third_parties):
        """生成单个自然人第三人的输入组件"""
        if total_third_parties == 1:
            st.subheader("第三人（自然人）")
        else:
            st.subheader(f"第三人 {index + 1}（自然人）")

        third_party = {
            "name": st.text_input("姓名", key=f"third_party_people_name_{index}", placeholder="请输入第三人姓名"),
            "gender": st.radio("性别", ["男", "女"], key=f"third_party_people_gender_{index}", horizontal=True),
            "dob": st_date_input("出生日期", key=f"third_party_people_dob_{index}", value='1949-01-01',min_value='1900-01-01',max_value='today'),
            "nationality": st.text_input("民族", key=f"third_party_people_nationality_{index}", placeholder="请输入民族"),
            "employer": st.text_input("工作单位", key=f"third_party_people_employer_{index}", placeholder="请输入工作单位"),
            "position": st.text_input("职务", key=f"third_party_people_position_{index}", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key=f"third_party_people_phone_{index}", placeholder="请输入联系电话"),
            "address": st.text_input("住所地（户籍所在地）", key=f"third_party_people_address_{index}", placeholder="请输入户籍所在地"),
            "residence": st.text_input("经常居住地", key=f"third_party_people_residence_{index}", placeholder="请输入经常居住地"),
        }
        self.third_parties.append(third_party)

    def _third_party_company_info(self, index, total_third_parties):
        """生成单个法人/非法人组织第三人的输入组件"""
        if total_third_parties == 1:
            st.subheader("第三人（法人、非法人组织）")
        else:
            st.subheader(f"第三人 {index + 1}（法人、非法人组织）")

        third_party = {
            "name": st.text_input("名称", key=f"third_party_company_name_{index}", placeholder="请输入第三人名称"),
            "address": st.text_input("住所地（主要办事机构所在地）", key=f"third_party_company_address_{index}", placeholder="请输入主要办事机构所在地"),
            "registered_address": st.text_input("注册地/登记地", key=f"third_party_company_registered_address_{index}", placeholder="请输入注册地/登记地"),
            "legal_representative": st.text_input("法定代表人/主要负责人", key=f"third_party_company_legal_representative_{index}", placeholder="请输入法定代表人/主要负责人"),
            "position": st.text_input("职务", key=f"third_party_company_position_{index}", placeholder="请输入职务"),
            "phone": st.text_input("联系电话", key=f"third_party_company_phone_{index}", placeholder="请输入联系电话"),
            "unified_code": st.text_input("统一社会信用代码", key=f"third_party_company_unified_code_{index}", placeholder="请输入统一社会信用代码"),
            "type": st.selectbox("类型", ["有限责任公司", "股份有限公司", "上市公司", "其他企业法人", "事业单位", "社会团体", "基金会", "社会服务机构", "机关法人", "农村集体经济组织法人", "城镇农村的合作经济组织法人", "基层群众性自治组织法人", "个人独资企业", "合伙企业", "不具有法人资格的专业服务机构"], key=f"third_party_company_type_{index}"),
            "ownership": st.radio("所有制", ["民营", "国有(控股)", "国有(参股)"], key=f"third_party_company_ownership_{index}", horizontal=True),
        }
        self.third_parties.append(third_party)

    def show(self):
        """生成第三人的输入组件"""
        num_third_parties = st.number_input("第三人数量", min_value=1, max_value=10, value=1, step=1, key="num_third_parties")

        for i in range(num_third_parties):
            third_party_type = st.radio(f"第三人 {i + 1} 类型", ["自然人", "法人/非法人组织"], key=f"third_party_type_{i}", horizontal=True)
            if third_party_type == "自然人":
                self._third_party_people_info(i, num_third_parties)
            else:
                self._third_party_company_info(i, num_third_parties)

    def get_third_parties(self):
        """获取所有第三人信息"""
        return self.third_parties