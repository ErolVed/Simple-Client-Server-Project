FROM python:3

ENV root_path=./PecanProject/pecanproject/


WORKDIR /Downloads/PecanProject

COPY PecanProject/pecanproject/requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python ./PecanProject/pecanproject/server.py

