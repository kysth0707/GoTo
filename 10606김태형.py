import os
import time
import clipboard
import webbrowser
from module import jsonManager
from module import window
from module import drawManager
from module import keyManager
from module import mapManager
from module import searchManager


def getInput(txt : str) -> str:
	# 기본 함수 input() 대신 getInput() 을 쓴 이유
	# 이상하게도 input() 을 쓰면 공백이 입력되어 버그가 생김
	# 따라서 공백이 아닐 때 까지 입력받게 함수를 작성함.
	print(txt, end = '')
	while True:
		a = input().strip()
		if a != "":
			return a

def saveDatas():
	jsonManager.saveJson("./data/datas.json", datas)

def addDatas(title : str, tags : list, content : str):
	global datas
	datas["count"] += 1
	datas["data"].append(
		{
			"t" : title,
			"a" : tags,
			"c" : content,
			"e" : time.strftime('%Y-%m-%d_%H:%M:%S')
		}
	)
	for tag in tags:
		if datas["tag"].get(tag) == None:
			datas["tag"][tag] = 0

settings = jsonManager.loadJson("settings.json")
langData = jsonManager.loadJson(f"./lang/{settings['lang']}.json")
langList = list(map(lambda x : x.split('.')[0], os.listdir('./lang')))
langNum = langList.index(settings['lang'])

datas = {}
try:
	datas = jsonManager.loadJson("./data/datas.json")
except:
	datas = {"count" : 0, "data" : [], "tag" : {}}

# datas 구조
# {
# 	"count" : 개수,
# 	"data" : [
# 		{
# 			"t" : 제목,
# 			"a" : 태그,
# 			"c" : 내용,
# 			"e" : 시간
# 		}
# 	],
# 	"tag" : {
# 		태그
# 	}
# }


lastKey = None

pageData = mapManager.changeTo(mapManager.MAIN_PAGE)

