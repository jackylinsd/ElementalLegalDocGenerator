CASE_CATEGORIES = [
    '保证保险合同纠纷',
    '机动车交通事故责任纠纷',
    '金融借款合同纠纷',
    '劳动争议纠纷',
    '离婚纠纷',
    '买卖合同纠纷',
    '民间借贷纠纷',
    '融资租赁合同纠纷',
    '物业服务合同纠纷',
    '银行信用卡纠纷',
    '证券虚假陈述责任纠纷'
]

CASE_COMPLAINT_PLAINTIFFS_NO_NP = [
    '劳动争议纠纷',
    '离婚纠纷'
]

CASE_COMPLAINT_PLAINTIFFS_COMPANY = [
    '保证保险合同纠纷',
    '物业服务合同纠纷',
]

CASE_COMPLAINT_PLAINTIFFS_BOTH = [
    '保证保险合同纠纷',
    '机动车交通事故责任纠纷',
    '金融借款合同纠纷',
    '买卖合同纠纷',
    '民间借贷纠纷',
    '融资租赁合同纠纷',
    '物业服务合同纠纷',
    '银行信用卡纠纷',
    '证券虚假陈述责任纠纷'
]

CASE_COMPLAINT_BOTH_PEOPLE_FIRST = [
    '机动车交通事故责任纠纷',
    '民间借贷纠纷',
    '证券虚假陈述责任纠纷'
]

PLEADING_PAGE_PATH = {  # 诉状类型
    "起诉状": "complaints",
    "答辩状": "answers",
}

CASE_TYPE_PAGE_PATH = {  # 案件类型
    "保证保险合同纠纷": "insurance_contract_dispute.py",
    "机动车交通事故责任纠纷": "traffic_accident_dispute.py",
    "金融借款合同纠纷": "financial_loan_dispute.py",
    "劳动争议纠纷": "labor_dispute.py",
    "离婚纠纷": "divorce_dispute.py",
    "买卖合同纠纷": "sales_contract_dispute.py",
    "民间借贷纠纷": "private_lending_dispute.py",
    "融资租赁合同纠纷": "leasing_contract_dispute.py",
    "物业服务合同纠纷": "property_service_dispute.py",
    "银行信用卡纠纷": "credit_card_dispute.py",
    "证券虚假陈述责任纠纷": "securities_misrepresentation_dispute.py"
}

CASE_COMPLAINT_DEFENDANT_NO_NP = [
    '离婚纠纷'
]



CASE_SPECIAL_DEFENDANT_COMPANY_TYPE = {
    "机动车交通事故责任纠纷" : "被告（保险公司或其他法人、非法人组织）",
    "劳动争议纠纷" : "被告"
}


CASE_COMPLAINT_RESPONDENTS_NO_NP = [
    '离婚纠纷'
]



CASE_SPECIAL_RESPONDENTS_COMPANY_TYPE = {
    "机动车交通事故责任纠纷" : "被告（保险公司或其他法人、非法人组织）",
    "劳动争议纠纷" : "被告"
}

CASE_COMPLAINT_RESPONDENTS_COMPANY = [
    '保证保险合同纠纷',
]

CASE_COMPLAINT_RESPONDENTS_BOTH = [
    '保证保险合同纠纷',
    '物业服务合同纠纷',
    '机动车交通事故责任纠纷',
    '金融借款合同纠纷',
    '买卖合同纠纷',
    '民间借贷纠纷',
    '融资租赁合同纠纷',
    '物业服务合同纠纷',
    '银行信用卡纠纷',
    '证券虚假陈述责任纠纷'
]
