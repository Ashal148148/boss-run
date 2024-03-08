from typing import List


THIEF_ARCHER_BASE_HP = [50,64,78,92,106,120,134,148,162,338,360,382,404,426,448,470,492,514,536,558,580,602,624,646,668,690,712,734,756,1103,1125,1147,1169,1191,1213,1235,1257,1279,1301,1323,1345,1367,1389,1411,1433,1455,1477,1499,1521,1543,1565,1587,1609,1631,1653,1675,1697,1719,1741,1763,1785,1807,1829,1851,1873,1895,1917,1939,1961,1983,2005,2027,2049,2071,2093,2115,2137,2159,2181,2203,2225,2247,2269,2291,2313,2335,2357,2379,2401,2423,2445,2467,2489,2511,2533,2555,2577,2599,2621,2643,2665,2687,2709,2731,2753,2775,2797,2819,2841,2863,2885,2907,2929,2951,2973,2995,3017,3039,3061,3083,3105,3127,3149,3171,3193,3215,3237,3259,3281,3303,3325,3347,3369,3391,3413,3435,3457,3479,3501,3523,3545,3567,3589,3611,3633,3655,3677,3699,3721,3743,3765,3787,3809,3831,3853,3875,3897,3919,3941,3963,3985,4007,4029,4051,4073,4095,4117,4139,4161,4183,4205,4227,4249,4271,4293,4315,4337,4359,4381,4403,4425,4447,4469,4491,4513,4535,4557,4579,4601,4623,4645,4667,4689,4711,4733,4755,4777,4799,4821,4843]
HERO_PAGE_BASE_HP = [50,64,78,92,106,120,134,148,162,401,431,473,527,593,659,725,791,857,923,989,1055,1121,1187,1253,1319,1385,1451,1517,1583,1974,2040,2106,2172,2238,2304,2370,2436,2502,2568,2634,2700,2766,2832,2898,2964,3030,3096,3162,3228,3294,3360,3426,3492,3558,3624,3690,3756,3822,3888,3954,4020,4086,4152,4218,4284,4350,4416,4482,4548,4614,4680,4746,4812,4878,4944,5010,5076,5142,5208,5274,5340,5406,5472,5538,5604,5670,5736,5802,5868,5934,6000,6066,6132,6198,6264,6330,6396,6462,6528,6594,6660,6726,6792,6858,6924,6990,7056,7122,7188,7254,7320,7386,7452,7518,7584,7650,7716,7782,7848,7914,7980,8046,8112,8178,8244,8310,8376,8442,8508,8574,8640,8706,8772,8838,8904,8970,9036,9102,9168,9234,9300,9366,9432,9498,9564,9630,9696,9762,9828,9894,9960,10026,10092,10158,10224,10290,10356,10422,10488,10554,10620,10686,10752,10818,10884,10950,11016,11082,11148,11214,11280,11346,11412,11478,11544,11610,11676,11742,11808,11874,11940,12006,12072,12138,12204,12270,12336,12402,12468,12534,12600,12666,12732,12798,12864,12930,12996,13062,13128,13194]
DK_BASE_HP = [50,64,78,92,106,120,134,148,162,401,431,473,527,593,659,725,791,857,923,989,1055,1121,1187,1253,1319,1385,1451,1517,1583,1649,1715,1781,1847,1913,1979,2045,2111,2177,2243,2309,2375,2441,2507,2573,2639,2705,2771,2837,2903,2969,3035,3101,3167,3233,3299,3365,3431,3497,3563,3629,3695,3761,3827,3893,3959,4025,4091,4157,4223,4289,4355,4421,4487,4553,4619,4685,4751,4817,4883,4949,5015,5081,5147,5213,5279,5345,5411,5477,5543,5609,5675,5741,5807,5873,5939,6005,6071,6137,6203,6269,6335,6401,6467,6533,6599,6665,6731,6797,6863,6929,6995,7061,7127,7193,7259,7325,7391,7457,7523,7589,7655,7721,7787,7853,7919,7985,8051,8117,8183,8249,8315,8381,8447,8513,8579,8645,8711,8777,8843,8909,8975,9041,9107,9173,9239,9305,9371,9437,9503,9569,9635,9701,9767,9833,9899,9965,10031,10097,10163,10229,10295,10361,10427,10493,10559,10625,10691,10757,10823,10889,10955,11021,11087,11153,11219,11285,11351,11417,11483,11549,11615,11681,11747,11813,11879,11945,12011,12077,12143,12209,12275,12341,12407,12473,12539,12605,12671,12737,12803,12869]
SAIR_BASE_HP = [50,64,78,92,106,120,134,148,162,338,363,388,413,438,463,488,513,538,563,588,613,638,663,688,713,738,763,788,813,1063,1088,1113,1138,1163,1188,1213,1238,1263,1288,1313,1338,1363,1388,1413,1438,1463,1488,1513,1538,1563,1588,1613,1638,1663,1688,1713,1738,1763,1788,1813,1838,1863,1888,1913,1938,1963,1988,2013,2038,2063,2088,2113,2138,2163,2188,2213,2238,2263,2288,2313,2338,2363,2388,2413,2438,2463,2488,2513,2538,2563,2588,2613,2638,2663,2688,2713,2738,2763,2788,2813,2838,2863,2888,2913,2938,2963,2988,3013,3038,3063,3088,3113,3138,3163,3188,3213,3238,3263,3288,3313,3338,3363,3388,3413,3438,3463,3488,3513,3538,3563,3588,3613,3638,3663,3688,3713,3738,3763,3788,3813,3838,3863,3888,3913,3938,3963,3988,4013,4038,4063,4088,4113,4138,4163,4188,4213,4238,4263,4288,4313,4338,4363,4388,4413,4438,4463,4488,4513,4538,4563,4588,4613,4638,4663,4688,4713,4738,4763,4788,4813,4838,4863,4888,4913,4938,4963,4988,5013,5038,5063,5088,5113,5138,5163,5188,5213,5238,5263,5288,5313]
BUCC_BASE_HP = [50,64,78,92,106,120,134,148,162,338,363,388,413,438,463,488,513,538,563,588,613,638,663,688,713,738,763,788,813,1063,1091,1128,1174,1229,1284,1339,1394,1449,1504,1559,1614,1669,1724,1779,1834,1889,1944,1999,2054,2109,2164,2219,2274,2329,2384,2439,2494,2549,2604,2659,2714,2769,2824,2879,2934,2989,3044,3099,3154,3209,3264,3319,3374,3429,3484,3539,3594,3649,3704,3759,3814,3869,3924,3979,4034,4089,4144,4199,4254,4309,4364,4419,4474,4529,4584,4639,4694,4749,4804,4859,4914,4969,5024,5079,5134,5189,5244,5299,5354,5409,5464,5519,5574,5629,5684,5739,5794,5849,5904,5959,6014,6069,6124,6179,6234,6289,6344,6399,6454,6509,6564,6619,6674,6729,6784,6839,6894,6949,7004,7059,7114,7169,7224,7279,7334,7389,7444,7499,7554,7609,7664,7719,7774,7829,7884,7939,7994,8049,8104,8159,8214,8269,8324,8379,8434,8489,8544,8599,8654,8709,8764,8819,8874,8929,8984,9039,9094,9149,9204,9259,9314,9369,9424,9479,9534,9589,9644,9699,9754,9809,9864,9919,9974,10029,10084,10139,10194,10249,10304,10359]

