from general import *
import numpy as np
# from query import *
pos= file_to_dict("Indexer/position_dict.pkl")
#
# positions = Query.positionDict.get(url).values()
#         docuWords = list(positions)
#         fWords = []
#         for i in docuWords:
#             fWords.append(tuple(i)[1])
#         arrayOFtf = np.array(fWords)
#
#         arrayOFtf = 1 + np.log(arrayOFtf)
print(pos)