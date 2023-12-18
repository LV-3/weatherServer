FROM python:3.9-slim-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 두 줄은 배포할 때 주석 해제하고 실행
COPY . /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000"]
