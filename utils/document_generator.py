from docxtpl import DocxTemplate
from datetime import datetime
import io
import os
import json
from typing import Protocol, Any
import logging
from utils.type import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BaseCaseFormatter:
    """通用案件数据格式化器，用于将案件数据转换为文档模板格式"""

    case_type = "通用案件"
    isComplaint = True

    @staticmethod
    def format_case(case):
        """将案件对象转换为适合文档模板的格式"""
        try:
            case_data = json.loads(case.to_json())

            # 添加安全的数据访问方法
            def safe_get(data, *keys, default=""):
                """安全地获取嵌套字典中的值"""
                current = data
                for key in keys:
                    if not isinstance(current, dict):
                        return default
                    current = current.get(key, default)
                    if current is None:
                        return default
                return current

            # 通用部分
            template_data = {
                "case_type": BaseCaseFormatter.case_type,
                "date": datetime.now().strftime("%Y年%m月%d日"),
                "party_informations": BaseCaseFormatter._format_party_informations(case_data),
                "competent_preservation": BaseCaseFormatter._format_competent_preservation(case_data),
                "agents": BaseCaseFormatter._format_agents(case_data),  # 委托代理人
                # 送达地址
                "delivery_info": BaseCaseFormatter._format_delivery_info(case_data),
                # 是否接受电子送达
                "electronic_delivery": BaseCaseFormatter._format_electronic_delivery(case_data),
            }

            return template_data

        except Exception as e:
            logger.error(f"BaseCaseFormatter格式化案件数据时出错: {str(e)}")
            raise ValueError(f"BaseCaseFormatter格式化案件数据失败: {str(e)}")

    @staticmethod
    def _format_party_informations(case_data):
        """格式化当事人信息（通用部分）"""
        party_informations = []
        plaintiff_case_type = case_data.get(
            "plaintiff", {}).get("case_type", {})
        is_plaintiff_both = True if plaintiff_case_type in CASE_COMPLAINT_PLAINTIFFS_BOTH else False
        respondent_case_type = case_data.get(
            "respondent", {}).get("case_type", {})
        is_respondent_both = True if respondent_case_type in CASE_COMPLAINT_RESPONDENTS_BOTH else False

        is_third_party = True if plaintiff_case_type not in CASE_COMPLAINT_PLAINTIFFS_NO_TP else False

        if BaseCaseFormatter.isComplaint:
            # 原告部分
            party_informations.append({
                "type": "原告" if plaintiff_case_type in CASE_COMPLAINT_DEFENDANT_NO_NP else "原告(自然人)",
                "information": BaseCaseFormatter._format_party_info(case_data.get("plaintiff", {}))
            })

            # 如果 case_type 是原告（法人、非法人组织），插入法人信息
            if is_plaintiff_both:
                party_informations.append({
                    "type": "原告（法人、非法人组织）" if plaintiff_case_type not in CASE_SPECIAL_DEFENDANT_COMPANY_TYPE
                    else CASE_SPECIAL_DEFENDANT_COMPANY_TYPE[plaintiff_case_type],
                    "information": BaseCaseFormatter._format_company_info(case_data.get("plaintiff", {}))
                })

            # 委托诉讼代理人
            party_informations.append({
                "type": "委托诉讼代理人",
                "information": BaseCaseFormatter._format_agents(case_data.get("plaintiff", {}))
            })

            # 送达地址及电子送达
            party_informations.append({
                "type": "送达地址（所填信息除书面特别声明更改外，适用于案件一审、二审、再审所有后续程序）及收件人、电话",
                "information": BaseCaseFormatter._format_delivery_info(case_data.get("plaintiff", {}))
            })
            party_informations.append({
                "type": "是否接受电子送达",
                "information": BaseCaseFormatter._format_electronic_delivery(case_data.get("plaintiff", {}))
            })

            # 被告部分
            party_informations.append({
                "type": "被告",
                "information": BaseCaseFormatter._format_party_info(case_data.get("defendant", {}))
            })

            if is_third_party:
                # 第三人部分
                party_informations.append({
                    "type": "第三人（法人、非法人组织）",
                    "information": BaseCaseFormatter._format_company_info(case_data.get("third_party", {})) 
                })

                party_informations.append({
                    "type": "第三人（自然人）",
                    "information": BaseCaseFormatter._format_party_info(case_data.get("third_party", {}))
                })

        else:
            # 答辩人部分
            party_informations.append({
                "type": "答辩人" if respondent_case_type in CASE_COMPLAINT_RESPONDENTS_NO_NP else "答辩人(自然人)",
                "information": BaseCaseFormatter._format_party_info(case_data.get("respondent", {}))
            })

            # 如果 case_type 是答辩人（法人、非法人组织），插入法人信息
            if is_respondent_both:
                party_informations.append({
                    "type": "答辩人（法人、非法人组织）" if respondent_case_type not in CASE_SPECIAL_RESPONDENTS_COMPANY_TYPE
                    else CASE_SPECIAL_RESPONDENTS_COMPANY_TYPE[respondent_case_type],
                    "information": BaseCaseFormatter._format_company_info(case_data.get("respondent", {}))
                })

            # 委托诉讼代理人
            party_informations.append({
                "type": "委托诉讼代理人",
                "information": BaseCaseFormatter._format_agents(case_data.get("respondent", {}))
            })

            # 送达地址及电子送达
            party_informations.append({
                "type": "送达地址（所填信息除书面特别声明更改外，适用于案件一审、二审、再审所有后续程序）及收件人、电话",
                "information": BaseCaseFormatter._format_delivery_info(case_data.get("respondent", {}))
            })
            party_informations.append({
                "type": "是否接受电子送达",
                "information": BaseCaseFormatter._format_electronic_delivery(case_data.get("respondent", {}))
            })

        return party_informations

    @staticmethod
    def _format_competent_preservation(case_data):
        """格式化约定管辖和诉讼保全信息（通用部分）"""
        jurisdiction_info_agreement = case_data.get(
            "jurisdiction_and_preservation", {}).get("arbitration_agreement", "")
        jurisdiction_info_details = case_data.get(
            "jurisdiction_and_preservation", {}).get("arbitration_details", "")
        format_jurisdiction_info = ''
        if jurisdiction_info_agreement == "有":
            format_jurisdiction_info = f'有☑\n合同条款及内容：\n{
                jurisdiction_info_details}\n无☐'
        else:
            format_jurisdiction_info = f'有☐\n合同条款及内容：\n无☑'

        preservation_info_pre_preservation = case_data.get(
            "jurisdiction_and_preservation", {}).get("pre_preservation", "")
        preservation_info_pre_preservation_court = case_data.get(
            "jurisdiction_and_preservation", {}).get("pre_preservation_court", "")
        preservation_info_pre_preservation_time = case_data.get(
            "jurisdiction_and_preservation", {}).get("pre_preservation_time", "")
        preservation_info_litigation_preservation = case_data.get(
            "jurisdiction_and_preservation", {}).get("litigation_preservation", "")
        preservation_info_litigation_preservation_request = case_data.get(
            "jurisdiction_and_preservation", {}).get("litigation_preservation_request", "")

        format_pre_preservation_info = ''
        if preservation_info_pre_preservation == '是':
            format_pre_preservation_info = f'已经诉前保全：是☑\n保全法院：{
                preservation_info_pre_preservation_court}\n保全时间：{preservation_info_pre_preservation_time}\n否☐\n'
        else:
            format_pre_preservation_info = f'已经诉前保全：是☐\n保全法院：\n保全时间：\n否☑\n'
        format_litigation_preservation_info = ''
        if preservation_info_litigation_preservation == '是':
            format_litigation_preservation_info = f'申请诉讼保全：是☑\n申请内容：{
                preservation_info_litigation_preservation_request}\n否☐'
        else:
            format_litigation_preservation_info = f'申请诉讼保全：是☐\n申请内容：\n否☑'

        format_preservation_info = f'{format_pre_preservation_info}\n{
            format_litigation_preservation_info}'

        competent_preservation = [
            {
                "type": "1.有无仲裁、法院管辖约定",
                "information": format_jurisdiction_info
            },
            {
                "type": "2.是否申请财产保全措施",
                "information": format_preservation_info
            }
        ]
        return competent_preservation

    @staticmethod
    def _format_party_info(party_data):
        """格式化单个当事人信息"""
        if not isinstance(party_data, dict):
            return ""

        # 使用集合简化条件判断
        party_keys = {"plaintiffs", "defendants",
                      "third_parties", "respondents"}
        if not party_keys.intersection(party_data.keys()):
            return ""

        # 提取字段映射表，便于维护和扩展
        fields = {
            'name': '姓名',
            'gender': '性别',
            'dob': '出生日期',
            'nationality': '民族',
            'employer': '工作单位',
            'position': '职务',
            'phone': '联系电话',
            'address': '住所地（户籍所在地）',
            'residence': '经常居住地'
        }

        parties = next((party_data.get(key)
                       for key in party_keys if party_data.get(key)), [])
        if not isinstance(parties, list):
            return ""

        info_lines = []
        for party in parties:
            if not isinstance(party, dict):
                continue  # 跳过非字典类型的当事人

            if party.get('type'):  # 跳过没有姓名的当事人
                continue

            for field, label in fields.items():
                value = party.get(field)
                if value is None:
                    value = ''

                if field == 'gender':  # 特殊处理性别字段
                    gender_map = {
                        "男": f"{label}：男☑ 女☐",
                        "女": f"{label}：男☐ 女☑"
                    }
                    info_lines.append(gender_map.get(value, f"{label}：男☐ 女☐"))
                else:
                    info_lines.append(f"{label}：{value}")

            info_lines.append("")  # 添加空行分隔不同当事人

        if len(info_lines) == 0:
            return "姓名：\n性别：男☐ 女☐\n出生日期：   年   月   日\n民族：\n工作单位：\n职务：\n联系电话：\n住所地（户籍所在地）：\n经常居住地："

        return "\n".join(info_lines).strip()  # 去除末尾的空行

    @staticmethod
    def _format_company_info(company_data):
        """Format company information according to the specified template"""
        if not isinstance(company_data, dict):
            return ""

        party_keys = {"plaintiffs", "defendants",
                      "third_parties", "respondents"}
        if not party_keys.intersection(company_data.keys()):
            return ""

        parties = next((company_data.get(key)
                       for key in party_keys if company_data.get(key)), [])
        if not isinstance(parties, list):
            return ""

        # 提取字段映射表，便于维护和扩展
        fields = {
            'name': '名称',
            'address': '住所地（主要办事机构所在地）',
            'registered_address': '注册地/登记地',
            'legal_representative': '法定代表人/主要负责人',
            'position': '职务',
            'phone': '联系电话',
            'unified_code': '统一社会信用代码'
        }
        # 处理企业类型
        company_types = [
            "有限责任公司",
            "股份有限公司",
            "上市公司",
            "其他企业法人",
            "事业单位",
            "社会团体",
            "基金会",
            "社会服务机构",
            "机关法人",
            "农村集体经济组织法人",
            "城镇农村的合作经济组织法人",
            "基层群众性自治组织法人",
            "个人独资企业",
            "合伙企业",
            "不具有法人资格的专业服务机构"
        ]

        info_lines = []
        type_lines = []
        for party in parties:
            if not isinstance(party, dict):
                continue  # 跳过非字典类型的当事人

            if party.get('gender'):  # 跳过自然人
                continue
            for field, label in fields.items():
                value = party.get(field)
                if value is None:
                    value = ''
                info_lines.append(f"{label}：{value}")

            current_type = party.get('type', '')

            type_line = '类型：'
            for t in company_types:
                checkbox = "☑" if t == current_type else "☐"
                type_line += f"{t}{checkbox} "

            type_lines.append(type_line)

            current_ownership = party.get('ownership', '')
            if current_ownership == '民营':
                type_lines.append("国有☐ （控股☐参股☐） 民营☑")
            elif current_ownership == '国有(控股)':
                type_lines.append("国有☑ （控股☑参股☐） 民营☐")
            elif current_ownership == '国有(参股)':
                type_lines.append("国有☐ （控股☐参股☑） 民营☐")
            else:
                type_lines.append("国有☐ （控股☐参股☐） 民营☐")

        if len(info_lines) == 0:
            return "名称：\n住所地（主要办事机构所在地）：\n注册地/登记地：\n法定代表人/主要负责人：\n职务：\n联系电话：\n统一社会信用代码：\n类型：有限责任公司☐ 股份有限公司☐ 上市公司☐ 其他企业法人☐ 事业单位☐ 社会团体☐ 基金会☐ 社会服务机构☐ 机关法人☐ 农村集体经济组织法人☐  城镇农村的合作经济组织法人☐ 基层群众性自治组织法人☐ 个人独资企业☐ 合伙企业☐ 不具有法人资格的专业服务机构☐\n国有☐ （控股☐参股☐） 民营☐"

        return "\n".join(info_lines + type_lines)

    @staticmethod
    def _format_agents(case_data):
        """格式化委托代理人信息，包含勾选框"""
        agents = case_data.get("agents", [])

        if not agents:
            # 如果没有代理人，返回默认的无代理人信息
            formatted_agent = "有：☐\n姓名：\n职务：\n单位：\n联系电话：\n代理权限：一般授权☐ 特别授权☐\n无：☑"
        else:
            # 如果有代理人，处理每个代理人的信息
            formatted_agent = "有：☑\n"
            for agent in agents:
                # 处理代理权限（authority）字段
                authority = agent.get("authority", "")
                if authority == "一般授权":
                    authority_formatted = "一般授权☑ 特别授权☐"
                elif authority == "特别授权":
                    authority_formatted = "一般授权☐ 特别授权☑"
                else:
                    authority_formatted = "一般授权☐ 特别授权☐"

                # 拼接每个代理人的信息
                formatted_agent += (
                    f"姓名：{agent.get('name', '')}\n"
                    f"职务：{agent.get('employer', '')}\n"
                    f"单位：{agent.get('position', '')}\n"
                    f"联系电话：{agent.get('phone', '')}\n"
                    f"代理权限：{authority_formatted}\n\n"
                )
            formatted_agent += "无：☐"  # 添加无代理人的勾选框

        return formatted_agent

    @staticmethod
    def _format_delivery_info(case_data):
        """格式化送达地址信息"""
        delivery_info = case_data.get("delivery_info", {})
        formatted_address = f"地址：{delivery_info.get('address', '')}\n收件人：{delivery_info.get(
            'recipient', '')}\n联系电话：{delivery_info.get('recipient_phone', '')}"

        return formatted_address

    @staticmethod
    def _format_electronic_delivery(case_data):
        """格式化是否接受电子送达信息"""
        electronic_delivery = case_data.get("electronic_delivery_info", {})

        formatted_electronic_delivery = ''
        method = f'方式：\n短信：{electronic_delivery.get('SMS', '')}\n微信:{electronic_delivery.get('wechat', '')}\n传真：{
            electronic_delivery.get('fax', '')}\n邮箱：{electronic_delivery.get('email', '')}\n其他：{electronic_delivery.get('other', '')}\n'

        if electronic_delivery:
            formatted_electronic_delivery = f'是☑ {method}否☐'
        else:
            formatted_electronic_delivery = f'是☐ {method}否☑'

        return formatted_electronic_delivery


