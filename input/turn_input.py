# === ターン強化 ===
import streamlit as st

def run():
    t = st.number_input(
        "このWAVEが始まって何ターン目？",
        min_value=1,
        value=1,
        step=1
    )

    return t