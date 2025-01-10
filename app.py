import streamlit as st
from page.components.complaint import Plaintiff
from utils.type import *
import os


# 动态生成 pages 字典
pages = {"首页": [st.Page("page/home.py", title="首页", url_path="home")]}
for case_type, page_path in CASE_TYPE_PAGE_PATH.items():
    # 为每种诉讼类型创建独特的URL pathname
    complaint_path = f'complaints_{page_path.replace(".py", "")}'
    answer_path = f'answers_{page_path.replace(".py", "")}'
    
    # 将页面添加到对应的诉状类型下
    if "起诉状" not in pages:
        pages["起诉状"] = []
    if "答辩状" not in pages:
        pages["答辩状"] = []
        
    pages["起诉状"].append(
        st.Page(f'page/complaints/{page_path}', 
                title=case_type,
                url_path=complaint_path
                )
    )
    pages["答辩状"].append(
        st.Page(f'page/defendant/{page_path}', 
                title=case_type,
                url_path=answer_path
                )
    )

pg = st.navigation(pages)
pg.run()