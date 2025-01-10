import streamlit as st
from page.components.complaint import Plaintiff
from page.components.jurisdiction_and_preservation import JurisdictionAndPreservation
from page.components.header import header

CASE_TYPE = "金融借款合同纠纷"

header(CASE_TYPE)

st.header("当事人信息")
Plaintiff(CASE_TYPE).show()
st.header("约定管辖和诉讼保全")
JurisdictionAndPreservation()