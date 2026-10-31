def es_bs_result(s,es,a,d):
    import function

    results = {}
    for ei, e in enumerate(es):
        e_yangdefsta = e["yangdefsta"]
        e_yindefsta = e["yindefsta"]
        e_agibuff = e["agibuff"]
        e_yangatkbuff = e["yangatkbuff"]
        e_yinatkbuff = e["yinatkbuff"]
        e_yangdefbuff = e["yangdefbuff"]
        e_yindefbuff = e["yindefbuff"]
        e_yangdef2buff = e["yangdef2buff"]
        e_yindef2buff = e["yindef2buff"]

        if e["fullbreak"] == "はい":
            e_yangdefsta /= 4
            e_yindefsta /= 4
            e_agibuff = 0
            e_yangatkbuff = 0
            e_yinatkbuff = 0
            e_yangdefbuff = 0
            e_yindefbuff = 0
            e_yangdef2buff = 0
            e_yindef2buff = 0

        # 陽防
        e_yangdef = (
            e_yangdefsta
            * 0.875 ** e["poison"]
            * function.statusfactor(e_yangdefbuff,e["yangdefbuffeter"],e_yangdef2buff)
            * (
                1
                - e["yangdefrev"] / 100
            )
        )

        if d == "神奈子":
            e_yangdef *= 0.7
        elif d == "白蓮":
            e_yangdef *= 0.55

        # 陰防
        e_yindef = (
            e_yindefsta
            * 0.875 ** e["burn"]
            * function.statusfactor(e_yindefbuff,e["yindefbuffeter"],e_yindef2buff)
            * (
                1
                - e["yindefrev"] / 100
            )
        )

        base_e_yangdef = e_yangdef
        base_e_yindef = e_yindef

        # CRI補正
        criatk = (
            (
                1
                + function.crifactor(a["criatkbuff"],e["cridefbuff"],a["criatkbuffeter"],e["cridefbuffeter"],a["criatk2buff"],e["cridef2buff"])
            )
            * (
                1
                + a["rescridmg"] / 100
            )
            * (
                1
                + a["zoncridmg"] / 100
            )
        )

        if d == "さとり":
            criatk *= 1.5
        elif d == "こいし":
            criatk *= 1.6

        # 注目補正
        total_focus = sum(function.calc_focusfactor(e["focusbuff"]) for e in es)
        focusfactor = function.calc_focusfactor(e["focusbuff"])
        if s["soloall"] == "単体":
            focus = 1
        else:
            focus = focusfactor * len(es) / total_focus

        # 単体耐性補正
        if s["soloall"] == "単体":
            if e["solobuff"] < 0:
                solo = 1 + 0.3 * (-e["solobuff"])
            else:
                solo = 1 / (1 + 0.05 * e["solobuff"])
        else:
            if e["solobuff"] < 0:
                solo = 1 / (1 + 0.3 * (-e["solobuff"]))
            else:
                solo = 1 + 0.05 * e["solobuff"]

        for bi, b in enumerate(s["bullets"]):
            e_yangdef = base_e_yangdef
            e_yindef = base_e_yindef
            b_power = b["power"]
            b_rawcriacc = b["rawcriacc"]

            if d == "諏訪子":
                b_power *= 1.6

            if b["penetrate"] == "はい":
                e_yangdef /= function.statusfactor(e_yangdefbuff,e["yangdefbuffeter"],e_yangdef2buff)
                e_yindef /= function.statusfactor(e_yindefbuff,e["yindefbuffeter"],e_yindef2buff)

            if e["killer"][bi] == "はい":
                b_rawcriacc = 100

            # CRI命中率
            criacc_bonus = 0
            
            if "弾性弾" in b["criaccupper"]:
                criacc_bonus += function.elast_blast(b_rawcriacc,e_yangatkbuff,e_yinatkbuff)
            
            if "爆破弾" in b["criaccupper"]:
                criacc_bonus += function.elast_blast(b_rawcriacc,e_yangdefbuff + e["yangdefbuffeter"],e_yindefbuff + e["yindefbuffeter"])
            
            if "精密弾" in b["criaccupper"]:
                criacc_bonus += function.preci(b_rawcriacc,e_agibuff)
            
            criacc = max(
                0,
                min(
                    100,
                    (
                        b_rawcriacc
                        + a["rescriacc"]
                        + a["zoncriacc"]
                        + criacc_bonus
                    )
                    * function.accfactor(a["criaccbuff"],e["criavobuff"],a["criaccbuffeter"],e["criavobuffeter"],a["criacc2buff"],e["criavo2buff"])
                )
            )

            # 弱点補正
            if b["element"] in e["unfavourables"]:
                affinity = (
                    2
                    * (
                        1 
                        + (
                            a["effup"]
                            - a["effdown"] 
                            + a["effupbuff"]
                        ) / 100
                    )
                    * (
                        1 
                        + (
                            e["unfavup"] 
                            - e["unfavcut"] 
                            + e["unfavupbuff"] 
                            - e["unfavcutbuff"]
                        ) / 100
                    )
                )
            elif b["element"] in e["favourables"]:
                affinity = (
                    0.5
                    * (
                        1 
                        + (
                            a["resup"] 
                            - a["resdown"] 
                            + a["resupbuff"]
                        ) / 100
                    )
                    * (
                        1 
                        + (
                            e["favup"] 
                            - e["favcut"] 
                            + e["favupbuff"] 
                            - e["favcutbuff"]
                        ) / 100
                    )
                )
            else:
                affinity = 1

            # 弾種&属性補正
            card_type_bonus = max(
                (
                    value
                    for element, value in s["card_type_buffs"]
                    if element == b["type"]
                ),
                default=0,
            )

            card_element_bonus = max(
                (
                    value
                    for element, value in s["card_element_buffs"]
                    if element == b["element"]
                ),
                default=0,
            )

            attacker_type_bonus = max(
                (
                    value
                    for element, value in a["type_buffs"]
                    if element == b["type"]
                ),
                default=0,
            )

            attacker_element_bonus = max(
                (
                    value
                    for element, value in a["element_buffs"]
                    if element == b["element"]
                ),
                default=0,
            )
            
            typebonus = (
                card_type_bonus 
                + attacker_type_bonus
            ) / 100

            elementbonus = (
                card_element_bonus 
                + attacker_element_bonus
            ) / 100

            # 弾種&属性カット
            typecut = max(
                (
                    value
                    for element, value in e["type_cuts"]
                    if element == b["type"]
                ),
                default=0,
            )

            elementcut = max(
                (
                    value
                    for element, value in e["element_cuts"]
                    if element == b["element"]
                ),
                default=0,
            )
            
            dmgcut = max(typecut, elementcut) / 100


            results[(ei, bi)] = {
                "enemy_index": ei,
                "bullet_index": bi,
                "s_lv": s["lv"],
                "power": b_power,
                "slice": b["slice"],
                "hard": b["hard"],
                "numbers": b["numbers"],
                "yangyin": b["yangyin"],
                "mirror": b["mirror"],
                "e_lv": e["lv"],
                "yangdef": e_yangdef,
                "yindef": e_yindef,
                "criatk": criatk,
                "focus": focus,
                "solo": solo,
                "criacc": criacc,
                "affinity": affinity,
                "typebonus": typebonus,
                "elementbonus": elementbonus,
                "dmgcut": dmgcut
            }

    return results