class Job:
    name: str
    mp_cost: int
    base_hp_gain: int
    base_hp: List[int]
    hp_gain_skill: int
    hp_gain_skill_level: int
    first_job_stat_requirement: int

    def __init__(self, name: str, mp_cost: int, hp_gain: int, base_hp: List[int], first_job_stat_requirement: int, hp_gain_skill: int = 0, hp_gain_skill_level: int = 200) -> None:
        self.name = name
        self.mp_cost = mp_cost
        self.base_hp_gain = hp_gain
        self.base_hp = base_hp
        self.first_job_stat_requirement = first_job_stat_requirement
        self.hp_gain_skill = hp_gain_skill
        self.hp_gain_skill_level = hp_gain_skill_level
        
    def __str__(self):
        return f"<Job(name={self.name}, mp_cost={self.mp_cost}, base_hp_gain={self.base_hp_gain}, hp_gain_skill={self.hp_gain_skill}, hp_gain_skill_level={self.hp_gain_skill_level})>"


archer_thief = Job(
    name="Archer/Thief",
    mp_cost=12,
    hp_gain=16,
    base_hp=THIEF_ARCHER_BASE_HP,
    first_job_stat_requirement=25
)
dk = Job(
    name="Spearman",
    mp_cost=4,
    hp_gain=20,
    base_hp=DK_BASE_HP,
    first_job_stat_requirement=35,
    hp_gain_skill=30,
    hp_gain_skill_level=14
)
hero_pala = Job(
    name="Hero/Paladin",
    mp_cost=4,
    hp_gain=20,
    base_hp=HERO_PAGE_BASE_HP,
    first_job_stat_requirement=35,
    hp_gain_skill=30,
    hp_gain_skill_level=14
)
bucc = Job(
    name="Brawler",
    mp_cost=16,
    hp_gain=18,
    base_hp=BUCC_BASE_HP,
    first_job_stat_requirement=20,
    hp_gain_skill=20,
    hp_gain_skill_level=34
)
sair = Job(
    name="Gunslinger",
    mp_cost=16,
    hp_gain=18,
    base_hp=SAIR_BASE_HP,
    first_job_stat_requirement=20
)

jobs = {"Thief": thief , "Archer": archer, "Brawler": bucc, "Gunslinger": sair, "Hero/Paladin": hero_pala, "Spearman":dk}