class DataFormatter(Protocol):
    """定义数据格式化器的接口"""
    @staticmethod
    def format_case(case: Any) -> dict:
        """将案件数据转换为模板所需的格式"""
        ...


class DocumentGenerator:
    """通用文档生成器类"""

    DOCUMENT_TYPES = {
        "complaint": "起诉状",
        "complaint_2p": "起诉状", # 只有两个部分的起诉状模版
        "defense": "答辩状",
        "defense_2p": "答辩状",  # 只有两个部分的答辩状模版
    }

    TEMPLATE_FILES = {
        "complaint": "complaint.docx",
        "complaint_2p": "complaint_2p.docx",
        "defense": "defense.docx",
        "defense_2p": "defense_2p.docx",
    }

    @classmethod
    def sanitize_filename(cls, name: str) -> str:
        """清理文件名中的非法字符"""
        return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)


    @classmethod
    def generate_document(
        cls,
        doc_type: str,
        thisCase: Any,
        formatter_class: type[DataFormatter],
        plaintiff_name: str,
        defendant_name: str = '',
        template_dir: str = "templates"
    ) -> tuple[bytes, str]:
        """
        生成文档并返回文件字节流和文件名

        Args:
            doc_type: 文档类型 ("complaint" 或 "defense")
            case: 案件对象
            formatter_class: 用于格式化数据的类(需实现format_case静态方法)
            plaintiff_name: 原告姓名
            defendant_name: 被告姓名
            template_dir: 模板文件目录

        Returns:
            tuple: (文件字节流, 文件名)
        """
        # 验证文档类型
        if doc_type not in cls.DOCUMENT_TYPES:
            raise ValueError(f"无效的文档类型: {doc_type}")

        # 获取当前目录并生成模板文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "..", template_dir, cls.TEMPLATE_FILES[doc_type])
        template_path = os.path.abspath(template_path)

        if not os.path.exists(template_path):
                    raise FileNotFoundError(f"找不到模板文件: {template_path}")

        # 清理文件名中的非法字符
        sanitized_plaintiff_name = cls.sanitize_filename(plaintiff_name)
        sanitized_defendant_name = cls.sanitize_filename(defendant_name)

        # 生成文件名
        current_date = datetime.now().strftime("%Y%m%d")
        doc_type_name = cls.DOCUMENT_TYPES[doc_type]
        filename_parts = [sanitized_plaintiff_name, doc_type_name, current_date]
        if defendant_name:
            filename_parts.insert(1, f"{sanitized_defendant_name}、")
        filename = "-".join(filename_parts) + ".docx"

        # 使用传入的格式化器格式化数据
        formatted_data = formatter_class.format_case(thisCase)
        print(formatted_data)
        preview_data = form_json_to_markdown(formatted_data, doc_type)

        # 生成文档
        doc = DocxTemplate(template_path)
        doc.render(formatted_data)

        # 将文档保存到字节流
        doc_stream = io.BytesIO()
        doc.save(doc_stream)
        doc_stream.seek(0)

        return doc_stream.getvalue(), filename, preview_data

