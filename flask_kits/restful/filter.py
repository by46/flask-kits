def filter_params():
    return [
        {
            "name": "page",
            "description": "page index used to pagination",
            "required": False,
            "dataType": "int",
            "paramType": "query"
        }, {
            "name": "per_page",
            "description": "page size per page",
            "required": False,
            "dataType": "int",
            "paramType": "query"
        }
    ]
