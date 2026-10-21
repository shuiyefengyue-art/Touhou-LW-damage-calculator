def d_result(t,eb,a):
    calc_results = {}

    for (ei,bi), data in eb.items():
        if data["mirror"] == "いいえ":
            if data["yangyin"] == "陽気":
                atk = a["yangatk"]
                a_def = a["yangdef"]
                e_def = data["yangdef"]
            else:
                atk = a["yinatk"]
                a_def = a["yindef"]
                e_def = data["yindef"]
        else:
            if data["yangyin"] == "陽気":
                atk = a["yangatk"]
                a_def = a["yangdef"]
                e_def = data["yindef"]
            else:
                atk = a["yinatk"]
                a_def = a["yindef"]
                e_def = data["yangdef"]

        a_atk = atk + a["agi"] * data["slice"] / 100 + a_def * data["hard"] / 100

        # 各バレットダメージ(理論値)
        if data["criacc"] != 0:
            maxdmg = (
                data["power"]
                * a_atk
                / e_def
                * a["lv"] * 100 / data["e_lv"]
                * 0.4
                * (
                    1 
                    + data["s_lv"] / 100
                )
                * data["affinity"]
                * (
                    1 
                    + data["typebonus"] 
                    + data["elementbonus"]
                )
                * (
                    1 
                    - data["dmgcut"]
                )
                * data["criatk"]
                * a["tunk"]
                * (
                    1 
                    + a["resdmg"] / 100
                )
                * (
                    1 
                    + a["zondmg"] / 100
                )
                * data["focus"]
                * data["solo"]
                / t
            )
        else:
            maxdmg = (
                data["power"]
                * a_atk
                / e_def
                * a["lv"] * 100 / data["e_lv"]
                * 0.4
                * (
                    1 
                    + data["s_lv"] / 100
                )
                * data["affinity"]
                * (
                    1 
                    + data["typebonus"] 
                    + data["elementbonus"]
                )
                * (
                    1 
                    - data["dmgcut"]
                )
                * a["tunk"]
                * (
                    1 
                    + a["resdmg"] / 100
                )
                * (
                    1 
                    + a["zondmg"] / 100
                )
                * data["focus"]
                * data["solo"]
                / t
            )

        # 各バレットダメージ(期待値)
        expdmg = (
            (
                data["power"]
                * a_atk
                / e_def
                * a["lv"] * 100 / data["e_lv"]
                * 0.4
                * (
                    1 
                    + data["s_lv"] / 100
                )
                * data["affinity"]
                * (
                    1 
                    + data["typebonus"] 
                    + data["elementbonus"]
                )
                * (
                    1 
                    - data["dmgcut"]
                )
                * a["tunk"]
                * (
                    1 
                    + a["resdmg"] / 100
                )
                * (
                    1 
                    + a["zondmg"] / 100
                )
                * data["focus"]
                * data["solo"]
                / t
            )
            * (
                1
                + (
                    data["criatk"]
                    -1
                )
                * data["criacc"] / 100
            )
            * 0.995
        )
        
        # 各バレットダメージ（最低値）
        if data["criacc"] == 100:
            mindmg = maxdmg * 0.99
        else:
            mindmg = (
                data["power"]
                * a_atk
                / e_def
                * a["lv"] * 100 / data["e_lv"]
                * 0.4
                * (
                    1 
                    + data["s_lv"] / 100
                )
                * data["affinity"]
                * (
                    1 
                    + data["typebonus"] 
                    + data["elementbonus"]
                )
                * (
                    1 
                    - data["dmgcut"]
                )
                * a["tunk"]
                * (
                    1 
                    + a["resdmg"] / 100
                )
                * (
                    1 
                    + a["zondmg"] / 100
                )
                * data["focus"]
                * data["solo"]
                / t
            )
        
        maxdamage = maxdmg * data["numbers"]
        expdamage = expdmg * data["numbers"]
        mindamage = mindmg * data["numbers"]

        calc_results[(ei, bi)] = {
            "maxdamageperone": maxdmg,
            "expdamageperone": expdmg,
            "mindamageperone": mindmg,
            "maxdamage": maxdamage,
            "expdamage": expdamage,
            "mindamage": mindamage,
        
            "power": data["power"],
            "atk": a_atk,
            "def": e_def,
            "a_lv": a["lv"],
            "e_lv": data["e_lv"],
            "s_lv": data["s_lv"],
            "criacc": data["criacc"],
            "affinity": data["affinity"],
            "typebonus": data["typebonus"],
            "elementbonus": data["elementbonus"],
            "cut": data["dmgcut"],
            "criatk": data["criatk"],
            "tunk": a["tunk"],
            "resdmg": a["resdmg"],
            "zondmg": a["zondmg"],
            "focus": data["focus"],
            "solo": data["solo"],
            "turn": t
        }

        # 敵1体あたりダメージ
    calc_results2 = []

    for ei in sorted(set(e for e, bi in calc_results)):
        summax = sum(
            data["maxdamage"]
            for (e, bi), data in calc_results.items()
            if e == ei
        )

        sumexp = sum(
            data["expdamage"]
            for (e, bi), data in calc_results.items()
            if e == ei
        )

        summin = sum(
            data["mindamage"]
            for (e, bi), data in calc_results.items()
            if e == ei
        )

        sumdmg = {
            "enemy_index": ei,
            "summax": summax,
            "sumexp": sumexp,
            "summin": summin
        }

        calc_results2.append(sumdmg)

    # 合計ダメージ
    all_max = sum(
        data["maxdamage"]
        for data in calc_results.values()
    )

    all_exp = sum(
        data["expdamage"]
        for data in calc_results.values()
    )

    all_min = sum(
        data["mindamage"]
        for data in calc_results.values()
    )

    calc_results3 = {
        "allmax": all_max,
        "allexp": all_exp,
        "allmin": all_min
    }

    return calc_results, calc_results2, calc_results3