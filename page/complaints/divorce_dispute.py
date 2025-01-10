# \pages\components\dispute.py 离婚纠纷
import streamlit as st
import pandas as pd
from datetime import date, datetime
import json
from page.components.complaint import Plaintiff, Defendant
from page.components.jurisdiction_and_preservation import JurisdictionAndPreservation
from page.components.header import header
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import logging

logger = logging.getLogger(__name__)


CASE_TYPE = '离婚纠纷'


class DivorceCaseFormatter(BaseCaseFormatter):
    """离婚案件数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(case):
        """将离婚案件对象转换为适合文档模板的格式"""
        try:
            case_data = json.loads(case.to_json())

            # 调用父类的通用格式化方法
            template_data = super(DivorceCaseFormatter,
                                  DivorceCaseFormatter).format_case(case)

            # 添加离婚案件的自定义部分
            template_data.update(
                DivorceCaseFormatter._format_custom_sections(case_data))

            return template_data

        except Exception as e:
            logger.error(f"格式化离婚案件数据时出错: {str(e)}")
            raise ValueError(f"格式化离婚案件数据失败: {str(e)}")

    @staticmethod
    def _format_custom_sections(case_data):
        """添加离婚案件的自定义部分"""
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

        return {
            "reply_matters": [
                {
                    "type": "1.解除婚姻关系",
                    "information": safe_get(case_data, "divorce_request", default="")
                },
                {
                    "type": "2.夫妻共同财产",
                    "information": DivorceCaseFormatter._format_property_info(safe_get(case_data, "property_data", default={}))
                },
                {
                    "type": "3.夫妻共同债务",
                    "information": DivorceCaseFormatter._format_debt_info(safe_get(case_data, "debts", default=[]))
                },
                {
                    "type": "4.子女直接抚养",
                    "information": DivorceCaseFormatter._format_children_info(safe_get(case_data, "children", default=[]))
                },
                {
                    "type": "5.子女抚养费",
                    "information": DivorceCaseFormatter._format_child_support_info(safe_get(case_data, "child_support", default={}))
                },
                {
                    "type": "6.探望权",
                    "information": DivorceCaseFormatter._format_visitation_info(safe_get(case_data, "visitation_rights", default={}))
                },
                {
                    "type": "7.离婚损害赔偿／离婚经济补偿／离婚经济帮助",
                    "information": DivorceCaseFormatter._format_damages_info(safe_get(case_data, "damages", default={}))
                },
                {
                    "type": "8.诉讼费用",
                    "information": safe_get(case_data, "litigation_fees", default={})
                },
                {
                    "type": "9.本表未列明的其他请求",
                    "information": safe_get(case_data, "other_requests", default={})
                }
            ],
            "reasons": [
                {
                    "type": "1.婚姻关系基本情况",
                    "information": DivorceCaseFormatter._format_marriage_info(safe_get(case_data, "marriage_info", default={}))
                },
                {
                    "type": "2.夫妻共同财产情况",
                    "information": safe_get(case_data, "property_facts", default="")
                },
                {
                    "type": "3.夫妻共同债务情况",
                    "information": safe_get(case_data, "debt_facts", default="")
                },
                {
                    "type": "4.子女直接抚养情况",
                    "information": safe_get(case_data, "custody_reason", default="")
                },
                {
                    "type": "5.子女抚养费情况",
                    "information": safe_get(case_data, "child_support_reason", default="")
                },
                {
                    "type": "6.子女探望权情况",
                    "information": safe_get(case_data, "visitation_reason", default="")
                },
                {
                    "type": "7.赔偿/补偿/经济帮助相关情况",
                    "information": safe_get(case_data, "compensation_reason", default="")
                },
                {
                    "type": "8.其他",
                    "information": safe_get(case_data, "other_information", default="")
                },
                {
                    "type": "9.诉请依据",
                    "information": safe_get(case_data, "legal_basis", default="")
                },
                {
                    "type": "10.证据清单",
                    "information": safe_get(case_data, "evidence_list", default="")
                }
            ]
        }

    @staticmethod
    def _format_owner(owner):
        """格式化所有者信息"""
        if owner == '原告':
            return "原告☑/被告☐/其他☐"
        elif owner == '被告':
            return "原告☐/被告☑/其他☐"
        else:
            return "原告☐/被告☐/其他☑"

    @staticmethod
    def _format_property_info(property_data):
        """格式化财产信息"""
        if not property_data:
            return "无财产☑\n有财产☐"

        info = ["无财产☐\n有财产☑"]

        # 房屋
        if property_data.get("houses"):
            for i, house in enumerate(property_data["houses"], 1):
                info.append(f"（{i}）房屋明细：归属：{DivorceCaseFormatter._format_owner(
                    house['owner'])}（{house['details']}）")

        # 汽车
        if property_data.get("cars"):
            for i, car in enumerate(property_data["cars"], 1):
                info.append(f"（{i}）汽车明细：归属：{DivorceCaseFormatter._format_owner(
                    car['owner'])}（{car['details']}）")

        # 存款
        if property_data.get("deposits"):
            for i, deposit in enumerate(property_data["deposits"], 1):
                info.append(f"（{i}）存款明细：归属：{DivorceCaseFormatter._format_owner(
                    deposit['owner'])}（{deposit['details']}）")

        # 其他财产
        if property_data.get("other_properties"):
            for i, other in enumerate(property_data["other_properties"], 1):
                info.append(f"（{i}）其他财产明细：归属：{DivorceCaseFormatter._format_owner(
                    other['owner'])}（{other['details']}）")

        return "\n".join(info)

    @staticmethod
    def _format_debt_info(debts):
        """格式化债务信息"""
        if not debts:
            return "无债务☑\n有债务☐"

        info = ['无债务☐\n有债务☑']
        for i, debt in enumerate(debts, 1):
            info.append(f"（{i}）债务{i}： {debt['描述']}  承担主体：{
                        DivorceCaseFormatter._format_owner(debt['承担主体'])}")
            if debt.get('其他承担主体'):
                info.append(f"({debt['其他承担主体']})")

        return "\n".join(info)

    @staticmethod
    def _format_children_info(children):
        """格式化子女信息"""
        if not children:
            return "无此问题☑\n有此问题☐"

        info = ["无此问题☐\n有此问题☑"]
        for i, child in enumerate(children, 1):
            info.append(f"（{i}） 子女{i}：{child['姓名']}   归属：{
                        DivorceCaseFormatter._format_owner(child['归属'])}")

        return "\n".join(info)

    @staticmethod
    def _format_child_support_info(support):
        """格式化子女抚养费信息"""
        if not support or not support.get("payer"):
            return "无此问题☑\n有此问题☐"

        info = ["无此问题☐\n有此问题☑"]
        info.append(
            f"抚养费承担主体：{DivorceCaseFormatter._format_owner(support['payer'])}")
        info.append(f"金额及明细:\n金额：{support['amount']}")
        if support.get("details"):
            info.append(f"明细：{support['details']}")
        if support.get("payment_method"):
            info.append(f"支付方式：{support['payment_method']}")

        return "\n".join(info)

    @staticmethod
    def _format_visitation_info(visitation):
        """格式化探望权信息"""
        if not visitation or not visitation.get("person"):
            return "无此问题☑\n有此问题☐"

        info = ["无此问题☐\n有此问题☑"]
        info.append(
            f"探望权行使主体：{DivorceCaseFormatter._format_owner(visitation['person'])}")
        if visitation.get("method"):
            info.append(f"行使方式：{visitation['method']}")

        return "\n".join(info)

    @staticmethod
    def _format_marriage_info(marriage):
        """格式化婚姻信息"""
        if not marriage:
            return "无"

        info = []

        info.append(f"结婚时间：{marriage['marriage_date']}")

        info.append(f"生育子女情况：{marriage['children_info']}")

        info.append(f"双方生活情况：{marriage['living_conditions']}")

        info.append(f"离婚事由：{marriage['divorce_reason']}")

        info.append(f"之前有无提起过离婚诉讼：{marriage['previous_divorce']}")

        return "\n".join(info)

    @staticmethod
    def _format_damages_info(damages):
        """格式化赔偿信息"""
        if not damages or damages == {"无此问题": 0.0}:
            return "无此问题☑\n离婚损害赔偿☐\n金额：\n离婚经济补偿☐\n金额：\n离婚经济帮助☐\n金额：\n"

        info = ["无此问题☐"]

        # 定义所有可能的损害类型
        damage_types = ["离婚损害赔偿", "离婚经济补偿", "离婚经济帮助"]

        for damage_type in damage_types:
            if damage_type in damages:
                info.append(f"{damage_type}☑")
                info.append(f"金额：{damages[damage_type]}")
            else:
                info.append(f"{damage_type}☐")
                info.append(f"金额：")

        return "\n".join(info)


class DivorceCase:
    def __init__(self):
        self.plaintiff = None
        self.defendant = None
        self.divorce_request = None
        self.property_data = {
            "houses": [],
            "cars": [],
            "deposits": [],
            "other_properties": []
        }
        self.debts = []  # 改为列表存储债务信息
        self.children = []  # 改为列表存储子女信息
        self.child_support = {
            "payer": None,
            "amount": None,
            "details": None,
            "payment_method": None
        }
        self.visitation_rights = {
            "person": None,
            "method": None
        }
        self.damages = {
            "type": None,
            "amount": None
        }
        self.marriage_info = {
            "marriage_date": None,
            "children_info": None,
            "living_conditions": None,
            "divorce_reason": None,
            "previous_divorce": None
        }
        self.jurisdiction_and_preservation = JurisdictionAndPreservation()
        self.property_facts = None
        self.debt_facts = None
        self.custody_reason = None
        self.child_support_reason = None
        self.visitation_reason = None
        self.compensation_reason = None
        self.legal_basis = None
        self.evidence_list = None

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


def claim(case):
    # 1. 解除婚姻关系
    st.subheader("1. 解除婚姻关系")
    case.divorce_request = st.text_area(
        "具体主张", key="divorce_request", placeholder="请输入解除婚姻关系的具体主张")

    # 2. 夫妻共同财产
    st.subheader("2. 夫妻共同财产")
    has_property = st.radio(
        "是否有夫妻共同财产", ["无财产", "有财产"], key="has_property", horizontal=True)

    if has_property == "有财产":
        # （1）房屋明细
        st.write("房屋明细")
        num_houses = st.number_input("房屋数量", min_value=0, max_value=10, value=len(
            case.property_data["houses"]), key="num_houses")

        # 调整房屋条目数量
        while len(case.property_data["houses"]) < num_houses:
            case.property_data["houses"].append(
                {"owner": "无", "owner_details": None, "details": ""})
        while len(case.property_data["houses"]) > num_houses:
            case.property_data["houses"].pop()

        # 显示房屋条目
        for i, house in enumerate(case.property_data["houses"]):
            st.write(f"房屋 {i + 1}")
            house["details"] = st.text_area("房屋详细信息", key=f"house_details_{
                                            i}", placeholder="请输入房屋的详细信息（如地址、面积、产权证号等）")
            house["owner"] = st.radio(
                "房屋归属", ["无", "原告", "被告", "其他"], key=f"house_owner_{i}", horizontal=True)
            if house["owner"] == "其他":
                house["owner_details"] = st.text_input("其他归属人", key=f"house_owner_details_{
                                                       i}", placeholder="请输入其他归属人")
            st.write("---")

        # （2）汽车明细
        st.write("汽车明细")
        num_cars = st.number_input("汽车数量", min_value=0, max_value=10, value=len(
            case.property_data["cars"]), key="num_cars")

        # 调整汽车条目数量
        while len(case.property_data["cars"]) < num_cars:
            case.property_data["cars"].append(
                {"owner": "无", "owner_details": None, "details": ""})
        while len(case.property_data["cars"]) > num_cars:
            case.property_data["cars"].pop()

        # 显示汽车条目
        for i, car in enumerate(case.property_data["cars"]):
            st.write(f"汽车 {i + 1}")
            car["details"] = st.text_area("汽车详细信息", key=f"car_details_{
                                          i}", placeholder="请输入汽车的详细信息（如品牌、型号、车牌号等）")
            car["owner"] = st.radio("汽车归属", ["无", "原告", "被告", "其他"], key=f"car_owner_{
                                    i}", horizontal=True)
            if car["owner"] == "其他":
                car["owner_details"] = st.text_input("其他归属人", key=f"car_owner_details_{
                                                     i}", placeholder="请输入其他归属人")
            st.write("---")

        # （3）存款明细
        st.write("存款明细")
        num_deposits = st.number_input("存款数量", min_value=0, max_value=10, value=len(
            case.property_data["deposits"]), key="num_deposits")

        # 调整存款条目数量
        while len(case.property_data["deposits"]) < num_deposits:
            case.property_data["deposits"].append(
                {"owner": "无", "owner_details": None, "details": ""})
        while len(case.property_data["deposits"]) > num_deposits:
            case.property_data["deposits"].pop()

        # 显示存款条目
        for i, deposit in enumerate(case.property_data["deposits"]):
            st.write(f"存款 {i + 1}")
            deposit["details"] = st.text_area("存款详细信息", key=f"deposit_details_{
                                              i}", placeholder="请输入存款的详细信息（如银行名称、账号、金额等）")
            deposit["owner"] = st.radio(
                "存款归属", ["无", "原告", "被告", "其他"], key=f"deposit_owner_{i}", horizontal=True)
            if deposit["owner"] == "其他":
                deposit["owner_details"] = st.text_input(
                    "其他归属人", key=f"deposit_owner_details_{i}", placeholder="请输入其他归属人")
            st.write("---")

        # （4）其他财产
        st.write("其他财产")
        num_other_properties = st.number_input("其他财产数量", min_value=0, max_value=10, value=len(
            case.property_data["other_properties"]), key="num_other_properties")

        # 调整其他财产条目数量
        while len(case.property_data["other_properties"]) < num_other_properties:
            case.property_data["other_properties"].append(
                {"owner": "无", "owner_details": None, "details": ""})
        while len(case.property_data["other_properties"]) > num_other_properties:
            case.property_data["other_properties"].pop()

        # 显示其他财产条目
        for i, other_property in enumerate(case.property_data["other_properties"]):
            st.write(f"其他财产 {i + 1}")
            other_property["details"] = st.text_area("其他财产明细", key=f"other_property_details_{
                                                     i}", placeholder="请输入其他财产的详细信息（如财产类型、数量、价值等）")
            other_property["owner"] = st.radio(
                "其他财产归属", ["无", "原告", "被告", "其他"], key=f"other_property_owner_{i}", horizontal=True)
            if other_property["owner"] == "其他":
                other_property["owner_details"] = st.text_input(
                    "其他归属人", key=f"other_property_owner_details_{i}", placeholder="请输入其他归属人")
            st.write("---")

    # 3. 夫妻共同债务（改为动态输入）
    st.subheader("3. 夫妻共同债务")
    has_debt = st.radio(
        "是否有夫妻共同债务", ["无债务", "有债务"], key="has_debt", horizontal=True)
    if has_debt == "有债务":
        num_debts = st.number_input(
            "债务数量", min_value=0, max_value=10, value=len(case.debts), key="num_debts")

        # 调整债务条目数量
        while len(case.debts) < num_debts:
            case.debts.append({"描述": "", "承担主体": "原告", "其他承担主体": ""})
        while len(case.debts) > num_debts:
            case.debts.pop()

        # 显示债务条目
        for i, debt in enumerate(case.debts):
            st.write(f"债务 {i + 1}")
            debt["描述"] = st.text_input("债务描述", key=f"debt_description_{
                                       i}", placeholder="请输入债务描述")
            debt["承担主体"] = st.radio("承担主体", ["原告", "被告", "其他"], key=f"debt_payer_{
                                    i}", horizontal=True)
            if debt["承担主体"] == "其他":
                debt["其他承担主体"] = st.text_input("其他承担主体", key=f"debt_other_payer_{
                                               i}", placeholder="请输入其他承担主体")
            st.write("---")

    # 4. 子女直接抚养（改为动态输入）
    st.subheader("4. 子女直接抚养")
    has_children = st.radio(
        "是否有子女直接抚养问题", ["无此问题", "有此问题"], key="has_children", horizontal=True)
    if has_children == "有此问题":
        num_children = st.number_input(
            "子女数量", min_value=0, max_value=10, value=len(case.children), key="num_children")

        # 调整子女条目数量
        while len(case.children) < num_children:
            case.children.append({"姓名": "", "归属": "原告"})
        while len(case.children) > num_children:
            case.children.pop()

        # 显示子女条目
        for i, child in enumerate(case.children):
            st.write(f"子女 {i + 1}")
            child["姓名"] = st.text_input("子女姓名", key=f"child_name_{
                                        i}", placeholder="请输入子女姓名")
            child["归属"] = st.radio("归属", ["原告", "被告"], key=f"child_custody_{
                                   i}", horizontal=True)
            st.write("---")

    # 5. 子女抚养费
    st.subheader("5. 子女抚养费")
    has_child_support = st.radio(
        "是否有子女抚养费问题", ["无此问题", "有此问题"], key="has_child_support", horizontal=True)
    if has_child_support == "有此问题":
        case.child_support["payer"] = st.radio(
            "抚养费承担主体", ["原告", "被告"], key="support_payer", horizontal=True)
        case.child_support["amount"] = st.number_input(
            "金额", key="support_amount", min_value=0.0, format="%.2f")
        case.child_support["details"] = st.text_area(
            "明细", key="support_details", placeholder="请输入抚养费的明细")
        case.child_support["payment_method"] = st.text_input(
            "支付方式", key="support_payment_method", placeholder="请输入支付方式")

    # 6. 探望权
    st.subheader("6. 探望权")
    has_visitation_rights = st.radio(
        "是否有探望权问题", ["无此问题", "有此问题"], key="has_visitation_rights", horizontal=True)
    if has_visitation_rights == "有此问题":
        case.visitation_rights["person"] = st.radio(
            "探望权行使主体", ["原告", "被告"], key="visitation_person", horizontal=True)
        case.visitation_rights["method"] = st.text_area(
            "行使方式", key="visitation_method", placeholder="请输入探望权的行使方式")

   # 7. 离婚损害赔偿／离婚经济补偿／离婚经济帮助
    st.subheader("7. 离婚损害赔偿／离婚经济补偿／离婚经济帮助")

    # 初始化 damages 数据
    case.damages = {}

    # 选择是否有相关问题
    has_damages = st.radio(
        "是否需要离婚损害赔偿、经济补偿或经济帮助",
        ["无此问题", "有相关问题"],
        key="has_damages",
        horizontal=True
    )

    if has_damages == "有相关问题":
        # 使用 checkbox 允许多选
        damage_types = {
            "离婚损害赔偿": st.checkbox("离婚损害赔偿", key="damages_checkbox"),
            "离婚经济补偿": st.checkbox("离婚经济补偿", key="compensation_checkbox"),
            "离婚经济帮助": st.checkbox("离婚经济帮助", key="assistance_checkbox")
        }

        # 根据用户选择动态添加类型和金额
        for damage_type, is_selected in damage_types.items():
            if is_selected:
                amount = st.number_input(
                    f"{damage_type}金额", key=f"{damage_type}_amount", min_value=0.0, format="%.2f")
                case.damages[damage_type] = amount

        # 如果没有选择任何选项，设置为 "无此问题"
        if not any(damage_types.values()):
            case.damages = {"无此问题": 0.0}
    else:
        # 如果选择 "无此问题"，直接设置数据
        case.damages = {"无此问题": 0.0}

    # 8. 诉讼费用
    st.subheader("8. 诉讼费用")
    case.litigation_fees = st.text_area(
        "诉讼费用", key="litigation_fees", placeholder="请输入诉讼费用，以及费用承担方")

    # 9. 其他请求
    st.subheader("9. 本表未列明的其他请求")
    case.other_requests = st.text_area(
        "其他请求", key="other_requests", placeholder="请输入其他请求的具体内容")


def fact(thisCase):
    # 1. 婚姻关系基本情况
    st.subheader("1. 婚姻关系基本情况")
    thisCase.marriage_info["marriage_date"] = st.date_input(
        "结婚时间", key="marriage_date")
    thisCase.marriage_info["children_info"] = st.text_area(
        "生育子女情况", key="children_info", placeholder="请输入生育子女情况")
    thisCase.marriage_info["living_conditions"] = st.text_area(
        "双方生活情况", key="living_conditions", placeholder="请输入双方生活情况")
    thisCase.marriage_info["divorce_reason"] = st.text_area(
        "离婚事由", key="divorce_reason", placeholder="请输入离婚事由")
    thisCase.marriage_info["previous_divorce"] = st.radio(
        "之前有无提起过离婚诉讼", ["无", "有"], key="previous_divorce", horizontal=True)

    # 2. 夫妻共同财产情况
    st.subheader("2. 夫妻共同财产情况")
    thisCase.property_facts = st.text_area(
        "事实和理由", key="property_facts", placeholder="请输入夫妻共同财产的事实和理由")

    # 3. 夫妻共同债务情况
    st.subheader("3. 夫妻共同债务情况")
    thisCase.debt_facts = st.text_area(
        "事实和理由", key="debt_facts", placeholder="请输入夫妻共同债务的事实和理由")

    # 4. 子女直接抚养情况
    st.subheader("4. 子女直接抚养情况")
    thisCase.custody_reason = st.text_area(
        "子女应归原告或者被告直接抚养的事由", key="custody_reason", placeholder="请输入子女直接抚养的事由")

    # 5. 子女抚养费情况
    st.subheader("5. 子女抚养费情况")
    thisCase.child_support_reason = st.text_area(
        "原告或者被告应支付抚养费及相应金额、支付方式的事由", key="child_support_reason", placeholder="请输入子女抚养费的事由")

    # 6. 子女探望权情况
    st.subheader("6. 子女探望权情况")
    thisCase.visitation_reason = st.text_area(
        "不直接抚养子女一方应否享有探望权以及具体行使方式的事由", key="visitation_reason", placeholder="请输入子女探望权的事由")

    # 7. 赔偿/补偿/经济帮助相关情况
    st.subheader("7. 赔偿/补偿/经济帮助相关情况")
    thisCase.compensation_reason = st.text_area(
        "符合离婚损害赔偿、离婚经济补偿或离婚经济帮助的相关事实等", key="compensation_reason", placeholder="请输入赔偿/补偿/经济帮助的相关事实")

    # 8. 其他
    st.subheader("8. 其他")
    thisCase.other_information = st.text_area(
        "其他", key="other_information", placeholder="请输入其他需要说明的内容")

    # 9. 诉请依据
    st.subheader("9. 诉请依据")
    thisCase.legal_basis = st.text_area(
        "法律及司法解释的规定，要写明具体条文", key="legal_basis", placeholder="请输入法律及司法解释的具体条文")

    # 10. 其他
    st.subheader("10. 证据清单（可另附页）")
    thisCase.evidence_list = st.text_area(
        "证据清单（可另附页）", value='附页', key="evidence_list", placeholder="可另附页")


# 初始化案件信息
thisCase = DivorceCase()


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

st.markdown("""______""")
st.header("诉讼请求和依据")
claim(thisCase)

st.markdown("""______""")
st.header("约定管辖和诉讼保全")
thisCase.jurisdiction_and_preservation.show()

st.markdown("""______""")
st.header("事实和理由")
fact(thisCase)

if st.button("生成起诉状"):
    # 输出 JSON 格式的案件信息
    # st.write("案件信息（JSON 格式）:")
    # st.json(case.to_json())
    # print(case.to_json())

    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "complaint",
                thisCase,
                DivorceCaseFormatter,
                thisCase.plaintiff.plaintiffs[0]["name"],
                thisCase.defendant.defendants[0]["name"],
            )

        st.download_button(
            label="下载起诉状",
            data=doc_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"生成文档时出错: {str(e)}")
