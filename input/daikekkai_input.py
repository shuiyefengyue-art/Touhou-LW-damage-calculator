# ===== 大結界 =====
import streamlit as st

import lists

def run():
    daikekkai = st.selectbox(
        "大結界&秘密封印",
        lists.daikekkais,
    )

    return daikekkai