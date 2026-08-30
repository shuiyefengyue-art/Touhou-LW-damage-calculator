import streamlit as st

st.title("東方LW ダメージ計算機")
st.write("by オマーン国際空港")

st.write("================================")
st.write("・実機で試したほうが大抵速いです。")
st.write("・全弾CRI前提の最大ダメージに加え、弾性弾などを考慮したCRI命中率で重みづけした期待値、CRI命中率が100%でないバレットにおいてCRIが発生しないとした最低値も同時に計算します。")
st.write("・バレットのヒット順が絡む条件、例えば攻撃中に敵がfullbreakする、バレット内効果でバフデバフが入る、などには対応していません。特に、敵の結界異常枚数はうまく設定してください。")
st.write("・敵の永続効果により、敵の能力欄自体が書き換わっている場合は入力に気を付けてください。")
st.write("・現在、最終の計算結果のみ小数点以下を切り捨てているため、実機とは少しずれた値が出力されます。仕様が分かり次第修正します。")
st.write("・PCで操作する場合、マウスのホイールによるスクロールが頻繁に効かなくなるので、画面端のスクロールバーを使ってください。すみま千円。")
st.write("================================")


# === リスト ===
types = ["通常弾","光弾","レーザー弾","肉弾","質量弾","御札弾","エネルギー弾","尖弾","斬撃","流体弾"]
elements = ["日","月","火","水","木","金","土","星","無"]
yangyins = ["陽気","陰気"]
soloalls = ["単体","全体"]
criaccuppers = ["弾性弾","精密弾","爆破弾"]
daikekkais = ["なし","早苗","神奈子","諏訪子","さとり","こいし"]
yesnos = ["いいえ","はい"]


# ===== 計算用関数 =====
# 能力計算
def statusfactor(firstbuff,firstbuffeter,secondbuff):
    raw1buff = firstbuff + firstbuffeter
    if raw1buff < -10:
        buff1 = -10 + (raw1buff + 10) / 3
    elif raw1buff <= 10:
        buff1 = raw1buff
    else:
        buff1 = 10 + (raw1buff - 10) / 3

    buff2 = secondbuff


    if buff1 < 0:
        buff1factor = 1 / (1 + 0.3 * (-buff1))
    else:
        buff1factor = 1 + 0.3 * buff1

    if buff2 < 0:
        buff2factor = 1 / (1 + 0.3 * (-buff2))
    else:
        buff2factor = 1 + 0.3 * buff2


    return buff1factor * buff2factor

# CRI攻撃計算
def crifactor(a_firstbuff,e_firstbuff,a_firstbuffeter,e_firstbuffeter,a_secondbuff,e_secondbuff):
    raw1buff = max(-10, min(10, a_firstbuff - e_firstbuff)) + max(-10, min(10, a_firstbuffeter - e_firstbuffeter))
    if raw1buff < -10:
        buff1 = -10 + (raw1buff + 10) / 3
    elif raw1buff <= 10:
        buff1 = raw1buff
    else:
        buff1 = 10 + (raw1buff - 10) / 3
    
    buff2 = max(-10, min(10, a_secondbuff - e_secondbuff))


    if buff1 < 0:
        buff1factor = 1 / (1 + 0.3 * (-buff1))
    else:
        buff1factor = 1 + 0.3 * buff1

    if buff2 < 0:
        buff2factor = 1 / (1 + 0.3 * (-buff2))
    else:
        buff2factor = 1 + 0.3 * buff2


    return 1 + buff1factor * buff2factor

# 命中系計算
def accfactor(a_firstbuff,e_firstbuff,a_firstbuffeter,e_firstbuffeter,a_secondbuff,e_secondbuff):
    raw1buff = max(-10, min(10, a_firstbuff - e_firstbuff)) + max(-10, min(10, a_firstbuffeter - e_firstbuffeter))
    if raw1buff < -10:
        buff1 = -10 + (raw1buff + 10) / 3
    elif raw1buff <= 10:
        buff1 = raw1buff
    else:
        buff1 = 10 + (raw1buff - 10) / 3
    
    buff2 = max(-10, min(10, a_secondbuff - e_secondbuff))

    
    if buff1 < 0:
        buff1factor = 1 / (1 + 0.2 * (-buff1))
    else:
        buff1factor = 1 + 0.2 * buff1

    if buff2 < 0:
        buff2factor = 1 / (1 + 0.2 * (-buff2))
    else:
        buff2factor = 1 + 0.2 * buff2


    return buff1factor * buff2factor

