import streamlit as st
from page.components.complaint import Plaintiff
from page.components.jurisdiction_and_preservation import JurisdictionAndPreservation
from page.components.header import header
from page.components.section import create_text_section, create_radio_section, CommonCasePlaintiff
from page.components.complaint import Defendant, Plaintiff, ThirdParty
from utils.document_generator import DocumentGenerator, BaseCaseFormatter
import json

CASE_TYPE = "银行信用卡纠纷"

thisCase = CommonCasePlaintiff()

def claim(thisCase):
    pass

def fact(thisCase):
    pass

class CreditCardCaseFormatter(BaseCaseFormatter):
    """数据格式化器"""

    BaseCaseFormatter.case_type = CASE_TYPE

    @staticmethod
    def format_case(case):
        """将案件对象转换为适合文档模板的格式"""
        case_data = json.loads(case.to_json())
        template_data = super(CreditCardCaseFormatter, CreditCardCaseFormatter).format_case(case)

        # 使用全局定义的问题列表
        # reply_questions = REPLY_QUESTIONS + ["答辩依据"]
        # reason_questions = REASON_QUESTIONS + [
        #     "其他需要说明的内容（可另附页）",
        #     "证据清单（可另附页）",
        # ]

        # template_data.update(
        #     {
        #         "reply_matters": [
        #             {"type": f"{i+1}. {q}", "information": info if info else ""}
        #             for i, (q, info) in enumerate(
        #                 zip(
        #                     reply_questions,
        #                     case_data.get("replay_matters", [])
        #                     + [""]
        #                     * (
        #                         len(reply_questions)
        #                         - len(case_data.get("replay_matters", []))
        #                     ),
        #                 )
        #             )
        #         ],
        #         "reasons": [
        #             {"type": f"{i+1}. {q}", "information": info if info else ""}
        #             for i, (q, info) in enumerate(
        #                 zip(
        #                     reason_questions,
        #                     case_data.get("reasons", [])
        #                     + [""]
        #                     * (
        #                         len(reason_questions)
        #                         - len(case_data.get("reasons", []))
        #                     ),
        #                 )
        #             )
        #         ],
        #     }
        # )
        return template_data


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
st.header("约定管辖和诉讼保全")
thisCase.jurisdiction_and_preservation.show()

st.markdown("""______""")
st.header("事实和理由")
fact(thisCase)

if st.button("生成起诉状"):
    # 输出 JSON 格式的案件信息
    st.write("案件信息（JSON 格式）:")
    st.json(thisCase.to_json())
    print(thisCase.to_json())

    try:
        with st.spinner("生成中..."):
            doc_bytes, filename = DocumentGenerator.generate_document(
                "complaint",
                thisCase,
                CreditCardCaseFormatter,
                thisCase.plaintiff.plaintiffs[0].get("name",""),
                thisCase.defendant.defendants[0].get("name",""),
            )

        st.download_button(
            label="下载起诉状",
            data=doc_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        import traceback
        st.error(f"生成文档时出错: {str(e)}\n{str(traceback.print_exc())}")
