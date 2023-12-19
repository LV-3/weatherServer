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
    weather_data = SKY_VALUE +', '+ PTY_VALUE

    rec_ctnt_id_list_1d_stacked = Counter(rec_ctnt_id_list_1d)
    sorted_rec_ctnt_id_list_1d_stacked = [ key for key,_ in rec_ctnt_id_list_1d_stacked.most_common()]

    if PTY_VALUE == "없음":
        get_img_url = get_weather_img(SKY_VALUE)
    else:
        get_img_url = get_weather_img(PTY_VALUE)




    item_dic = {"weather": weather_data, 
                "content_id": sorted_rec_ctnt_id_list_1d_stacked,
                "ImgUrl": get_img_url}
    
    db_get(item_dic)

    return ctnt_id_list

    # isA = upload_dict_to_s3(bucket=bucket_name, file_name=file_name, file=payload_data)


@app.post("/db_get")
def db( ):
    ctnt_id = 'uq_1710, uq_970, uq_1136, uq_1501, uq_1830, uq_330, uq_1556, uq_1156, uq_1688, uq_1716, uq_1565, uq_1836, uq_1631, uq_1173, uq_550, uq_1654, uq_914, uq_432, uq_1675, uq_2014, uq_702, uq_1315, uq_1402, uq_1560, uq_419, uq_718, uq_772, uq_315, uq_542, uq_1308, uq_844, uq_1497, uq_890, uq_1413, uq_1160, uq_1549, uq_1687, uq_879, uq_1224, uq_1263, uq_952, uq_1309, uq_1257, uq_893, uq_1659, uq_703, uq_801, uq_1006, uq_1034, uq_1741, uq_1986, uq_1815, uq_1855, uq_178, uq_1796, uq_1797, uq_1592, uq_1671, uq_1744, uq_1507, uq_723, uq_1465, uq_2, uq_2026, uq_1835, uq_1037, uq_4, uq_896, uq_1496, uq_321, uq_1966, uq_791, uq_1363, uq_1814, uq_1931, uq_117, uq_386, uq_161, uq_277, uq_158, uq_671, uq_660, uq_197, uq_626, uq_524, uq_193, uq_309, uq_1798, uq_1607, uq_1181, uq_1180, uq_108, uq_518, uq_1214, uq_1409, uq_1067, uq_1792, uq_2017, uq_306, uq_438'
    ctnt_id_list = ctnt_id.split(', ')

    item_dic = {"weather": "맑음", 
                "content_id": ctnt_id_list,
                "ImgUrl": "https://ifh.cc/g/jtjy3V.png"}
    db_get(item_dic)
