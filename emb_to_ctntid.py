import numpy as np
import pandas as pd
import faiss
import pickle
import random


class WeatherIndex:
    def __init__(self):

        self.index = faiss.read_index('resources/weather_faiss_index_1219.index')

        # index 파일 갈아끼기
        with open('resources/FaissIndex2UniqueId_weather.pickle','rb') as pickle_file:
            self.FaissIndex2Content_id = pickle.load(pickle_file)


    def ContentId2FaissIndex(self, content_id: int) -> np.ndarray:
        faiss_index = self.FaissIndex2Content_id.get(content_id)
        emb = self.index.reconstruct(faiss_index)
        emb_np = np.array(emb).reshape(1, -1)
        return emb_np
    
    
    def search(self, vec_list: list) -> list[str]:
        k = 30
        # vec_list = ['우울 V', '로맨스 V', ,,]
        vec_list = np.array(vec_list)
        vec_list = vec_list.reshape(1,-1)

        D, I = self.index.search(vec_list, k)

        index_list = I.flatten().tolist()

        recommend_content_id = [str(self.FaissIndex2Content_id.get(key)) for key in self.FaissIndex2Content_id.keys() if key in index_list]

        return recommend_content_id