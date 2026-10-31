# ===== 攻撃側の状態 =====
import streamlit as st

import lists

def run():
    attacker = {
        "lv": 100,
        "maxHP": 5000,
        "agista": 2000,
        "yangatksta": 2000,
        "yinatksta": 2000,
        "yangdefsta": 2000,
        "yindefsta": 2000,
        "effup": 0,
        "effdown": 0,
        "resup": 0,
        "resdown": 0,
        "currentHP": 5000,
        "power": 5.00,
        "graze": 5,
        "freeze": 0,
        "poison": 0,
        "burn": 0,
        "agibuff": 10,
        "agibuffeter": 0,
        "yangatkbuff": 10,
        "yangatkbuffeter": 0,
        "yinatkbuff": 10,
        "yinatkbuffeter": 0,
        "yangdefbuff": 10,
        "yangdefbuffeter": 0,
        "yindefbuff": 10,
        "yindefbuffeter": 0,
        "criatkbuff": 10,
        "criatkbuffeter": 0,
        "criaccbuff": 10,
        "criaccbuffeter": 0,
        "agi2buff": 0,
        "yangatk2buff": 0,
        "yinatk2buff": 0,
        "yangdef2buff": 0,
        "yindef2buff": 0,
        "criatk2buff": 0,
        "criacc2buff": 0,
        "agiadd": 0,
        "agirev": 0,
        "yangatkadd": 0,
        "yinatkadd": 0,
        "yinatkrev": 0,
        "yangdefadd": 0,
        "yindefadd": 0,
        "effupbuff": 0,
        "resupbuff": 0,
        "type_buffs": [],
        "element_buffs": [],
        "HPtunk": 0,
        "powertunk": 0,
        "grazetunk": 0,
        "resdmg": 0,
        "rescriacc": 0,
        "resagi": 0,
        "rescridmg": 0,
        "zoncridmg": 0,
        "zonagi": 0,
        "zoncriacc": 0,
        "zondmg": 0,
        "uniagi": 0,
        "uniyangatk": 0,
        "budagi": 0,
        "budyangatk": 0
    }

    with st.container(height=450):
        attacker["lv"] = st.number_input(
            "レベル(転生キャラなら+40)",
            min_value=1,
            value=attacker["lv"]
        )

        attacker["maxHP"] = st.number_input(
            "最大HP(絵札補正を足した値)",
            min_value=1,
            value=attacker["maxHP"]
        )

        attacker["agista"] = st.number_input(
            "速力ステータス(絵札補正を足した値)",
            min_value=1,
            value=attacker["agista"]
        )

        attacker["yangatksta"] = st.number_input(
            "陽攻ステータス(絵札補正を足した値)",
            min_value=1,
            value=attacker["yangatksta"]
        )

        attacker["yinatksta"] = st.number_input(
            "陰攻ステータス(絵札補正を足した値)",
            min_value=1,
            value=attacker["yinatksta"]
        )

        attacker["yangdefsta"] = st.number_input(
            "陽防ステータス(絵札補正を足した値)",
            min_value=1,
            value=attacker["yangdefsta"]
        )

        attacker["yindefsta"] = st.number_input(
            "陰防ステータス(絵札補正を足した値)",
            min_value=1,
            value=attacker["yindefsta"]
        )

        attacker["effup"] = st.number_input(
            "有利属性に与えるダメージを_(%)アップ(能力)",
            min_value=0,
            value=attacker["effup"]
        )

        attacker["effdown"] = st.number_input(
            "有利属性に与えるダメージを_(%)ダウン(能力)",
            min_value=0,
            value=attacker["effdown"]
        )

        attacker["resup"] = st.number_input(
            "不利属性に与えるダメージを_(%)アップ(能力)",
            min_value=0,
            value=attacker["resup"]
        )

        attacker["resdown"] = st.number_input(
            "不利属性に与えるダメージを_(%)ダウン(能力)",
            min_value=0,
            value=attacker["resdown"]
        )

        attacker["currentHP"] = st.number_input(
            "ターン開始時HP",
            min_value=1,
            value=attacker["currentHP"]
        )

        attacker["power"] = st.number_input(
            "ターン開始時霊力",
            min_value=0.00,
            value=attacker["power"]
        )

        attacker["graze"] = st.number_input(
            "ターン開始時結界数",
            min_value=1,
            value=attacker["graze"]
        )

        attacker["freeze"] = st.number_input(
            "攻撃時凍結枚数(能力欄に毒霧に関する記述があれば0)",
            min_value=0,
            value=attacker["freeze"],
            step=1
        )

        attacker["poison"] = st.number_input(
            "攻撃時毒霧枚数(能力欄に毒霧に関する記述があれば0)",
            min_value=0,
            value=attacker["poison"],
            step=1
        )

        attacker["burn"] = st.number_input(
            "攻撃時燃焼枚数(能力欄に燃焼に関する記述があれば0)",
            min_value=0,
            value=attacker["burn"],
            step=1
        )

        attacker["agibuff"] = st.number_input(
            "速力バフ",
            min_value=-10,
            max_value=10,
            value=attacker["agibuff"],
            step=1
        )

        attacker["agibuffeter"] = st.number_input(
            "速力バフ(永続)",
            min_value=-10,
            max_value=10,
            value=attacker["agibuffeter"],
            step=1
        )

        attacker["yangatkbuff"] = st.number_input(
            "陽攻バフ",
            min_value=-10,
            max_value=10,
            value=attacker["yangatkbuff"],
            step=1
        )

        attacker["yangatkbuffeter"] = st.number_input(
            "陽攻バフ(永続)",
            min_value=-10,
            max_value=10,
            value=attacker["yangatkbuffeter"],
            step=1
        )

        attacker["yinatkbuff"] = st.number_input(
            "陰攻バフ",
            min_value=-10,
            max_value=10,
            value=attacker["yinatkbuff"],
            step=1
        )

        attacker["yinatkbuffeter"] = st.number_input(
            "陰攻バフ(永続)",
            min_value=-10,
            max_value=10,
            value=attacker["yinatkbuffeter"],
            step=1
        )

        attacker["yangdefbuff"] = st.number_input(
            "陽防バフ",
            min_value=-10,
            max_value=10,
            value=attacker["yangdefbuff"],
            step=1
        )

        attacker["yangdefbuffeter"] = st.number_input(
            "陽防バフ(永続)",
            min_value=-10,
            max_value=10,
            value=attacker["yangdefbuffeter"],
            step=1
        )

        attacker["yindefbuff"] = st.number_input(
            "陰防バフ",
            min_value=-10,
            max_value=10,
            value=attacker["yindefbuff"],
            step=1
        )

        attacker["yindefbuffeter"] = st.number_input(
            "陰防バフ(永続)",
            min_value=-10,
            max_value=10,
            value=attacker["yindefbuffeter"],
            step=1
        )

        attacker["criatkbuff"] = st.number_input(
            "CRI攻撃バフ",
            min_value=-10,
            max_value=10,
            value=attacker["criatkbuff"],
            step=1
        )

        attacker["criatkbuffeter"] = st.number_input(
            "CRI攻撃バフ(永続)",
            min_value=-10,
            max_value=10,
            value=attacker["criatkbuffeter"],
            step=1
        )

        attacker["criaccbuff"] = st.number_input(
            "CRI命中バフ",
            min_value=-10,
            max_value=10,
            value=attacker["criaccbuff"],
            step=1
        )

        attacker["criaccbuffeter"] = st.number_input(
            "CRI命中バフ(永続)",
            min_value=-10,
            max_value=10,
            value=attacker["criaccbuffeter"],
            step=1
        )

        attacker["agi2buff"] = st.number_input(
            "速力Ⅱバフ",
            min_value=-10,
            max_value=10,
            value=attacker["agi2buff"],
            step=1
        )

        attacker["yangatk2buff"] = st.number_input(
            "陽攻Ⅱバフ",
            min_value=-10,
            max_value=10,
            value=attacker["yangatk2buff"],
            step=1
        )

        attacker["yinatk2buff"] = st.number_input(
            "陰攻Ⅱバフ",
            min_value=-10,
            max_value=10,
            value=attacker["yinatk2buff"],
            step=1
        )

        attacker["yangdef2buff"] = st.number_input(
            "陽防Ⅱバフ",
            min_value=-10,
            max_value=10,
            value=attacker["yangdef2buff"],
            step=1
        )

        attacker["yindef2buff"] = st.number_input(
            "陰防Ⅱバフ",
            min_value=-10,
            max_value=10,
            value=attacker["yindef2buff"],
            step=1
        )

        attacker["criatk2buff"] = st.number_input(
            "CRI攻撃Ⅱバフ",
            min_value=-10,
            max_value=10,
            value=attacker["criatk2buff"],
            step=1
        )

        attacker["criacc2buff"] = st.number_input(
            "CRI命中Ⅱバフ",
            min_value=-10,
            max_value=10,
            value=attacker["criacc2buff"],
            step=1
        )

        attacker["agiadd"] = st.number_input(
            "速力蓄積の値(異種の「○○→速力」の合計。例:2818 * 0.7 + 2656 * 0.2 = 2503.8)",
            min_value=0,
            value=attacker["agiadd"]
        )

        attacker["agirev"] = st.number_input(
            "速力逆相の値",
            min_value=0,
            value=attacker["agirev"]
        )

        attacker["yangatkadd"] = st.number_input(
            "陽攻蓄積の値",
            min_value=0,
            value=attacker["yangatkadd"]
        )

        attacker["yinatkadd"] = st.number_input(
            "陰攻蓄積の値",
            min_value=0,
            value=attacker["yinatkadd"]
        )

        attacker["yinatkrev"] = st.number_input(
            "陰攻逆相の値",
            min_value=0,
            value=attacker["yinatkrev"]
        )

        attacker["yangdefadd"] = st.number_input(
            "陽防蓄積の値",
            min_value=0,
            value=attacker["yangdefadd"]
        )

        attacker["yindefadd"] = st.number_input(
            "陰防蓄積の値",
            min_value=0,
            value=attacker["yindefadd"]
        )

        attacker["effupbuff"] = st.number_input(
            "有利属性に与えるダメージを_(%)アップ(バフ)",
            min_value=0,
            value=attacker["effupbuff"]
        )

        attacker["resupbuff"] = st.number_input(
            "不利属性に与えるダメージを_(%)アップ(バフ)",
            min_value=0,
            value=attacker["resupbuff"]
        )

        a_type_buffs = []
        st.subheader("弾種補正(バフ)")

        for i, bullet_type in enumerate(lists.types):
            value = st.number_input(
                f"{bullet_type}(%)",
                min_value=0,
                value=0,
                key=f"a_type_buff_{i}"
            )
            if value != 0:
                a_type_buffs.append((bullet_type, value))

        attacker["type_buffs"] = a_type_buffs

        a_element_buffs = []
        st.subheader("属性補正(バフ)")

        for i, bullet_element in enumerate(lists.elements):
            value = st.number_input(
                f"{bullet_element}(%)",
                min_value=0,
                value=0,
                key=f"a_element_buff_{i}"
            )
            if value != 0:
                a_element_buffs.append((bullet_element, value))

        attacker["element_buffs"] = a_element_buffs

        attacker["HPtunk"] = st.number_input(
            "HP蓄力の基礎倍率(%)",
            min_value=0,
            value=attacker["HPtunk"]
        )

        attacker["powertunk"] = st.number_input(
            "霊力蓄力の基礎倍率(%)",
            min_value=0,
            value=attacker["powertunk"]
        )

        attacker["grazetunk"] = st.number_input(
            "結界蓄力の基礎倍率(%)",
            min_value=0,
            value=attacker["grazetunk"]
        )

        attacker["resdmg"] = st.number_input(
            "共鳴(ダメージアップ)(%)",
            min_value=0,
            value=attacker["resdmg"]
        )

        attacker["rescriacc"] = st.number_input(
            "共鳴(基礎CRI命中アップ)(%)",
            min_value=0,
            value=attacker["rescriacc"]
        )

        attacker["resagi"] = st.number_input(
            "共鳴(速力アップ)(%)",
            min_value=0,
            value=attacker["resagi"]
        )

        attacker["rescridmg"] = st.number_input(
            "共鳴(CRIダメージアップ)(%)",
            min_value=0,
            value=attacker["rescridmg"]
        )

        attacker["zoncridmg"] = st.number_input(
            "ゾーン(CRIダメージアップ)(%)",
            min_value=0,
            value=attacker["zoncridmg"]
        )

        attacker["zonagi"] = st.number_input(
            "ゾーン(速力アップ)(%)",
            min_value=0,
            value=attacker["zonagi"]
        )

        attacker["zoncriacc"] = st.number_input(
            "ゾーン(基礎CRI命中アップ)(%)",
            min_value=0,
            value=attacker["zoncriacc"]
        )

        attacker["zondmg"] = st.number_input(
            "ゾーン(ダメージアップ)(%)",
            min_value=0,
            value=attacker["zondmg"]
        )

        attacker["uniagi"] = st.number_input(
            "団結(速力)(%)",
            min_value=0,
            value=attacker["uniagi"]
        )

        attacker["uniyangatk"] = st.number_input(
            "団結(陽攻)(%)",
            min_value=0,
            value=attacker["uniyangatk"]
        )

        attacker["budagi"] = st.number_input(
            "バディコネクト(速力)(%)",
            min_value=0,
            value=attacker["budagi"]
        )
        
        attacker["budyangatk"] = st.number_input(
            "バディコネクト(陽攻)(%)",
            min_value=0,
            value=attacker["budyangatk"]
        )


        return attacker