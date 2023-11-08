import copy

MAIN_PAGE = 0
CREATE_PAGE = 1
LIST_PAGE = 2
SEARCH_PAGE = 3
SHOW_PAGE = 4

CURRNET_MAP = MAIN_PAGE

BASIC_PAGE_DATA = {
    MAIN_PAGE : {
        "currentPos" : 0,
    },
    CREATE_PAGE : {
        "currentPos" : 0,
        "title" : "",
        "tag" : [],
        "content" : "",
    },
    LIST_PAGE : {
        "currentPos" : 0,
        "listPos" : 0,
	},
    SHOW_PAGE : {
        "currentPos" : 0,
        "data" : {}
	},
    SEARCH_PAGE : {
        "currentPos" : 0,
        "searchType" : 0,
        "searchText" : "",
        "searchedData" : [],
        "listPos" : 0,
	}
}

def changeTo(targetPage : int) -> dict:
    """
    changeTo(타겟 맵)
    -> 기본 dict 변수 리턴
    """
    global CURRNET_MAP
    CURRNET_MAP = targetPage

    return copy.deepcopy(BASIC_PAGE_DATA[CURRNET_MAP])