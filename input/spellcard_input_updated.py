# === 使用スペカ情報 ===
import copy
import importlib
import pkgutil

import streamlit as st
import lists
import lastwords


def get_last_words():
    last_words = {}

    
    for module_info in pkgutil.iter_modules(lastwords.__path__):
        if module_info.name.startswith("_"):
            continue

        module = importlib.import_module(
        f"lastwords.{module_info.name}"
        )

        if hasattr(module, "NAME") and hasattr(module, "DATA"):
            last_words[module.NAME] = module.DATA

    return last_words


LAST_WORDS = get_last_words()
MANUAL_INPUT = "手動入力"


def default_bullet():
    return {
        "power": 0.00,
        "rawcriacc": 0,
        "slice": 0,
        "hard": 0,
        "numbers": 0,
        "type": lists.types[0],
        "element": lists.elements[0],
        "yangyin": lists.yangyins[0],
        "criaccupper": [],
        "mirror": lists.yesnos[0],
        "penetrate": lists.yesnos[0],
    }


def load_selected_lastword():
    selected = st.session_state.get("selected_lastword", MANUAL_INPUT)

    if selected == MANUAL_INPUT or selected not in LAST_WORDS:
        return

    data = copy.deepcopy(LAST_WORDS[selected])

    # スペカの基本情報
    st.session_state["spell_soloall"] = data["soloall"]
    st.session_state["spell_lv"] = data["lv"]

    # バレット情報
    old_bullet_count = len(st.session_state.get("bullets", []))
    new_bullets = copy.deepcopy(data["bullets"])
    st.session_state["bullets"] = new_bullets

    bullet_fields = [
        "power",
        "rawcriacc",
        "slice",
        "hard",
        "numbers",
        "type",
        "element",
        "yangyin",
        "criaccupper",
        "mirror",
        "penetrate",
    ]

    for i, bullet in enumerate(new_bullets):
        for field in bullet_fields:
            st.session_state[f"bullet_{i}_{field}"] = copy.deepcopy(bullet[field])

    for i in range(len(new_bullets), old_bullet_count):
        for field in bullet_fields:
            st.session_state.pop(f"bullet_{i}_{field}", None)

    type_buffs = dict(data.get("card_type_buffs", []))
    element_buffs = dict(data.get("card_element_buffs", []))

    for i, bullet_type in enumerate(lists.types):
        st.session_state[f"card_type_buff_{i}"] = type_buffs.get(bullet_type, 0)

    for i, bullet_element in enumerate(lists.elements):
        st.session_state[f"card_element_buff_{i}"] = element_buffs.get(
            bullet_element, 0
        )


