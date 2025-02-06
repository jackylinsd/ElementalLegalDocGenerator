import streamlit as st
from utils.type import *

footer = '''
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: #333;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
</style>

<div class="footer">
    <p>© 2025 李伯阳</p>
</div>
'''


st.title("要素式诉状生成器")


pleading_type = st.selectbox("请选择你的文书类型：", PLEADING_PAGE_PATH.keys() )
case_type = st.selectbox("请选择你的案件类型：", CASE_CATEGORIES)

if st.button("搜索模版",type='primary'):
    st.page_link(f"page/{PLEADING_PAGE_PATH[pleading_type]}/{CASE_TYPE_PAGE_PATH[case_type]}",label="开始填写")


st.markdown("_____")
st.subheader("说明")
st.markdown("1. 可以直接在侧边栏选择或搜索模版使用：选择文书类型和案件类型，点击`搜索模版`，再点击`开始填写`即可进入相应文书的填写页面。\n2. 根据模版内容填写完成后，点击`生成`按钮，数秒后即可生成完毕，然后点击`下载`按钮即可下载。\n3. 目前为测试版，可能有错漏之处，请尽量复查文件内容。\n4. 需要部署协助或有其他疑惑、建议，请联系微信`legal-lby`。")
st.markdown(footer,unsafe_allow_html=True)
