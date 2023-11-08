SORT_TIME = 0
SORT_TITLE = 1
SORT_TAG = 2
SORT_CONTENT = 3

def search(allDatas : list, sortType : int = SORT_TITLE, searchText : str = "") -> list:
	if searchText != "":
		returnData = []
		for data in allDatas:
			if (
				searchText in data['t']
				or f"[{searchText}]" in data['a']
				or searchText in data['c']
				or searchText in data['e']
			):
				returnData.append(data)
		return returnData
	
	if sortType == SORT_TIME:
		return sorted(allDatas, key=lambda x : x['e'])
	elif sortType == SORT_TITLE:
		return sorted(allDatas, key=lambda x : x['t'])
	elif sortType == SORT_TAG:
		return sorted(allDatas, key=lambda x : x['a'])
	elif sortType == SORT_CONTENT:
		return sorted(allDatas, key=lambda x : x['c'])