# 弾性&爆破弾CRI命中補正値
def elast_blast(rawcriacc,e_yang1,e_yin1):
    if e_yang1 + e_yin1 < 0:
        return 0
    else:
        return (100 - rawcriacc) * (e_yang1 + e_yin1) / 20

# 精密弾CRI命中補正値
def preci(rawcriacc,e_agi):
    if e_agi < 0:
        return 0
    else:
        return (100 - rawcriacc) * e_agi / 10

# 注目補正値
def calc_focusfactor(f):
    if f < 0:
        return (1 / (1 + 0.3 * (-f))) ** 1.5
    else:
        return (1 + 0.3 * f) ** 3


# ===== 入力 =====
# === ターン強化 ===
st.header("ターン強化")

t = st.number_input(
    "このWAVEが始まって何ターン目？",
    min_value=1,
    value=1,
    step=1
)

# === 使用スペカ情報 ===
st.header("使用スペカ情報")

# 単体or全体
spell_soloall = st.selectbox(
    "単体or全体",
    soloalls
)

# スペカ&ショットレベル補正
spell_lv = st.number_input(
    "スペカ&ショットレベル補正(Lossy's JournalのLV Multの値。新キャラでまだ反映されてないなら、とりあえず30でいいと思います。)(%)",
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
        "mirror": 0
    })

if st.button("- 最後に追加したバレットを削除"):
    if st.session_state.bullets:
        st.session_state.bullets.pop()
        st.rerun()

for i, bullet in enumerate(st.session_state.bullets, 1):
     with st.expander(f"{i} 段目", expanded = False):

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
            types,
            key=f"bullet_{i}_type"
        )

        bullet["element"] = st.selectbox(
            "属性",
            elements,
            key=f"bullet_{i}_element"
        )

        bullet["yangyin"] = st.selectbox(
            "陰陽",
            yangyins,
            key=f"bullet_{i}_yangyin"
        )

        bullet["criaccupper"] = st.multiselect(
            "CRI命中上乗せ弾",
            criaccuppers,
            default=bullet["criaccupper"],
            key=f"bullet_{i}_criaccupper"
        )

        bullet["mirror"] = st.selectbox(
            "鏡面弾?",
            yesnos,
            key=f"bullet_{i}_mirror"
        )

# 絵札弾種補正
st.subheader("弾種補正(絵札)")
spell_card_type_buffs = []
for i, bullet_type in enumerate(types):
    value = st.number_input(
        f"{bullet_type}(%)",
        min_value=0,
        value=0,
        key=f"card_type_buff_{i}"
    )

    if value != 0:
        spell_card_type_buffs.append((bullet_type, value))

# 絵札属性補正
st.subheader("属性補正(絵札)")
spell_card_element_buffs = []
for i, bullet_element in enumerate(elements):
    value = st.number_input(
        f"{bullet_element}(%)",
        min_value=0,
        value=0,
        key=f"card_element_buff_{i}"
    )

    if value != 0:
        spell_card_element_buffs.append((bullet_element, value))


# ===== 攻撃側の状態 =====
st.header("攻撃側の状態")

# ステータス&能力
with st.expander("ステータス&能力",expanded = False):
    a_lv = st.number_input(
        "レベル(転生キャラなら+40)",
        min_value=1,
        value=100
    )

    a_maxHP = st.number_input(
        "最大HP(絵札補正を足した値)",
        min_value=1,
        value=5000
    )

    a_agista = st.number_input(
        "速力ステータス(絵札補正を足した値)",
        min_value=1,
        value=1500
    )

    a_yangatksta = st.number_input(
        "陽攻ステータス(絵札補正を足した値)",
        min_value=1,
        value=1500
    )

    a_yinatksta = st.number_input(
        "陰攻ステータス(絵札補正を足した値)",
        min_value=1,
        value=1500
    )

    a_yangdefsta = st.number_input(
        "陽防ステータス(絵札補正を足した値)",
        min_value=1,
        value=1500
    )

    a_yindefsta = st.number_input(
        "陰防ステータス(絵札補正を足した値)",
        min_value=1,
        value=1500
    )

    a_effup = st.number_input(
        "有利属性に与えるダメージを_(%)アップ(能力)",
        min_value=0,
        value=0
    )

    a_effdown = st.number_input(
        "有利属性に与えるダメージを_(%)ダウン(能力)",
        min_value=0,
        value=0
    )

    a_resup = st.number_input(
        "不利属性に与えるダメージを_(%)アップ(能力)",
        min_value=0,
        value=0
    )

    a_resdown = st.number_input(
        "不利属性に与えるダメージを_(%)ダウン(能力)",
        min_value=0,
        value=0
    )

    a_currentHP = st.number_input(
        "ターン開始時HP",
        min_value=1,
        value=5000
    )

    a_power = st.number_input(
        "ターン開始時霊力",
        min_value=0.00,
        value=5.00
    )

    a_graze = st.number_input(
        "ターン開始時結界数",
        min_value=1,
        value=5
    )

    a_freeze = st.number_input(
        "攻撃時凍結枚数(能力欄に毒霧に関する記述があれば0)",
        min_value=0,
        value=0,
        step=1
    )

    a_poison = st.number_input(
        "攻撃時毒霧枚数(能力欄に毒霧に関する記述があれば0)",
        min_value=0,
        value=0,
        step=1
    )

    a_burn = st.number_input(
        "攻撃時燃焼枚数(能力欄に燃焼に関する記述があれば0)",
        min_value=0,
        value=0,
        step=1
    )