def run():
    if "bullets" not in st.session_state:
        st.session_state.bullets = []

    if "selected_lastword" not in st.session_state:
        st.session_state["selected_lastword"] = MANUAL_INPUT

    if "spell_soloall" not in st.session_state:
        st.session_state["spell_soloall"] = lists.soloalls[0]

    if "spell_lv" not in st.session_state:
        st.session_state["spell_lv"] = 30

    spell = {
        "soloall": st.session_state["spell_soloall"],
        "lv": st.session_state["spell_lv"],
        "bullets": st.session_state.bullets,
        "card_type_buffs": [],
        "card_element_buffs": [],
    }

    # ラストワード選択
    st.subheader("ラストワード")
    lastword_names = [MANUAL_INPUT] + sorted(LAST_WORDS.keys())

    if st.session_state["selected_lastword"] not in lastword_names:
        st.session_state["selected_lastword"] = MANUAL_INPUT

    st.selectbox(
        "ラストワード名",
        options=lastword_names,
        key="selected_lastword",
        on_change=load_selected_lastword
    )

    spell["soloall"] = st.selectbox(
        "単体or全体",
        lists.soloalls,
        key="spell_soloall",
    )

    spell["lv"] = st.number_input(
        "スペカ&ショットレベル補正(Lossy's JournalのLV Multの値。不明なら、とりあえず30でいいと思います。)(%)",
        min_value=0,
        step=1,
        key="spell_lv",
    )

    # バレット情報
    st.subheader("バレット情報")

    if st.button("+ バレットを追加"):
        st.session_state.bullets.append(default_bullet())
        st.rerun()

    if st.button("- 最後に追加したバレットを削除"):
        if st.session_state.bullets:
            removed_index = len(st.session_state.bullets) - 1
            st.session_state.bullets.pop()

            for field in [
                "power",
                "rawcriacc",
                "slice",
                "hard",
                "numbers",
                "type",
                "element",
                "yangyin",
                "criaccupper",
                "mirror",
                "penetrate",
            ]:
                st.session_state.pop(f"bullet_{removed_index}_{field}", None)

            st.rerun()

    bullet_fields = [
        "power",
        "rawcriacc",
        "slice",
        "hard",
        "numbers",
        "type",
        "element",
        "yangyin",
        "criaccupper",
        "mirror",
        "penetrate",
    ]

    for i, bullet in enumerate(st.session_state.bullets):
        for field in bullet_fields:
            key = f"bullet_{i}_{field}"
            if key not in st.session_state:
                st.session_state[key] = copy.deepcopy(bullet[field])

    for i, bullet in enumerate(st.session_state.bullets):
        with st.expander(f"{i + 1} 段目", expanded=False):
            bullet["power"] = st.number_input(
                "威力",
                min_value=0.00,
                key=f"bullet_{i}_power",
            )

            bullet["rawcriacc"] = st.number_input(
                "基礎CRI率(%)",
                min_value=0,
                key=f"bullet_{i}_rawcriacc",
            )

            bullet["slice"] = st.number_input(
                "斬烈(%)",
                min_value=0,
                key=f"bullet_{i}_slice",
            )

            bullet["hard"] = st.number_input(
                "硬質(%)",
                min_value=0,
                key=f"bullet_{i}_hard",
            )

            bullet["numbers"] = st.number_input(
                "弾数",
                min_value=0,
                step=1,
                key=f"bullet_{i}_numbers",
            )

            bullet["type"] = st.selectbox(
                "弾種",
                lists.types,
                key=f"bullet_{i}_type",
            )

            bullet["element"] = st.selectbox(
                "属性",
                lists.elements,
                key=f"bullet_{i}_element",
            )

            bullet["yangyin"] = st.selectbox(
                "陰陽",
                lists.yangyins,
                key=f"bullet_{i}_yangyin",
            )

            bullet["criaccupper"] = st.multiselect(
                "CRI命中上乗せ弾",
                lists.criaccuppers,
                key=f"bullet_{i}_criaccupper",
            )

            bullet["mirror"] = st.selectbox(
                "鏡面弾?",
                lists.yesnos,
                key=f"bullet_{i}_mirror",
            )

            bullet["penetrate"] = st.selectbox(
                "貫通弾?",
                lists.yesnos,
                key=f"bullet_{i}_penetrate",
            )

    spell["bullets"] = st.session_state.bullets

    # 絵札弾種補正
    st.subheader("弾種補正(絵札)")

    for i, bullet_type in enumerate(lists.types):
        key = f"card_type_buff_{i}"
        if key not in st.session_state:
            st.session_state[key] = 0

        value = st.number_input(
            f"{bullet_type}(%)",
            min_value=0,
            step=1,
            key=key,
        )

        if value != 0:
            spell["card_type_buffs"].append((bullet_type, value))

    # 絵札属性補正
    st.subheader("属性補正(絵札)")

    for i, bullet_element in enumerate(lists.elements):
        key = f"card_element_buff_{i}"
        if key not in st.session_state:
            st.session_state[key] = 0

        value = st.number_input(
            f"{bullet_element}(%)",
            min_value=0,
            step=1,
            key=key,
        )

        if value != 0:
            spell["card_element_buffs"].append((bullet_element, value))

    return spell