while True:
	keyManager.update()
	currentKey = keyManager.getKeys().copy()


	if lastKey != currentKey:
		# 맵 새로고침

		# 화살표 이동
		if currentKey["left arrow"]:
			pageData["currentPos"] -= 1
		elif currentKey["right arrow"]:
			pageData["currentPos"] += 1
		elif currentKey["up arrow"]:
			pageData["currentPos"] -= 1
		elif currentKey["down arrow"]:
			pageData["currentPos"] += 1
		
		
		if mapManager.CURRNET_MAP == mapManager.MAIN_PAGE:
			# ================================== 메인 페이지
			pageData["currentPos"] %= 4 # 최대 4칸 움직임


			# 현재 선택 중인 아이템 그리기
			data = langData.copy()

			for i, x in enumerate(['main.create', 'main.search', 'main.list', 'main.changeLang']):
				c = "◆" if pageData["currentPos"] == i else "◇"
				data[x] = f"{c} {langData[x]} {c}"

			data['langHere'] = settings['lang']

			drawManager.draw(window.MAP["main"], data)
		

			# 선택
			if currentKey['enter']:
				# 확인 키
				if pageData["currentPos"] == 0:
					pageData = mapManager.changeTo(mapManager.CREATE_PAGE)
					# 생성
				elif pageData["currentPos"] == 1:
					pageData = mapManager.changeTo(mapManager.SEARCH_PAGE)
					# 검색
				elif pageData["currentPos"] == 2:
					pageData = mapManager.changeTo(mapManager.LIST_PAGE)
					# 목록
				elif pageData["currentPos"] == 3:
					# 언어 변경
					langNum += 1
					langNum %= len(langList)
					settings['lang'] = langList[langNum]
					langData = jsonManager.loadJson(f"./lang/{settings['lang']}.json")
					jsonManager.saveJson("settings.json", {'lang' : settings['lang']})

			if currentKey['esc']:
				break
		
		elif mapManager.CURRNET_MAP == mapManager.CREATE_PAGE:
			# ================================== 생성 페이지
			pageData["currentPos"] %= 4

			# 현재 선택 중인 아이템 그리기
			data = langData.copy()

			for i, x in enumerate(['create.title', 'create.tag', 'create.content', 'create.create']):
				c = "◆" if pageData["currentPos"] == i else "◇"
				data[x] = f"{c} {langData[x]} {c}"


			# 입력된 값 그리기
			data['titleHere'] = pageData['title']
			data['tagHere'] = " ".join(pageData['tag'])
			data['contentHere'] = pageData['content']

			drawManager.draw(window.MAP["create"], data)

			# 내용 설정하기
			if currentKey['enter']:
				if pageData['currentPos'] == 0:
					# 제목 입력
					pageData['title'] = getInput(f"{data['create.title.input']} : ")

				elif pageData['currentPos'] == 1:
					# 태그 입력
					a = getInput(f"{data['create.tag.input']} : ")
					a = f"[{a}]"
					
					if a not in pageData['tag']:
						pageData['tag'].append(a)
						

				elif pageData['currentPos'] == 2:
					# 내용 입력
					pageData['content'] = getInput(f"{data['create.content.input']} : ")


				elif pageData['currentPos'] == 3:
					addDatas(pageData['title'], pageData['tag'], pageData['content'])
					saveDatas()
					pageData = mapManager.changeTo(mapManager.MAIN_PAGE)

			if currentKey['esc']:
				pageData = mapManager.changeTo(mapManager.MAIN_PAGE)

		elif mapManager.CURRNET_MAP == mapManager.LIST_PAGE:
			# ================================== 목록 페이지
			pageData["currentPos"] %= 11

			data = langData.copy()

			c = "◆" if pageData["currentPos"] == 0 else "◇"
			data['list.previous'] = f"{c} {langData['list.previous']} {c}"
			c = "◆" if pageData["currentPos"] == 10 else "◇"
			data['list.next'] = f"{c} {langData['list.next']} {c}"
			
			for i in range(9):
				c = "◆" if pageData["currentPos"] == (i + 1) else "◇"
				try:
					target = datas["data"][i + pageData['listPos']]
					data[f"list.item{i}"] = f"{c} {i + pageData['listPos']}. {target['t']} | {' '.join(target['a'])} | {target['c']}"
				except:
					data[f"list.item{i}"] = f"{c} {i + pageData['listPos']}."

			if currentKey['enter']:
				if pageData['currentPos'] == 0:
					if pageData['listPos'] >= 9:
						pageData['listPos'] -= 9
				elif pageData['currentPos'] == 10:
					pageData['listPos'] += 9
				else:
					try:
						target = datas["data"][pageData['currentPos'] - 1 + pageData['listPos']]
						pageData = mapManager.changeTo(mapManager.SHOW_PAGE)
						pageData['data'] = target
					except:
						pass

			data['list.countHere'] = str(datas['count'])
				
			drawManager.draw(window.MAP["list"], data)

			if currentKey['esc']:
				pageData = mapManager.changeTo(mapManager.MAIN_PAGE)

		elif mapManager.CURRNET_MAP == mapManager.SHOW_PAGE:
			# ================================== 보여주기 페이지
			pageData["currentPos"] %= 4

			data = langData.copy()

			for i, x in enumerate(['create.title', 'create.tag', 'create.content', 'create.time']):
				c = "◆" if pageData["currentPos"] == i else "◇"
				data[x] = f"{c} {langData[x]} {c}"

			data['titleHere'] = pageData['data']['t']
			data['tagHere'] = " ".join(pageData['data']['a'])
			data['contentHere'] = pageData['data']['c']
			data['timeHere'] = pageData['data']['e']
		
			
			if currentKey['enter']:
				clipboard.copy([
					data['titleHere'],
					data['tagHere'],
					data['contentHere'],
					data['timeHere']
				][pageData['currentPos']])


			drawManager.draw(window.MAP["show"], data)

			if currentKey['esc']:
				pageData = mapManager.changeTo(mapManager.MAIN_PAGE)

		elif mapManager.CURRNET_MAP == mapManager.SEARCH_PAGE:
			# ================================== 검색 페이지
			pageData["currentPos"] %= 12

			data = langData.copy()

			for i, x in enumerate(['search.sort.time', 'search.sort.title', 'search.sort.tag', 'search.sort.content', 'search.text', 'list.previous']):
				c = "◆" if pageData["currentPos"] == i else "◇"
				data[x] = f"{c} {langData[x]} "
			
			c = "◆" if pageData["currentPos"] == 11 else "◇"
			data['list.next'] = f"{c} {langData['list.next']} {c}"
			
			for i in range(5):
				c = "◆" if pageData["currentPos"] == (i + 6) else "◇"
				try:
					target = pageData['searchedData'][i + pageData['listPos']]
					data[f"list.item{i}"] = f"{c} {i + pageData['listPos']}. {target['t']} | {' '.join(target['a'])} | {target['c']}"
				except:
					data[f"list.item{i}"] = f"{c} {i + pageData['listPos']}."
		
			
			if currentKey['enter']:
				if pageData['currentPos'] <= 3:
					a = [searchManager.SORT_TIME, 
		  				 searchManager.SORT_TITLE, 
						 searchManager.SORT_CONTENT, 
						 searchManager.SORT_CONTENT]
					pageData['searchedData'] = searchManager.search(datas['data'], a[pageData['currentPos']])
				elif pageData['currentPos'] == 4:
					pageData['searchText'] = getInput(f"{data['search.text']}")
					pageData['searchedData'] = searchManager.search(datas['data'], searchManager.SORT_TITLE, pageData['searchText'])
					pageData['listPos'] = 0

				elif pageData['currentPos'] == 5:
					if pageData['listPos'] >= 5:
						pageData['listPos'] -= 5
				elif pageData['currentPos'] == 11:
					pageData['listPos'] += 5
				else:
					try:
						target = pageData['searchedData'][pageData['currentPos'] - 6 + pageData['listPos']]
						pageData = mapManager.changeTo(mapManager.SHOW_PAGE)
						pageData['data'] = target
						continue
					except:
						pass

			data['searchHere'] = str(pageData['searchText'])
			data['search.countHere'] = str(len(pageData['searchedData']))

			drawManager.draw(window.MAP["search"], data)

			if currentKey['esc']:
				pageData = mapManager.changeTo(mapManager.MAIN_PAGE)


			
		

	lastKey = keyManager.getKeys().copy()




'''
2023학년도 2학기 정보 수행평가
학번:10606
성명:김태형
진로 희망:프로그래머

날짜 및 코딩 작업 요약
10.23: 코딩 구상 및 000 000 작성

2023.10.25 : 기본적인 구조 완성 / drawManager, jsonMAnager, keyManager, mapManager, window, 메인 페이지 생성
2023.10.27 : 생성 페이지 제작
2023.10.28 : input() 버그 확인
2023.10.29 : input() 버그 해결 및 태그 데이터 저장, 목록 기능 추가, 검색 기능 구현 중
2023.10.30 : 검색 기능 완료 및 lang/en.json 추가


'''


