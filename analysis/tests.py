from django import db
from django.test import TestCase

jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjEzMDYwMjA0MDQ2In0.9CrXgcQ73sFafCmlDI_adWRSgf4qjGVZoiGBP4jBYN8"

"""
result = \
    {
        "month": 12,
        "order": {
            "w_sales": "0.00",
            "w_champ_sales": "0.00",
            "w_champ_id": null,
            "w_champ_name": null,
            "m_sales": "134,068,912.00",
            "m_rose": 37.24,
            "m_champ_sales": "18,352,879.00",
            "m_champ_id": "9dHN60nhnLrRG6wNaS",
            "m_champ_name": "Boss"
        },
        "finance": {
            "rose": "36,380,904.00",
            "list": [
                {
                    "m": 12,
                    "sales": "134,068,912.00"
                },
                {
                    "m": 11,
                    "sales": "97,688,008.00"
                },
                {
                    "m": 10,
                    "sales": "0.00"
                },
                {
                    "m": 9,
                    "sales": "0.00"
                }
            ]
        },
        "material": {
            "w": [],
            "m": [
                {
                    "name": "铁块",
                    "category_name": "建材",
                    "cost": "25.00"
                },
                {
                    "name": "玻璃",
                    "category_name": "建材",
                    "cost": "20.00"
                }
            ]
        },
        "store": {
            "w": [
                {
                    "count": -4,
                    "name": "碳纤维",
                    "unit": "g",
                    "category_name": "电池材料"
                },
                {
                    "count": -2,
                    "name": "石墨",
                    "unit": "根",
                    "category_name": "电池材料"
                },
                {
                    "count": -1,
                    "name": "电极片",
                    "unit": "片",
                    "category_name": ""
                }
            ],
            "m": [
                {
                    "count": -1111,
                    "name": "",
                    "unit": "",
                    "category_name": ""
                },
                {
                    "count": -110,
                    "name": "",
                    "unit": "",
                    "category_name": ""
                },
                {
                    "count": -10,
                    "name": "",
                    "unit": "",
                    "category_name": ""
                }
            ]
        },
        "product": {
            "w": [
                {
                    "count": -118,
                    "name": "999感冒灵",
                    "unit": "盒",
                    "category_name": "口服"
                }
            ],
            "m": [
                {
                    "count": -5000,
                    "name": "",
                    "unit": "",
                    "category_name": ""
                },
                {
                    "count": -10,
                    "name": "",
                    "unit": "",
                    "category_name": ""
                }
            ]
        }
    }"""
