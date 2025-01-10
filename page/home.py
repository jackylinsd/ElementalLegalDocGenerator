import streamlit as st
from utils.type import *



st.title("要素式诉状生成器")


pleading_type = st.selectbox("请选择你的文书类型：", PLEADING_PAGE_PATH.keys() )
case_type = st.selectbox("请选择你的案件类型：", CASE_CATEGORIES)

if st.button("搜索模版",type='primary'):
    st.page_link(f"page/{PLEADING_PAGE_PATH[pleading_type]}/{CASE_TYPE_PAGE_PATH[case_type]}",label="开始填写")   
