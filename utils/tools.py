import streamlit as st


def st_date_input(label, key, value="today"):
    """
    自定义日期选择组件，默认返回格式化后的日期（X年X月X日）。
    """
    # 调用 st.date_input 获取用户选择的日期
    selected_date = st.date_input(label, value=value, key=key)

    # 将日期格式化为 "X年X月X日" 的格式
    formatted_date = selected_date.strftime("%Y年%m月%d日")

    # 返回格式化后的日期
    return formatted_date
