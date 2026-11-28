# ===== 敵側の状態 =====
import copy
import pkgutil
import importlib

import streamlit as st
import lists
import sandbags

def default_enemy():
    return {
        "killer": [],
        "lv": 100,
        "unfavourables": [],
        "favourables": [],
        "yangdefsta": 3000,
        "yindefsta": 3000,
        "favup": 0,
        "favcut": 0,
        "unfavup": 0,
        "unfavcut": 0,
        "fullbreak": 0,
        "poison": 0,
        "burn": 0,
        "agibuff": 0,
        "yangatkbuff": 0,
        "yinatkbuff": 0,
        "yangdefbuff": -10,
        "yangdefbuffeter": 0,
        "yindefbuff": -10,
        "yindefbuffeter": 0,
        "cridefbuff": 0,
        "cridefbuffeter": 0,
        "criavobuff": 0,
        "criavobuffeter": 0,
        "yangdef2buff": 0,
        "yindef2buff": 0,
        "cridef2buff": 0,
        "criavo2buff": 0,
        "yangdefrev": 0,
        "yindefrev": 0,
        "concridef": 0,
        "focusbuff": 0,
        "solobuff": 0,
        "favupbuff": 0,
        "favcutbuff": 0,
        "unfavupbuff": 0,
        "unfavcutbuff": 0,
        "type_cuts": [],
        "element_cuts": []
    }

def get_enemies():
    enemies = {}

    for module_info in pkgutil.iter_modules(sandbags.__path__):
        if module_info.name.startswith("_"):
            continue

        module = importlib.import_module(
            f"sandbags.{module_info.name}"
        )

        if hasattr(module, "NAME") and hasattr(module, "DATA"):
            enemies[module.NAME] = module.DATA

    return enemies

def load_selected_enemy(i):
    enemies = get_enemies()
    selected = st.session_state[f"enemy_{i}_selected"]

    if selected == MANUAL_INPUT:
        return

    data = copy.deepcopy(enemies[selected])
    enemy = st.session_state.enemies[i]

    enemy.update(data)

    for field, value in data.items():
        if field not in ["killer", "type_cuts", "element_cuts"]:
            st.session_state[f"enemy_{i}_{field}"] = copy.deepcopy(value)

    killer = data.get("killer", [])

    for j in range(len(st.session_state.bullets)):
        value = killer[j] if j < len(killer) else lists.yesnos[0]
        st.session_state[f"enemy_{i}_killer_{j}"] = value

    type_cuts = dict(data.get("type_cuts", []))

    for j, bullet_type in enumerate(lists.types):
        st.session_state[f"e_{i}_type_cuts_{j}"] = type_cuts.get(bullet_type, 0)

    element_cuts = dict(data.get("element_cuts", []))

    for j, bullet_element in enumerate(lists.elements):
        st.session_state[f"e_{i}_element_cuts_{j}"] = element_cuts.get(bullet_element, 0)

MANUAL_INPUT = "手動入力"

