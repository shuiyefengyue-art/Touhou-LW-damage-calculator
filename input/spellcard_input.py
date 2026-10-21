# === 使用スペカ情報 ===
import streamlit as st

import lists

def run():
    spell = {
        "soloall": 0,
        "lv": 30,
        "bullets": [],
        "card_type_buffs": [],
        "card_element_buffs": []
    }
    # 単体or全体
    spell["soloall"] = st.selectbox(
        "単体or全体",
        lists.soloalls
    )

    # スペカ&ショットレベル補正
    spell["lv"] = st.number_input(
        "スペカ&ショットレベル補正(Lossy's JournalのLV Multの値。不明なら、とりあえず30でいいと思います。)(%)",
        min_value=0,
        value=30
    )

    # バレット情報
    if "bullets" not in st.session_state:
        st.session_state.bullets = []

    st.subheader("バレット情報")

    if st.button("+ バレットを追加"):
        st.session_state.bullets.append({
            "power": 0.00,
            "rawcriacc": 0,
            "slice": 0,
            "hard": 0,
            "numbers": 0,
            "type": 0,
            "element": 0,
            "yangyin": 0,
            "criaccupper": [],
            "mirror": 0,
            "penetrate": 0
        })

    if st.button("- 最後に追加したバレットを削除"):
        if st.session_state.bullets:
            st.session_state.bullets.pop()
            st.rerun()

    for i, bullet in enumerate(st.session_state.bullets):
        with st.expander(f"{i + 1} 段目", expanded=False):

            bullet["power"] = st.number_input(
                "威力",
                min_value=0.00,
                value=bullet["power"],
                key=f"bullet_{i}_power"
            )

            bullet["rawcriacc"] = st.number_input(
                "基礎CRI率(%)",
                min_value=0,
                value=bullet["rawcriacc"],
                key=f"bullet_{i}_rawcriacc"
            )

            bullet["slice"] = st.number_input(
                "斬烈(%)",
                min_value=0,
                value=bullet["slice"],
                key=f"bullet_{i}_slice"
            )

            bullet["hard"] = st.number_input(
                "硬質(%)",
                min_value=0,
                value=bullet["hard"],
                key=f"bullet_{i}_hard"
            )

            bullet["numbers"] = st.number_input(
                "弾数",
                min_value=0,
                value=bullet["numbers"],
                step=1,
                key=f"bullet_{i}_numbers"
            )

            bullet["type"] = st.selectbox(
                "弾種",
                lists.types,
                key=f"bullet_{i}_type"
            )

            bullet["element"] = st.selectbox(
                "属性",
                lists.elements,
                key=f"bullet_{i}_element"
            )

            bullet["yangyin"] = st.selectbox(
                "陰陽",
                lists.yangyins,
                key=f"bullet_{i}_yangyin"
            )

            bullet["criaccupper"] = st.multiselect(
                "CRI命中上乗せ弾",
                lists.criaccuppers,
                default=bullet["criaccupper"],
                key=f"bullet_{i}_criaccupper"
            )

            bullet["mirror"] = st.selectbox(
                "鏡面弾?",
                lists.yesnos,
                key=f"bullet_{i}_mirror"
            )

            bullet["penetrate"] = st.selectbox(
                "貫通弾?",
                lists.yesnos,
                key=f"bullet_{i}_penetrate"
            )

    spell["bullets"] = st.session_state.bullets

    # 絵札弾種補正
    st.subheader("弾種補正(絵札)")
    spell_card_type_buffs = []

    for i, bullet_type in enumerate(lists.types):
        value = st.number_input(
            f"{bullet_type}(%)",
            min_value=0,
            value=0,
            key=f"card_type_buff_{i}"
        )

        if value != 0:
            spell_card_type_buffs.append((bullet_type, value))

    spell["card_type_buffs"] = spell_card_type_buffs

    # 絵札属性補正
    st.subheader("属性補正(絵札)")
    spell_card_element_buffs = []

    for i, bullet_element in enumerate(lists.elements):
        value = st.number_input(
            f"{bullet_element}(%)",
            min_value=0,
            value=0,
            key=f"card_element_buff_{i}"
        )

        if value != 0:
            spell_card_element_buffs.append((bullet_element, value))

    spell["card_element_buffs"] = spell_card_element_buffs


    return spell