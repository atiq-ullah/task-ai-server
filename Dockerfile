FROM python:3.12
EXPOSE 8000
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY entrypoint.sh entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
