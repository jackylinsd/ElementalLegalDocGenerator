import streamlit as st

css = """
<style>
/* 针对不含 stMainMenuList 的下拉菜单 */
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) {
    position: relative;
}

/* 隐藏下拉菜单中的原始英文月份文本 */
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"] {
    visibility: hidden;
    position: relative;
    text-align: center;
}

/* 通用的 ::after 样式，确保居中 */
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]::after {
    visibility: visible;
    position: absolute;
    left: 0;
    right: 0;
    margin: 0 auto;
    width: 100%;
    top: 50%;
    transform: translateY(-50%);
    text-align: center;
}

/* 为下拉菜单的每个月份指定中文内容 */
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(1)::after { content: "一月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(2)::after { content: "二月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(3)::after { content: "三月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(4)::after { content: "四月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(5)::after { content: "五月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(6)::after { content: "六月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(7)::after { content: "七月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(8)::after { content: "八月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(9)::after { content: "九月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(10)::after { content: "十月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(11)::after { content: "十一月"; }
[data-baseweb="menu"]:not([data-testid="stMainMenuList"]) [role="option"]:nth-child(12)::after { content: "十二月"; }

/* 隐藏日期选择器中的原始星期文本 */
div[data-baseweb="calendar"] [alt="Monday"],
div[data-baseweb="calendar"] [alt="Tuesday"],
div[data-baseweb="calendar"] [alt="Wednesday"],
div[data-baseweb="calendar"] [alt="Thursday"],
div[data-baseweb="calendar"] [alt="Friday"],
div[data-baseweb="calendar"] [alt="Saturday"],
div[data-baseweb="calendar"] [alt="Sunday"] {
    visibility: hidden;
    position: relative;
    text-align: center;
}

/* 使用 ::after 显示日期选择器中的中文星期并居中 */
div[data-baseweb="calendar"] [alt="Monday"]::after { content: "周一"; visibility: visible; position: absolute; left: 0; right: 0; margin: 0 auto; width: 100%; top: 50%; transform: translateY(-50%); text-align: center; }
div[data-baseweb="calendar"] [alt="Tuesday"]::after { content: "周二"; visibility: visible; position: absolute; left: 0; right: 0; margin: 0 auto; width: 100%; top: 50%; transform: translateY(-50%); text-align: center; }
div[data-baseweb="calendar"] [alt="Wednesday"]::after { content: "周三"; visibility: visible; position: absolute; left: 0; right: 0; margin: 0 auto; width: 100%; top: 50%; transform: translateY(-50%); text-align: center; }
div[data-baseweb="calendar"] [alt="Thursday"]::after { content: "周四"; visibility: visible; position: absolute; left: 0; right: 0; margin: 0 auto; width: 100%; top: 50%; transform: translateY(-50%); text-align: center; }
div[data-baseweb="calendar"] [alt="Friday"]::after { content: "周五"; visibility: visible; position: absolute; left: 0; right: 0; margin: 0 auto; width: 100%; top: 50%; transform: translateY(-50%); text-align: center; }
div[data-baseweb="calendar"] [alt="Saturday"]::after { content: "周六"; visibility: visible; position: absolute; left: 0; right: 0; margin: 0 auto; width: 100%; top: 50%; transform: translateY(-50%); text-align: center; }
div[data-baseweb="calendar"] [alt="Sunday"]::after { content: "周日"; visibility: visible; position: absolute; left: 0; right: 0; margin: 0 auto; width: 100%; top: 50%; transform: translateY(-50%); text-align: center; }

/* 隐藏主菜单按钮 */
[data-testid="stMainMenu"] button {
    display: none; /* 或 visibility: hidden; 根据需求选择 */
}
</style>
"""



def st_date_input(label, key, value="today",min_value=None, max_value=None):
    """
    自定义日期选择组件，默认返回格式化后的日期（X年X月X日）。
    """
    # st.html(css)
    # 调用 st.date_input 获取用户选择的日期
    selected_date = st.date_input(label, value=value, key=key, max_value=max_value, min_value=min_value)

    if selected_date == "":
        return ''

    # 将日期格式化为 "X年X月X日" 的格式
    formatted_date = selected_date.strftime("%Y年%m月%d日")

    # 返回格式化后的日期
    return formatted_date