# バフ
with st.expander("バフ(能力欄の結界異常バフを加算した値を入力)", expanded = False):
    a_agibuff = st.number_input(
        "速力バフ",
        min_value=-10,
        max_value=10,
        value=10,
        step=1
    )

    a_agibuffeter = st.number_input(
        "速力バフ(永続)",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_yangatkbuff = st.number_input(
        "陽攻バフ",
        min_value=-10,
        max_value=10,
        value=10,
        step=1
    )

    a_yangatkbuffeter = st.number_input(
        "陽攻バフ(永続)",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_yinatkbuff = st.number_input(
        "陰攻バフ",
        min_value=-10,
        max_value=10,
        value=10,
        step=1
    )

    a_yinatkbuffeter = st.number_input(
        "陰攻バフ(永続)",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_yangdefbuff = st.number_input(
        "陽防バフ",
        min_value=-10,
        max_value=10,
        value=10,
        step=1
    )
    
    a_yangdefbuffeter = st.number_input(
        "陽防バフ(永続)",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )
    
    a_yindefbuff = st.number_input(
        "陰防バフ",
        min_value=-10,
        max_value=10,
        value=10,
        step=1
    )
    
    a_yindefbuffeter = st.number_input(
        "陰防バフ(永続)",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_criatkbuff = st.number_input(
        "CRI攻撃バフ",
        min_value=-10,
        max_value=10,
        value=10,
        step=1
    )

    a_criatkbuffeter = st.number_input(
        "CRI攻撃バフ(永続)",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_criaccbuff = st.number_input(
        "CRI命中バフ",
        min_value=-10,
        max_value=10,
        value=10,
        step=1
    )
    
    a_criaccbuffeter = st.number_input(
        "CRI命中バフ(永続)",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_agi2buff = st.number_input(
        "速力Ⅱバフ",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_yangatk2buff = st.number_input(
        "陽攻Ⅱバフ",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_yinatk2buff = st.number_input(
        "陰攻Ⅱバフ",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_yangdef2buff = st.number_input(
        "陽防Ⅱバフ",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_yindef2buff = st.number_input(
        "陰防Ⅱバフ",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_criatk2buff = st.number_input(
        "CRI攻撃Ⅱバフ",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_criacc2buff = st.number_input(
        "CRI命中Ⅱバフ",
        min_value=-10,
        max_value=10,
        value=0,
        step=1
    )

    a_agiadd = st.number_input(
        "速力蓄積の値(小数点以下切り捨て)(例:○○ステ2615の70%を速力「に」上乗せしているなら、1830.5の小数点以下を切り捨てて1830)",
        min_value=0,
        value=0
    )

    a_agirev = st.number_input(
        "速力逆相の値(小数点以下切り捨て)",
        min_value=0,
        value=0
    )

    a_yangatkadd = st.number_input(
        "陽攻蓄積の値(小数点以下切り捨て)",
        min_value=0,
        value=0
    )

    a_yinatkadd = st.number_input(
        "陰攻蓄積の値(小数点以下切り捨て)",
        min_value=0,
        value=0
    )

    a_yangdefadd = st.number_input(
        "陽防蓄積の値(小数点以下切り捨て)",
        min_value=0,
        value=0
    )

    a_yindefadd = st.number_input(
        "陰防蓄積の値(小数点以下切り捨て)",
        min_value=0,
        value=0
    )

    a_effupbuff = st.number_input(
        "有利属性に与えるダメージを_(%)アップ(バフ)",
        min_value=0,
        value=0
    )

    a_resupbuff = st.number_input(
        "不利属性に与えるダメージを_(%)アップ(バフ)",
        min_value=0,
        value=0
    )

    a_type_buffs = []
    st.subheader("弾種補正(バフ)")
    for i, bullet_type in enumerate(types):
        value = st.number_input(
            f"{bullet_type}(%)",
            min_value=0,
            value=0,
            key=f"a_type_buff_{i}"
        )

        if value != 0:
            a_type_buffs.append((bullet_type, value))

    a_element_buffs = []
    st.subheader("属性補正(バフ)")
    for i, bullet_element in enumerate(elements):
        value = st.number_input(
            f"{bullet_element}(%)",
            min_value=0,
            value=0,
            key=f"a_element_buff_{i}"
        )

        if value !=0:
            a_element_buffs.append((bullet_element, value))

    a_HPtunk = st.number_input(
        "HP蓄力の基礎倍率(%)(例:F1霧雨魔理沙なら100)",
        min_value=0,
        value=0
    )

    a_powertunk = st.number_input(
        "霊力蓄力の基礎倍率(%)(例:Cz1#霧雨魔理沙なら25)",
        min_value=0,
        value=0
    )

    a_grazetunk = st.number_input(
        "結界蓄力の基礎倍率(%)(例:L80八雲藍なら20)",
        min_value=0,
        value=0
    )

    a_resdmg = st.number_input(
        "共鳴(ダメージアップ)(%)(例:LR1宇佐見蓮子、前衛4人なら20)",
        min_value=0,
        value=0
    )

    a_rescriacc = st.number_input(
        "共鳴(基礎CRI命中アップ)(%)",
        min_value=0,
        value=0
    )

    a_resagi = st.number_input(
        "共鳴(速力アップ)(%)",
        min_value=0,
        value=0
    )

    a_rescridmg = st.number_input(
        "共鳴(CRIダメージアップ)(%)",
        min_value=0,
        value=0
    )

    a_zoncridmg = st.number_input(
        "ゾーン(CRIダメージアップ)(%)(例:L10.1十六夜咲夜、チーム内LIVE2人なら20)",
        min_value=0,
        value=0
    )

    a_zonagi = st.number_input(
        "ゾーン(速力アップ)(%)",
        min_value=0,
        value=0
    )

    a_zoncriacc = st.number_input(
        "ゾーン(基礎CRI命中アップ)(%)",
        min_value=0,
        value=0
    )

    a_zondmg = st.number_input(
        "ゾーン(ダメージアップ)(%)",
        min_value=0,
        value=0
    )


# ===== 大結界 =====
st.header("大結界")
daikekkai = st.selectbox(
    "大結界",
    daikekkais,
    index=0
)


# ===== 敵側の状態 =====
st.header("敵側の状態")
st.write("デバフはマイナスで入力することに注意してください。")
if "enemies" not in st.session_state:
    st.session_state.enemies = []

if st.button("+ 敵を追加"):
    st.session_state.enemies.append({
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
        "focusbuff": 0,
        "solobuff": 0,
        "favupbuff": 0,
        "favcutbuff": 0,
        "unfavupbuff": 0,
        "unfavcutbuff": 0,
        "type_cuts": [],
        "element_cuts":[]
    })

if st.button("- 最後に追加した敵を削除"):
    if st.session_state.enemies:
        st.session_state.enemies.pop()
        st.rerun()

for i, enemy in enumerate(st.session_state.enemies):
    with st.expander(f"敵 {i + 1}", expanded = False):
        killer = []
        for j, bullet in enumerate(st.session_state.bullets, 1):
            value = st.selectbox(
                f"バレットの{j}段目は特攻範囲?",
                yesnos,
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
            elements,
            default=enemy["unfavourables"],
            key=f"enemy_{i}_unfavourables"
        )

        enemy["favourables"] = st.multiselect(
            "耐性属性",
            elements,
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
            yesnos,
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
            "陽防逆相(%)(例:C3アリス・マーガトロイドなら20)",
            min_value=0,
            value=enemy["yangdefrev"],
            key=f"enemy_{i}_yangdefrev"
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
        for j, bullet_type in enumerate(types):
            value = st.number_input(
                f"{bullet_type}(%)",
                min_value=0,
                value=0,
                key=f"e_{i}_type_cuts_{j}"
            )
        
            if value != 0:
                e_type_cuts.append((bullet_type, value))
        enemy["type_cuts"] = e_type_cuts

        e_element_cuts = []
        st.subheader("属性カット")
        for j, bullet_element in enumerate(elements):
            value = st.number_input(
                f"{bullet_element}(%)",
                min_value=0,
                value=0,
                key=f"e_{i}_element_cuts_{j}"
            )
                
            if value != 0:
                e_element_cuts.append((bullet_element, value))
        enemy["element_cuts"] = e_element_cuts


# =====各要素計算=====
# ターン強化
turnfactor = (t - 1) * (t - 2) / 870

# 速力(攻撃側)
a_agi = (
    (a_agista + a_agiadd + a_agirev)
    * 0.875 ** a_freeze
    * statusfactor(a_agibuff,a_agibuffeter,a_agi2buff)
    * (1 + a_resagi / 100)
    * (1 + a_zonagi / 100)
)

# 陽攻(攻撃側)
a_yangatk = (
    (a_yangatksta + a_yangatkadd)
    * 0.875 ** a_poison
    * statusfactor(a_yangatkbuff,a_yangatkbuffeter,a_yangatk2buff)
)
if daikekkai == "早苗":
    a_yangatk *= 1.5

# 陰攻(攻撃側)
a_yinatk = (
    (a_yinatksta + a_yinatkadd)
    * 0.875 ** a_burn
    * statusfactor(a_yinatkbuff,a_yinatkbuffeter,a_yinatk2buff)
)

# 陽防(攻撃側)
a_yangdef = (
    (a_yangdefsta + a_yangdefadd)
    * 0.875 ** a_poison
    * statusfactor(a_yangdefbuff,a_yangdefbuffeter,a_yangdef2buff)
)
if daikekkai == "神奈子":
    a_yangdef *= 1.3

# 陰防(攻撃側)
a_yindef = (
    (a_yindefsta + a_yindefadd)
    * 0.875 ** a_burn
    * statusfactor(a_yindefbuff,a_yindefbuffeter,a_yindef2buff)
)

# 蓄力
a_tunk = (
    1
    + (a_HPtunk * (a_currentHP / a_maxHP) / 100)
    + (a_powertunk * a_power / 100)
    + (a_grazetunk * a_graze / 100)
)

calc_results = {}
for ei, enemy in enumerate(st.session_state.enemies, 1):
    e_killer = enemy["killer"]
    e_yangdefsta = enemy["yangdefsta"]
    e_yindefsta = enemy["yindefsta"]
    e_agibuff = enemy["agibuff"]
    e_yangatkbuff = enemy["yangatkbuff"]
    e_yinatkbuff = enemy["yinatkbuff"]
    e_yangdefbuff = enemy["yangdefbuff"]
    e_yindefbuff = enemy["yindefbuff"]
    e_yangdef2buff = enemy["yangdef2buff"]
    e_yindef2buff = enemy["yindef2buff"]

    if enemy["fullbreak"] == "はい":
        e_yangdefsta /= 4
        e_yindefsta /= 4
        e_agibuff = 0
        e_yangatkbuff = 0
        e_yinatkbuff = 0
        e_yangdefbuff = 0
        e_yindefbuff = 0
        e_yangdef2buff = 0
        e_yindef2buff = 0

    # 陽防(敵)
    e_yangdef = (
        e_yangdefsta
        * 0.875 ** enemy["poison"]
        * statusfactor(e_yangdefbuff,enemy["yangdefbuffeter"],e_yangdef2buff)
        * (1 - enemy["yangdefrev"] / 100)
    )
    if daikekkai == "神奈子":
        e_yangdef *= 0.7

    # 陰防(敵)
    e_yindef = (
        e_yindefsta
        * 0.875 ** enemy["burn"]
        * statusfactor(e_yindefbuff,enemy["yindefbuffeter"],e_yindef2buff)
    )

    # CRI補正
    criatk = (
        crifactor(a_criatkbuff,enemy["cridefbuff"],a_criatkbuffeter,enemy["cridefbuffeter"],a_criatk2buff,enemy["cridef2buff"])
        * (1 + a_rescridmg / 100)
        * (1 + a_zoncridmg / 100)
    )
    if daikekkai == "さとり":
        criatk *= 1.5
    if daikekkai == "こいし":
        criatk *= 1.6

    #注目補正値
    total_focus = sum(calc_focusfactor(e["focusbuff"]) for e in st.session_state.enemies)
    focusfactor = calc_focusfactor(enemy["focusbuff"])
    if spell_soloall == "単体":
        distribution = 1
    else:
        distribution = focusfactor * len(st.session_state.enemies) / total_focus

    # 単体耐性補正
    if spell_soloall == "単体":
        if enemy["solobuff"] < 0:
            solofactor = 1 + 0.3 * (-enemy["solobuff"])
        else:
            solofactor = 1 / (1 + 0.05 * enemy["solobuff"])
    else:
        if enemy["solobuff"] < 0:
            solofactor = 1 / (1 + 0.3 * (-enemy["solobuff"]))
        else:
            solofactor = 1 + 0.05 * enemy["solobuff"]

    for bi, bullet in enumerate(st.session_state.bullets, 1):
        b_power = bullet["power"]
        b_rawcriacc = bullet["rawcriacc"]

        if daikekkai == "諏訪子":
            b_power *= 1.6

        if e_killer[bi - 1] == "はい":
            b_rawcriacc = 100

        # CRI命中率
        criacc_bonus = 0

        if "弾性弾" in bullet["criaccupper"]:
            criacc_bonus += elast_blast(
                b_rawcriacc,
                e_yangatkbuff,
                e_yinatkbuff
            )

        if "爆破弾" in bullet["criaccupper"]:
            criacc_bonus += elast_blast(
                b_rawcriacc,
                e_yangdefbuff + enemy["yangdefbuffeter"],
                e_yindefbuff + enemy["yindefbuffeter"]
            )

        if "精密弾" in bullet["criaccupper"]:
            criacc_bonus += preci(
                b_rawcriacc,
                e_agibuff
            )

        criacc = max(
            0,
            min(
                100,
                (
                    b_rawcriacc
                    + a_rescriacc
                    + a_zoncriacc
                    + criacc_bonus
                )
                * accfactor(
                    a_criaccbuff,
                    enemy["criavobuff"],
                    a_criaccbuffeter,
                    enemy["criavobuffeter"],
                    a_criacc2buff,
                    enemy["criavo2buff"]
                )
            )
        )

        # 弾種&属性補正
        if bullet["element"] in enemy["unfavourables"]:
            affinity = (2
                        * (1 + (a_effup - a_effdown + a_effupbuff) / 100)
                        * (1 + (enemy["unfavup"] - enemy["unfavcut"] + enemy["unfavupbuff"] - enemy["unfavcutbuff"]) / 100)
            )
        elif bullet["element"] in enemy["favourables"]:
            affinity = (0.5
                        * (1 + (a_resup - a_resdown + a_resupbuff) / 100)
                        * (1 + (enemy["favup"] - enemy["favcut"] + enemy["favupbuff"] - enemy["favcutbuff"]) / 100)
            )
        else:
            affinity = 1

        # 弾種&属性補正
        card_bullet_type_bonus = max((v for t, v in spell_card_type_buffs if t == bullet["type"]), default=0)
        card_bullet_element_bonus = max((v for e, v in spell_card_element_buffs if e == bullet["element"]), default=0)
        buff_bullet_type_bonus = max((v for t, v in a_type_buffs if t == bullet["type"]), default=0)
        buff_bullet_element_bonus = max((v for e, v in a_element_buffs if e == bullet["element"]), default=0)

        typebonus = (card_bullet_type_bonus + buff_bullet_type_bonus) / 100
        elementbonus = (card_bullet_element_bonus + buff_bullet_element_bonus) / 100

        # 弾種&属性カット
        typecut = max((v for t, v in enemy["type_cuts"] if t == bullet["type"]), default=0)
        elementcut = max((v for e, v in enemy["element_cuts"] if e == bullet["element"]), default=0)

        dmgcut = max(typecut, elementcut) / 100

        calc_results[(ei, bi)] = {
            "enemy_index": ei,
            "bullet_index": bi,
            "e_yangdef": e_yangdef,
            "e_yindef": e_yindef,
            "criatk": criatk,
            "distribution": distribution,
            "solofactor": solofactor,
            "b_power": b_power,
            "criacc": criacc,
            "affinity": affinity,
            "typebonus": typebonus,
            "elementbonus": elementbonus,
            "dmgcut": dmgcut
        }


# =====ダメージ計算=====
dmg_results = {}

for ei, enemy in enumerate(st.session_state.enemies, 1):
    for bi, bullet in enumerate(st.session_state.bullets, 1):
        result = calc_results[(ei, bi)]

        # 陰陽
        if bullet["mirror"] == "いいえ":
            if bullet["yangyin"] == "陽気":
                atk = a_yangatk
                sdef = a_yangdef
                edef = result["e_yangdef"]
            else:
                atk = a_yinatk
                sdef = a_yindef
                edef = result["e_yindef"]
        else:
            if bullet["yangyin"] == "陽気":
                atk = a_yangatk
                sdef = a_yangdef
                edef = result["e_yindef"]
            else:
                atk = a_yinatk
                sdef = a_yindef
                edef = result["e_yangdef"]


        # 各バレットダメージ(理論値)
        if result["criacc"] != 0:
            maxdmg = (
                result["b_power"]
                * (
                    atk
                    + a_agi * bullet["slice"] / 100
                    + sdef * bullet["hard"] / 100
                )
                / edef
                * a_lv * 100 / enemy["lv"]
                * 0.4
                * (1 + spell_lv / 100)
                * result["affinity"]
                * (1 + result["typebonus"] + result["elementbonus"])
                * (1 - result["dmgcut"])
                * result["criatk"]
                * a_tunk
                * (1 + a_resdmg / 100)
                * (1 + a_zondmg / 100)
                * result["distribution"]
                * result["solofactor"]
                / (1 + turnfactor)
            )
        else:
            maxdmg = (
                result["b_power"]
                * (
                    atk
                    + a_agi * bullet["slice"] / 100
                    + sdef * bullet["hard"] / 100
                )
                / edef
                * a_lv * 100 / enemy["lv"]
                * 0.4
                * (1 + spell_lv / 100)
                * result["affinity"]
                * (1 + result["typebonus"] + result["elementbonus"])
                * (1 - result["dmgcut"])
                * a_tunk
                * (1 + a_resdmg / 100)
                * (1 + a_zondmg / 100)
                * result["distribution"]
                * result["solofactor"]
                / (1 + turnfactor)
            )

        # 各バレットダメージ（最低値）
        if result["criacc"] == 100:
            mindmg = maxdmg * 0.99
        else:
            mindmg = (
                result["b_power"]
                * (
                    atk
                    + a_agi * bullet["slice"] / 100
                    + sdef * bullet["hard"] / 100
                )
                / edef
                * a_lv * 100 / enemy["lv"]
                * 0.4
                * (1 + spell_lv / 100)
                * result["affinity"]
                * (1 + result["typebonus"] + result["elementbonus"])
                * (1 - result["dmgcut"])
                * a_tunk
                * (1 + a_resdmg / 100)
                * (1 + a_zondmg / 100)
                * result["distribution"]
                * result["solofactor"]
                / (1 + turnfactor)
                * 0.99
            )

        # 各バレットダメージ(期待値)
        expdmg = (
                (
                    result["b_power"]
                * (
                    atk
                    + a_agi * bullet["slice"] / 100
                    + sdef * bullet["hard"] / 100
                )
                / edef
                * a_lv * 100 / enemy["lv"]
                * 0.4
                * (1 + spell_lv / 100)
                * result["affinity"]
                * (1 + result["typebonus"] + result["elementbonus"])
                * (1 - result["dmgcut"])
                * result["criatk"]
                * a_tunk
                * (1 + a_resdmg / 100)
                * (1 + a_zondmg / 100)
                * result["distribution"]
                * result["solofactor"]
                / (1 + turnfactor) 
                * result["criacc"] / 100
                * 0.995
                )
                + (
                    result["b_power"]
                * (
                    atk
                    + a_agi * bullet["slice"] / 100
                    + sdef * bullet["hard"] / 100
                )
                / edef
                * a_lv * 100 / enemy["lv"]
                * 0.4
                * (1 + spell_lv / 100)
                * result["affinity"]
                * (1 + result["typebonus"] + result["elementbonus"])
                * (1 - result["dmgcut"])
                * a_tunk
                * (1 + a_resdmg / 100)
                * (1 + a_zondmg / 100)
                * result["distribution"]
                * result["solofactor"]
                / (1 + turnfactor) 
                * (100 - result["criacc"]) / 100
                * 0.995
                )
        )

        maxdamage = maxdmg * bullet["numbers"]
        expdamage = expdmg * bullet["numbers"]
        mindamage = mindmg * bullet["numbers"]

        dmg_results[(ei, bi)] = {
            "maxdamageperone": maxdmg,
            "expdamageperone": expdmg,
            "mindamageperone": mindmg,
            "maxdamage": maxdmg * bullet["numbers"],
            "expdamage": expdmg * bullet["numbers"],
            "mindamage": mindmg * bullet["numbers"],
            "criacc": result["criacc"],

            "b_power": result["b_power"],
            "atk": atk,
            "agi": a_agi,
            "slice": bullet["slice"],
            "a_def": sdef,
            "hard": bullet["hard"],
            "e_def": edef,
            "a_lv": a_lv,
            "e_lv": enemy["lv"],
            "s_lv": spell_lv,
            "affinity": result["affinity"],
            "typebonus": result["typebonus"],
            "elementbonus": result["elementbonus"],
            "cut": result["dmgcut"],
            "criatk": result["criatk"],
            "tunk": a_tunk,
            "resdmg": a_resdmg,
            "zondmg": a_zondmg,
            "distribution": result["distribution"],
            "solo": result["solofactor"],
            "turn": 1 + turnfactor
        }


# ===== ダメージ計算結果の表示 =====
if st.button("ダメージを計算", type="primary"):
    if not st.session_state.enemies:
        st.warning("敵を1体以上追加してください。")
    elif not st.session_state.bullets:
        st.warning("バレットを1段以上追加してください。")
    else:
        st.header("ダメージ結果")
        # ===== 全敵合計 =====
        all_max = sum(
            dmg_results[(ei, bi)]["maxdamage"]
            for ei in range(1, len(st.session_state.enemies) + 1)
            for bi in range(1, len(st.session_state.bullets) + 1)
        )

        all_exp = sum(
            dmg_results[(ei, bi)]["expdamage"]
            for ei in range(1, len(st.session_state.enemies) + 1)
            for bi in range(1, len(st.session_state.bullets) + 1)
        )

        all_min = sum(
            dmg_results[(ei, bi)]["mindamage"]
            for ei in range(1, len(st.session_state.enemies) + 1)
            for bi in range(1, len(st.session_state.bullets) + 1)
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("最大(乱数は1.00)", f"{all_max:,.0f}")

        with col2:
            st.metric("期待値", f"{all_exp:,.0f}")

        with col3:
            st.metric("最低(乱数は0.99)", f"{all_min:,.0f}")

        st.divider()

        for ei, enemy in enumerate(st.session_state.enemies, 1):
            st.subheader(f"敵 {ei}")

            # 各敵の3値
            total_max = sum(
                dmg_results[(ei, bi)]["maxdamage"]
                for bi in range(1, len(st.session_state.bullets) + 1)
            )
            total_exp = sum(
                dmg_results[(ei, bi)]["expdamage"]
                for bi in range(1, len(st.session_state.bullets) + 1)
            )
            total_min = sum(
                dmg_results[(ei, bi)]["mindamage"]
                for bi in range(1, len(st.session_state.bullets) + 1)
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("最大(乱数は1.00)", f"{total_max:,.0f}")
            with col2:
                st.metric("期待値(乱数は0.995)", f"{total_exp:,.0f}")
            with col3:
                st.metric("最低(乱数は0.99)", f"{total_min:,.0f}")

            # 各段の詳細
            with st.expander("各段の詳細"):
                for bi, bullet in enumerate(st.session_state.bullets, 1):
                    result = dmg_results[(ei, bi)]
                    st.write(
                        f"**{bi}段目**　"
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

            st.divider()


# ===== 計算要素の確認 =====
if st.button("計算要素を確認"):
    if not st.session_state.enemies:
        st.warning("敵を1体以上追加してください。")
    elif not st.session_state.bullets:
        st.warning("バレットを1段以上追加してください。")
    else:
        st.header("計算要素の確認")
        for ei, enemy in enumerate(st.session_state.enemies, 1):
            st.subheader(f"敵 {ei}")
            for bi, bullet in enumerate(st.session_state.bullets, 1):

                debug = dmg_results[(ei, bi)]

                with st.expander(f"{bi}段目"):

                    st.write(f"b_power = {debug['b_power']}")
                    st.write(f"atk = {debug['atk']}")
                    st.write(f"agi = {debug['agi']}")
                    st.write(f"slice = {debug['slice']}%")
                    st.write(f"a_def = {debug['a_def']}")
                    st.write(f"hard = {debug['hard']}%")
                    st.write(f"e_def = {debug['e_def']}")
                    st.write(f"a_lv = {debug['a_lv']}")
                    st.write(f"e_lv = {debug['e_lv']}")
                    st.write(f"s_lv = {debug['s_lv']}%")
                    st.write(f"affinity = {debug['affinity']}")
                    st.write(f"typebonus = {debug['typebonus']}")
                    st.write(f"elementbonus = {debug['elementbonus']}")
                    st.write(f"cut = {debug['cut']}")
                    st.write(f"criatk = {debug['criatk']}")
                    st.write(f"tunk = {debug['tunk']}")
                    st.write(f"resdmg = {debug['resdmg']}%")
                    st.write(f"zondmg = {debug['zondmg']}%")
                    st.write(f"distribution = {debug['distribution']}")
                    st.write(f"solo = {debug['solo']}")
                    st.write(f"turn = {debug['turn']}")
