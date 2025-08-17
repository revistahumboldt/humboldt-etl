config_analysis = {
    "resultType": "DATA_ONLY",
    "queryObject": {
        "columns": [
            {
                "name": "page_category_text_15",
                "scope": "OBJECT",
                "context": "PAGE",
                "lowerLimit": 1,
                "upperLimit": 30000
            },
            {
                "name": "page_url",
                "scope": "OBJECT",
                "context": "PAGE",
                "lowerLimit": 1,
                "upperLimit": 30000
            },
            {
                "name": "time_days",
                "sortDirection": "ASCENDING",
                "sortIndex": 1,
                "scope": "OBJECT",
                "context": "NONE"
            },
            {
                "name": "location_country",
                "scope": "OBJECT",
                "context": "SESSION"
            },
            {
                "name": "device_deviceClass",
                "scope": "OBJECT",
                "context": "SESSION"
            },
            {
                "name": "pages_pageImpressions",
                "columnPeriod": "ANALYSIS",
                "scope": "OBJECT",
                "context": "PAGE",
                "variant": "NORMAL"
            },
            {
                "name": "pages_entries",
                "columnPeriod": "ANALYSIS",
                "scope": "OBJECT",
                "context": "PAGE"
            },
            {
                "name": "visits_bounces",
                "columnPeriod": "ANALYSIS",
                "scope": "OBJECT",
                "context": "PAGE"
            },
            {
                "name": "visitors",
                "columnPeriod": "ANALYSIS",
                "scope": "OBJECT",
                "context": "SESSION"
            },
            {
                "name": "pages_durationAvg",
                "columnPeriod": "ANALYSIS",
                "scope": "OBJECT"
            },

        ],
        "predefinedContainer": {
            "filters": [
                {
                    "name": "time_range",
                    "value1": "2025-02-01 00:00:00",
                    "value2": "2025-02-28 00:00:00",
                    "filterPredicate": "BETWEEN",
                    "connector": "AND",
                    "context": "NONE",
                    "caseSensitive": False
                },
                {
                    "name": "page_url",
                    "value1": "https://www.goethe.de/prj/hum/*",
                    "connector": "AND",
                    "filterPredicate": "LIKE",
                    "value2": "",
                    "context": "NONE",
                    "caseSensitive": False,
                    "title": "Seiten-URL"
                }
            ],
            "containers": [
                {
                    "filters": [
                        {
                            "name": "page_category_text_4",
                            "connector": "AND",
                            "filterPredicate": "NOT_LIKE",
                            "value1": "fem",
                            "value2": "",
                            "context": "PAGE",
                            "caseSensitive": False
                        },
                        {
                            "name": "page_category_text_4",
                            "connector": "OR",
                            "filterPredicate": "NOT_LIKE",
                            "value1": "nac",
                            "value2": "",
                            "context": "PAGE",
                            "caseSensitive": False
                        },
                        {
                            "name": "page_category_text_4",
                            "connector": "OR",
                            "filterPredicate": "NOT_LIKE",
                            "value1": "pdk",
                            "value2": "",
                            "context": "PAGE",
                            "caseSensitive": False
                        },
                        {
                            "name": "page_category_text_4",
                            "connector": "OR",
                            "filterPredicate": "NOT_LIKE",
                            "value1": "pos",
                            "value2": "",
                            "context": "PAGE",
                            "caseSensitive": False
                        },
                        {
                            "name": "page_category_text_4",
                            "connector": "OR",
                            "filterPredicate": "NOT_LIKE",
                            "value1": "zgt",
                            "value2": "",
                            "context": "PAGE",
                            "caseSensitive": False
                        }
                    ],
                    "containers": [],
                    "connector": "AND",
                    "context": "PAGE",
                    "inOrNotIn": "IN",
                    "type": "NORMAL"
                }
            ]
        },
        "variant": "PIVOT_AS_LIST",
        "elementPeriod": "ELEMENT"
    }
}
