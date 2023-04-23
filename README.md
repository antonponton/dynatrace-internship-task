# Backend oriented task

I choose to do this task in python

## Instructions to run the server an test operations:

-To start the server, run this command:
```
python -m server.py
```
-To query operation 1, run this command:
```
curl http://localhost:8000/exchangerates/rates/a/AUD/2022-05-13/
```
-To query operation 2, run this command:
```
curl http://localhost:8000/exchangerates/rates/a/AUD/last/5/
```
-To query operation 3, run this command:
```
curl http://localhost:8000/exchangerates/rates/c/AUD/last/5/
```