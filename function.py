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


    return buff1factor * buff2factor

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