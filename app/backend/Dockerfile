FROM python:3.9

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

COPY ./app ./

CMD ["python", "server.py"]