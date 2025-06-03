Простая подсистема хранения данных для системы обнаружения трещин в стеклянных изделиях. Реализована на Flask + SQLAlchemy + SQLite.

---

Установка
```
pip install -r requirements.txt
```

Запуск
```
set FLASK_APP=app.py
flask run
```

Запросы

Получить список трещин
```
curl http://127.0.0.1:5000/cracks
```

Добавить одну трещину
```
curl -X POST "http://127.0.0.1:5000/cracks?location=corner&length=12.5&depth=1.2&status=minor"
```

Удалить трещину по ID
```
curl -X DELETE http://127.0.0.1:5000/cracks/1
```

Массовая загрузка из JSON
```
curl -X POST http://127.0.0.1:5000/cracks/upload_json ^
  -F "file=@cracks.json;type=application/json"
```
