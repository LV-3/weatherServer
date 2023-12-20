WEATHER_IMG = {
    "구름많음": "https://ifh.cc/g/r9GmtD.png",
    "흐림": "https://ifh.cc/g/QyPxgn.png",
    "맑음": "https://ifh.cc/g/jtjy3V.png",
    "없음": "https://ifh.cc/g/jtjy3V.png",
    "빗방울": "https://ifh.cc/g/RNxHC0.png",
    "빗방울눈날림": "https://ifh.cc/g/RNxHC0.png",
    "비": "https://ifh.cc/g/mSRLRh.png",
    "눈": "https://ifh.cc/g/c2dLdV.png",
    "눈날림": "https://ifh.cc/g/c2dLdV.png",
    "비/눈": "https://ifh.cc/g/c2dLdV.png"
}
def get_weather_img(weather_type):
    return WEATHER_IMG.get(weather_type)