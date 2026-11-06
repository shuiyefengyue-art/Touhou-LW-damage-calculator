NAME = "C3<磨弓:私が袿姫様の作った衣装を一番可愛く着れるんです"

DATA = {
    "soloall": "全体",
    "lv": 28,

    "bullets": [
        # 1段目
        {
            "power": 3.68,
            "rawcriacc": 10,
            "slice": 220,
            "hard": 0,
            "numbers": 32,
            "type": "尖弾",
            "element": "土",
            "yangyin": "陽気",
            "criaccupper": ["弾性弾"],
            "mirror": "いいえ",
            "penetrate": "いいえ",
        },
        # 2段目
        {
            "power": 6.44,
            "rawcriacc": 13,
            "slice": 0,
            "hard": 0,
            "numbers": 5,
            "type": "尖弾",
            "element": "土",
            "yangyin": "陽気",
            "criaccupper": ["弾性弾"],
            "mirror": "いいえ",
            "penetrate": "いいえ",
        },
        # 3段目
        {
            "power": 7.38,
            "rawcriacc": 13,
            "slice": 160,
            "hard": 0,
            "numbers": 4,
            "type": "尖弾",
            "element": "土",
            "yangyin": "陽気",
            "criaccupper": [],
            "mirror": "いいえ",
            "penetrate": "いいえ",
        },
        # 4段目
        {
            "power": 9.28,
            "rawcriacc": 15,
            "slice": 0,
            "hard": 0,
            "numbers": 3,
            "type": "尖弾",
            "element": "土",
            "yangyin": "陽気",
            "criaccupper": ["弾性弾"],
            "mirror": "いいえ",
            "penetrate": "いいえ",
        },
        # 5段目
        {
            "power": 25.04,
            "rawcriacc": 15,
            "slice": 160,
            "hard": 0,
            "numbers": 1,
            "type": "尖弾",
            "element": "土",
            "yangyin": "陽気",
            "criaccupper": ["弾性弾"],
            "mirror": "いいえ",
            "penetrate": "いいえ",
        },
        # 6段目
        {
            "power": 22.59,
            "rawcriacc": 20,
            "slice": 240,
            "hard": 0,
            "numbers": 1,
            "type": "尖弾",
            "element": "土",
            "yangyin": "陽気",
            "criaccupper": [],
            "mirror": "いいえ",
            "penetrate": "いいえ",
        },
    ],

    "card_type_buffs": [("尖弾", 50)],
    "card_element_buffs": [("土", 50), ("星", 50)]
}


for bi, bullet in enumerate(DATA["bullets"]):
    bullet["rawacc"] = [100, 95, 95, 90, 90, 85][bi]


lawcp = (
    sum(
        bullet["power"]
        * bullet["rawacc"] / 100
        * (
            1
            + bullet["rawcriacc"] / 100
        )
        * bullet["numbers"]
        * (
            1
            + DATA["lv"] / 100
        )
        for bullet in DATA["bullets"]
    )
)

print(lawcp)