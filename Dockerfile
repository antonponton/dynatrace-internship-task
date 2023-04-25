FROM python:3
WORKDIR /dynatrace
COPY . .
ENV PYTHONUNBUFFERED=1
CMD [ "python", "server.py" ]
EXPOSE 8000