def form_json_to_markdown(form_data: dict, doc_type: str = "complaint") -> str:
    """
    将表单JSON数据转换为Markdown表格格式
    
    Args:
        form_data: 表单数据字典
        doc_type: 文书类型，可选值："complaint"或"defense"
    """
    markdown = []
    
    # 添加标题
    markdown.append("#### 填写内容预览")
    markdown.append(f"#### 案由：{form_data['case_type']}")
    if doc_type == "defense":
        markdown.append(f"##### 案号：{form_data['case_num']}")
    markdown.append(f"##### 填写日期：{form_data['date']}\n")
    
    # 处理当事人信息
    markdown.append("##### 当事人信息")
    markdown.append("| 项目 | 内容 |")
    markdown.append("|------|------|")
    for party in form_data['party_informations']:
        information = party['information'].replace('\n', '<br>')
        markdown.append(f"| {party['type']} | {information} |")
    markdown.append("")
    
    # 处理管辖与保全信息
    if 'competent_preservation' in form_data and form_data['competent_preservation']:
        markdown.append("##### 管辖与保全")
        markdown.append("| 项目 | 内容 |")
        markdown.append("|------|------|")
        for item in form_data['competent_preservation']:
            information = item['information'].replace('\n', '<br>')
            markdown.append(f"| {item['type']} | {information} |")     
        markdown.append("")
    
    # 处理请求/答辩事项
    if 'reply_matters' in form_data:
        section_title = "诉讼请求" if doc_type == "complaint" else "答辩事项"
        markdown.append(f"##### {section_title}")
        markdown.append("| 项目 | 内容 |")
        markdown.append("|------|------|")
        for item in form_data['reply_matters']:
            information = item['information'].replace('\n', '<br>')
            markdown.append(f"| {item['type']} | {information} |")    
        markdown.append("")
    
    # 处理事实与理由
    if 'reasons' in form_data and form_data['reasons']:
        markdown.append("##### 事实与理由")
        markdown.append("| 项目 | 内容 |")
        markdown.append("|------|------|")
        for item in form_data['reasons']:
            information = item['information'].replace('\n', '<br>')
            markdown.append(f"| {item['type']} | {information} |")    
        markdown.append("")
    
    return "\n".join(markdown)