def run():
    if "enemies" not in st.session_state:
        st.session_state.enemies = []

    if st.button("+ 敵を追加"):
        st.session_state.enemies.append(default_enemy())
        st.rerun()


    if st.button("- 最後に追加した敵を削除"):
        if st.session_state.enemies:
            removed_index = len(st.session_state.enemies) - 1
            st.session_state.enemies.pop()

            for key in list(st.session_state.keys()):
                if key.startswith(f"enemy_{removed_index}_") or key.startswith(f"e_{removed_index}_"):
                    del st.session_state[key]

            st.rerun()

    enemy_names = [MANUAL_INPUT] + sorted(get_enemies().keys())

    for i, enemy in enumerate(st.session_state.enemies):
        with st.expander(f"敵 {i + 1}", expanded=False):

            selected_key = f"enemy_{i}_selected"

            if selected_key not in st.session_state:
                st.session_state[selected_key] = MANUAL_INPUT

            st.selectbox(
                "敵データを選択",
                options=enemy_names,
                key=selected_key,
                on_change=load_selected_enemy,
                args=(i,)
            )

            with st.container(height=450):
                killer = []
                for j, bullet in enumerate(st.session_state.bullets):
                    value = st.selectbox(
                        f"バレットの{j + 1}段目は特攻範囲?",
                        lists.yesnos,
                        key=f"enemy_{i}_killer_{j}"
                    )
                    killer.append(value)
                enemy["killer"] = killer

                enemy["lv"] = st.number_input(
                    "レベル(永遠戦線(ランキング)は100)",
                    min_value=1,
                    value=enemy["lv"],
                    key=f"enemy_{i}_lv"
                )

                enemy["unfavourables"] = st.multiselect(
                    "弱点属性",
                    lists.elements,
                    default=enemy["unfavourables"],
                    key=f"enemy_{i}_unfavourables"
                )

                enemy["favourables"] = st.multiselect(
                    "耐性属性",
                    lists.elements,
                    default=enemy["favourables"],
                    key=f"enemy_{i}_favourables"
                )

                enemy["yangdefsta"] = st.number_input(
                    "陽防ステータス",
                    min_value=1,
                    value=enemy["yangdefsta"],
                    key=f"enemy_{i}_yangdefsta"
                )

                enemy["yindefsta"] = st.number_input(
                    "陰防ステータス",
                    min_value=1,
                    value=enemy["yindefsta"],
                    key=f"enemy_{i}_yindefsta"
                )

                enemy["favup"] = st.number_input(
                    "有利属性から受けるダメージを_(%)アップ(能力)",
                    min_value=0,
                    value=enemy["favup"],
                    key=f"enemy_{i}_favup"
                )

                enemy["favcut"] = st.number_input(
                    "有利属性から受けるダメージを_(%)ダウン(能力)",
                    min_value=0,
                    value=enemy["favcut"],
                    key=f"enemy_{i}_favcut"
                )

                enemy["unfavup"] = st.number_input(
                    "不利属性から受けるダメージを_(%)アップ(能力)",
                    min_value=0,
                    value=enemy["unfavup"],
                    key=f"enemy_{i}_unfavup"
                )

                enemy["unfavcut"] = st.number_input(
                    "不利属性から受けるダメージを_(%)ダウン(能力)",
                    min_value=0,
                    value=enemy["unfavcut"],
                    key=f"enemy_{i}_unfavcut"
                )

                enemy["fullbreak"] = st.selectbox(
                    "fullbreak状態?",
                    lists.yesnos,
                    key=f"enemy_{i}_fullbreak"
                )

                enemy["poison"] = st.number_input(
                    "攻撃時毒霧枚数(能力欄に毒霧に関する記述があれば0)",
                    min_value=0,
                    value=enemy["poison"],
                    step=1,
                    key=f"enemy_{i}_poison"
                )

                enemy["burn"] = st.number_input(
                    "攻撃時燃焼枚数(能力欄に燃焼に関する記述があれば0)",
                    min_value=0,
                    value=enemy["burn"],
                    step=1,
                    key=f"enemy_{i}_burn"
                )

                enemy["agibuff"] = st.number_input(
                    "速力バフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["agibuff"],
                    step=1,
                    key=f"enemy_{i}_agibuff"
                )

                enemy["yangatkbuff"] = st.number_input(
                    "陽攻バフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["yangatkbuff"],
                    step=1,
                    key=f"enemy_{i}_yangatkbuff"
                )

                enemy["yinatkbuff"] = st.number_input(
                    "陰攻バフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["yinatkbuff"],
                    step=1,
                    key=f"enemy_{i}_yinatkbuff"
                )

                enemy["yangdefbuff"] = st.number_input(
                    "陽防バフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["yangdefbuff"],
                    step=1,
                    key=f"enemy_{i}_yangdefbuff"
                )

                enemy["yangdefbuffeter"] = st.number_input(
                    "陽防バフ(永続)",
                    min_value=-10,
                    max_value=10,
                    value=enemy["yangdefbuffeter"],
                    step=1,
                    key=f"enemy_{i}_yangdefbuffeter"
                )

                enemy["yindefbuff"] = st.number_input(
                    "陰防バフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["yindefbuff"],
                    step=1,
                    key=f"enemy_{i}_yindefbuff"
                )

                enemy["yindefbuffeter"] = st.number_input(
                    "陰防バフ(永続)",
                    min_value=-10,
                    max_value=10,
                    value=enemy["yindefbuffeter"],
                    step=1,
                    key=f"enemy_{i}_yindefbuffeter"
                )

                enemy["cridefbuff"] = st.number_input(
                    "CRI防御バフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["cridefbuff"],
                    step=1,
                    key=f"enemy_{i}_cridefbuff"
                )

                enemy["cridefbuffeter"] = st.number_input(
                    "CRI防御バフ(永続)",
                    min_value=-10,
                    max_value=10,
                    value=enemy["cridefbuffeter"],
                    step=1,
                    key=f"enemy_{i}_cridefbuffeter"
                )

                enemy["criavobuff"] = st.number_input(
                    "CRI回避バフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["criavobuff"],
                    step=1,
                    key=f"enemy_{i}_criavobuff"
                )

                enemy["criavobuffeter"] = st.number_input(
                    "CRI回避バフ(永続)",
                    min_value=-10,
                    max_value=10,
                    value=enemy["criavobuffeter"],
                    step=1,
                    key=f"enemy_{i}_criavobuffeter"
                )

                enemy["yangdef2buff"] = st.number_input(
                    "陽防Ⅱバフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["yangdef2buff"],
                    step=1,
                    key=f"enemy_{i}_yangdef2buff"
                )

                enemy["yindef2buff"] = st.number_input(
                    "陰防Ⅱバフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["yindef2buff"],
                    step=1,
                    key=f"enemy_{i}_yindef2buff"
                )

                enemy["cridef2buff"] = st.number_input(
                    "CRI防御Ⅱバフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["cridef2buff"],
                    step=1,
                    key=f"enemy_{i}_cridef2buff"
                )

                enemy["criavo2buff"] = st.number_input(
                    "CRI回避Ⅱバフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["criavo2buff"],
                    step=1,
                    key=f"enemy_{i}_criavo2buff"
                )

                enemy["yangdefrev"] = st.number_input(
                    "逆相(陽防)(%)(例:C3アリス・マーガトロイドなら20)",
                    min_value=0,
                    value=enemy["yangdefrev"],
                    key=f"enemy_{i}_yangdefrev"
                )

                enemy["yindefrev"] = st.number_input(
                    "逆相(陰防)(例:C8<<饕餮尤魔なら20)",
                    min_value=0,
                    value=enemy["yindefrev"],
                    key=f"enemy_{i}_yindefrev"
                )

                enemy["concridef"] = st.number_input(
                    "響奏(CRI防御)(%)(例:ZSTH-0001霧雨魔理沙なら10*6=60)",
                    min_value=0,
                    value=enemy["concridef"],
                    key=f"enemy_{i}_concridef"
                )

                enemy["focusbuff"] = st.number_input(
                    "注目バフ",
                    min_value=-10,
                    max_value=10,
                    value=enemy["focusbuff"],
                    step=1,
                    key=f"enemy_{i}_focusbuff"
                )

                enemy["solobuff"] = st.number_input(
                    "単体耐性(単体耐性は+、全体耐性は-)",
                    min_value=-10,
                    max_value=10,
                    value=enemy["solobuff"],
                    step=1,
                    key=f"enemy_{i}_solobuff"
                )

                enemy["favupbuff"] = st.number_input(
                    "有利属性から受けるダメージを_(%)アップ(バフ)",
                    min_value=0,
                    value=enemy["favupbuff"],
                    key=f"enemy_{i}_favupbuff"
                )

                enemy["favcutbuff"] = st.number_input(
                    "有利属性から受けるダメージを_(%)ダウン(バフ)",
                    min_value=0,
                    value=enemy["favcutbuff"],
                    key=f"enemy_{i}_favcutbuff"
                )

                enemy["unfavupbuff"] = st.number_input(
                    "不利属性から受けるダメージを_(%)アップ(バフ)",
                    min_value=0,
                    value=enemy["unfavupbuff"],
                    key=f"enemy_{i}_unfavupbuff"
                )

                enemy["unfavcutbuff"] = st.number_input(
                    "不利属性から受けるダメージを_(%)ダウン(バフ)",
                    min_value=0,
                    value=enemy["unfavcutbuff"],
                    key=f"enemy_{i}_unfavcutbuff"
                )

                e_type_cuts = []
                st.subheader("弾種カット")

                for j, bullet_type in enumerate(lists.types):
                    default_value = dict(enemy["type_cuts"]).get(bullet_type, 0)

                    value = st.number_input(
                        f"{bullet_type}(%)",
                        min_value=0,
                        value=default_value,
                        key=f"e_{i}_type_cuts_{j}"
                    )
                    if value != 0:
                        e_type_cuts.append((bullet_type, value))

                enemy["type_cuts"] = e_type_cuts

                e_element_cuts = []
                st.subheader("属性カット")

                for j, bullet_element in enumerate(lists.elements):
                    default_value = dict(enemy["element_cuts"]).get(bullet_element, 0)

                    value = st.number_input(
                        f"{bullet_element}(%)",
                        min_value=0,
                        value=default_value,
                        key=f"e_{i}_element_cuts_{j}"
                    )
                    if value != 0:
                        e_element_cuts.append((bullet_element, value))

                enemy["element_cuts"] = e_element_cuts


    return st.session_state.enemies