import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def arr_convert(arr):
	res = []
	for i in range(len(arr[0])):
		tmp = []
		for j in range(len(arr)):
			tmp.append(arr[j][i])
		res.append(tmp)
	return res	



def show_graph(arr, date):
	res_percent = arr_convert(arr)

	index = np.arange(5)
	data = {}
	for percent in range(len(res_percent)):
		data[f'смена {percent + 1}'] = res_percent[percent]

	print(data)

	df = pd.DataFrame(data)
	df.plot(kind='bar')
	plt.xticks(np.arange(len(res_percent[0])), date)
	plt.yticks(np.arange(0, 100))
	plt.show()
	plt.savefig('foo.png', bbox_inches='tight') # - сохранение в .png для вывода
	
