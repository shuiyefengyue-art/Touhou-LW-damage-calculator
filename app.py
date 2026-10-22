import streamlit as st

st.set_page_config(layout="wide")


# 説明
import discription
discription.run()


# 入力
st.header("ターン強化")
from input import turn_input
t = turn_input.run()

st.header("使用スペカ情報")
with st.container(height=450):
    from input import spellcard_input_updated
    s = spellcard_input_updated.run()

left_col, right_col = st.columns(2)

with left_col:
    st.header("敵側の状態")
    st.write("デバフはマイナスで入力することに注意してください。")

    from input import enemy_input
    es = enemy_input.run()

with right_col:
    st.header("攻撃側の状態")

    from input import attacker_input
    a = attacker_input.run()

st.header("大結界&秘密封印")
from input import daikekkai_input
d = daikekkai_input.run()


#結果(要素)
if not s["bullets"]:
    st.info("先にバレットを1段以上追加してください。")
    st.stop()

from result import turn_result
turn = turn_result.t_result(t)

from result import enemybullet_result
enemies_bullets = enemybullet_result.es_bs_result(s,es,a,d)

from result import attacker_result
attacker = attacker_result.a_result(a,d)


# 結果(ダメージ)
from damage import dmgcalc
dmg_per_e_b, dmg_per_e, dmgall = dmgcalc.d_result(turn,enemies_bullets,attacker)

st.header("ダメージ")
if not es:
    st.warning("敵を1体以上追加してください。")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("最大(乱数は1.00)", f"{dmgall['allmax']:,.0f}")
    
    with col2:
        st.metric("期待値", f"{dmgall['allexp']:,.0f}")
    
    with col3:
        st.metric("最低(乱数は0.99)", f"{dmgall['allmin']:,.0f}")

    st.divider()

    for ei, e in enumerate(es):
        st.subheader(f"敵 {ei + 1}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "最大(乱数は1.00)",
                f"{dmg_per_e[ei]['summax']:,.0f}"
            )

        with col2:
            st.metric(
                "期待値(乱数は0.995)",
                f"{dmg_per_e[ei]['sumexp']:,.0f}"
            )

        with col3:
            st.metric(
                "最低(乱数は0.99)",
                f"{dmg_per_e[ei]['summin']:,.0f}"
            )

        with st.expander("各段の詳細"):
            for bi, b in enumerate(s["bullets"]):
                result = dmg_per_e_b[(ei, bi)]
                st.write(
                    f"**{bi + 1}段目**　"
                    f"CRI率: {result['criacc']:.1f}%"
                )
        
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(
                        f"最大: {result['maxdamageperone']:,.0f}"
                    )
                with col2:
                    st.write(
                        f"期待値: {result['expdamageperone']:,.0f}"
                    )
                with col3:
                    st.write(
                        f"最低: {result['mindamageperone']:,.0f}"
                    )


# ===== 計算要素の確認 =====
if st.button("計算要素を確認"):
    if not es:
        st.warning("敵を1体以上追加してください。")
    else:
        st.header("計算要素の確認")
        for ei, e in enumerate(es):
            st.subheader(f"敵 {ei + 1}")
            for bi, b in enumerate(s["bullets"]):

                debug = dmg_per_e_b[(ei, bi)]

                with st.expander(f"{bi + 1}段目"):

                    st.write(f"威力 = {debug['power']}")
                    st.write(f"攻撃力(攻撃側) = {debug['atk']}")
                    st.write(f"防御力(敵側) = {debug['def']}")
                    st.write(f"攻撃側レベル = {debug['a_lv']}")
                    st.write(f"敵側レベル = {debug['e_lv']}")
                    st.write(f"スペルレベル = {debug['s_lv']}%")
                    st.write(f"相性補正 = {debug['affinity']}")
                    st.write(f"弾種補正 = {debug['typebonus']}")
                    st.write(f"属性補正 = {debug['elementbonus']}")
                    st.write(f"ダメージカット = {debug['cut']}")
                    st.write(f"CRI補正 = {debug['criatk']}")
                    st.write(f"蓄力 = {debug['tunk']}")
                    st.write(f"共鳴(ダメージアップ) = {debug['resdmg']}%")
                    st.write(f"ゾーン(ダメージアップ) = {debug['zondmg']}%")
                    st.write(f"注目 = {debug['focus']}")
                    st.write(f"単体&全体補正 = {debug['solo']}")
                    st.write(f"ターン強化 = {debug['turn']}")