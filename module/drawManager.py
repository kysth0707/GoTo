import os
import time

def draw(mapData : list, data : dict):
	line = "\n".join(mapData)
	for key, value in data.items():
		line = line.replace(f"[{key}]", value)

	os.system('cls')
	print(line)