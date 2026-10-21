def a_result(a,d):
    import function

    # 速力
    a_agi = (
        (
            a["agista"]
            + a["agiadd"]
            + a["agirev"]
        )
        * 0.875 ** a["freeze"]
        * function.statusfactor(a["agibuff"],a["agibuffeter"],a["agi2buff"])
        * (
            1
            + a["resagi"] / 100
        )
        * (
            1
            + a["zonagi"] / 100
        )
    )

    # 陽攻
    a_yangatk = (
        (
            a["yangatksta"]
            + a["yangatkadd"]
        )
        * 0.875 ** a["poison"]
        * function.statusfactor(a["yangatkbuff"],a["yangatkbuffeter"],a["yangatk2buff"])
    )

    if d == "早苗":
        a_yangatk *= 1.5

    # 陰攻
    a_yinatk = (
        (
            a["yinatksta"]
            + a["yinatkadd"]
            + a["yinatkrev"]
        )
        * 0.875 ** a["burn"]
        * function.statusfactor(a["yinatkbuff"],a["yinatkbuffeter"],a["yinatk2buff"])
    )

    if d == "アリス":
        a_yinatk *= 3.0

    # 陽防
    a_yangdef = (
        (
            a["yangdefsta"]
            + a["yangdefadd"]
        )
        * 0.875 ** a["poison"]
        * function.statusfactor(a["yangdefbuff"],a["yangdefbuffeter"],a["yangdef2buff"])
    )

    if d == "神奈子":
        a_yangdef *= 1.3

    # 陰防
    a_yindef = (
        (
            a["yindefsta"]
            + a["yindefadd"]
        )
        * 0.875 ** a["burn"]
        * function.statusfactor(a["yindefbuff"],a["yindefbuffeter"],a["yindef2buff"])
    )

    # 蓄力
    a_tunk = (
        1
        + (
            a["HPtunk"]
            * a["currentHP"] / a["maxHP"]
            + a["powertunk"]
            * a["power"]
            + a["grazetunk"]
            * a["graze"]
        ) / 100
    )

    a_result = {
        "lv": a["lv"],
        "agi": a_agi,
        "yangatk": a_yangatk,
        "yinatk": a_yinatk,
        "yangdef": a_yangdef,
        "yindef": a_yindef,
        "tunk": a_tunk,
        "resdmg": a["resdmg"],
        "zondmg": a["zondmg"]
    }

    return a_result