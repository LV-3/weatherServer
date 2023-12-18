import openai
from dotenv import load_dotenv
import os

class Embedding:
    def __init__(self) -> None:
        load_dotenv()
        openai.api_key = os.getenv("OPEN_API_KEY")


    def encoding(self, word: str) -> list[float]:    
        response = openai.embeddings.create(
            model = 'text-embedding-ada-002',
            input  = word,
        )
            
        return response.data[0].embedding


    def word_embedding(self, template_list: list):
        weather_dic = []

        for word in template_list:
            emb_results = self.encoding(word)

            new_key = word
            new_value = emb_results

            new_entry = {new_key: new_value}

            weather_dic.append(new_entry)
        
        return weather_dic  