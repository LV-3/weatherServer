from fastapi import FastAPI, Request
from langchainClass import ExtractWord
from embeddding import Embedding
from emb_to_ctntid import WeatherIndex
from db_connection import db_get
from collections import Counter
from resources.weather_img import get_weather_img

# 현재 시간을 얻기
app = FastAPI()

@app.get("/")
def dummy():
    return {"h": "i"}


@app.post("/endpoint")
async def process_payload(request: Request):
    try:
        payload_data = await request.json()
        print("Data inside FastAPI endpoint:", payload_data)

    except Exception as e:
        return {"error": str(e)}
    ctnt_id_list = []
    extract = ExtractWord()

    template_list = extract.run(payload_data["last_sky_value"], payload_data["last_pty_value"])


    print('template_list :', template_list)
    embed = Embedding()
    word_embedding_data = embed.word_embedding(template_list)
    for i in range(len(word_embedding_data)):
        print(word_embedding_data[i].keys())


    weather_idx = WeatherIndex()
    for idx in range(len(template_list)):
        embedding_vector = (word_embedding_data[idx].get(template_list[idx]))
        
        rec_ctnt_id_list = weather_idx.search(embedding_vector)
        # rec_ctnt_id_list: list
        print("rec_ctnt_id_list", rec_ctnt_id_list)
        
        ctnt_id_list.append(rec_ctnt_id_list)

    rec_ctnt_id_list_1d = [elm for sublist in ctnt_id_list for elm in sublist]
    

    SKY_VALUE = payload_data["last_sky_value"]
    PTY_VALUE = payload_data["last_pty_value"]


    rec_ctnt_id_list_1d_stacked = Counter(rec_ctnt_id_list_1d)
    sorted_rec_ctnt_id_list_1d_stacked = [ key for key,_ in rec_ctnt_id_list_1d_stacked.most_common()]


    if PTY_VALUE == "없음":
        get_img_url = get_weather_img(SKY_VALUE)
        weather_data = SKY_VALUE

    else:
        get_img_url = get_weather_img(PTY_VALUE)
        weather_data = PTY_VALUE    

    if weather_data == '빗방울눈날림':
        weather_data = '빗방울/눈날림'


    item_dic = {"weather": weather_data, 
                "content_id": sorted_rec_ctnt_id_list_1d_stacked,
                "ImgUrl": get_img_url}
    
    db_get(item_dic)

    return ctnt_id_list

    # isA = upload_dict_to_s3(bucket=bucket_name, file_name=file_name, file=payload_data)