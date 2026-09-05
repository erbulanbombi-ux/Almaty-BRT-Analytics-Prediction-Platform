# Almaty LRT Simulation Lab

Интерактивный исследовательский прототип для анализа будущей LRT-сети Алматы. Главный сценарий проекта находится на одной странице:

`LRT route → stations → predicted delay → simulation result`

> Данные и расчёты в текущей версии синтетические. Проект демонстрирует инженерный и ML-подход, но не является официальным прогнозом транспортной системы Алматы.

![CI](https://github.com/erbulanbombi-ux/Almaty-LRT-Analytics-Prediction-Platform/actions/workflows/ci.yml/badge.svg)

## Что можно сделать

- выбрать станции отправления и назначения;
- найти кратчайший путь по LRT-сети алгоритмом Dijkstra;
- изменить `traffic`, `passenger demand` и `LRT frequency`;
- увидеть, как меняются задержка, время поездки и вероятность соблюдения расписания;
- обучить модель `HistGradientBoostingRegressor` на демонстрационном датасете;
- сравнить модель с Ridge baseline и проверить её через `TimeSeriesSplit`;
- открыть EDA notebook с распределениями и корреляциями.

## Запуск demo

Для статического интерактивного demo:

```powershell
python -m http.server 5500
```

Откройте <http://localhost:5500>.

Страница работает без Python API: simulation и поиск маршрута выполняются в браузере. Поэтому demo удобно показывать локально даже без сервера модели.

## Запуск ML API

Создайте окружение и установите зависимости:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Обучите модель и запустите API:

```powershell
python train.py
uvicorn app:app --reload
```

Доступные endpoints:

- `GET /health` — состояние модели;
- `POST /predict` — прогноз задержки по признакам;
- `POST /simulate` — расчёт сценария движения;
- `POST /route` — кратчайший маршрут Dijkstra.

Полная интерактивная документация API доступна автоматически по `/docs`, а README намеренно оставлен коротким.

## Модель и данные

`train.py` сохраняет модель в `models/brt_model.joblib`, а метрики в `reports/metrics.json`. Исторические имена `brt_*` оставлены для совместимости с текущими файлами проекта.

Признаки модели включают уклон, степень изоляции коридора, конфликтные повороты, пассажиропоток, предыдущие задержки, коридор, погоду и час пик. Целевая переменная — `delay_minutes`.

Метрики последнего обучения нельзя переносить на реальную LRT-систему: датасет синтетический и нужен для проверки pipeline.

## Алгоритм маршрута

`route_planner.py` содержит взвешенный граф станций и реализацию Dijkstra. Вес ребра — расстояние между станциями в километрах. Алгоритм возвращает список станций оптимального пути и его длину.

## Структура

```text
├── index.html              # Одностраничное интерактивное demo
├── style.css               # Интерфейс Simulation Lab
├── script.js               # Dijkstra и simulation в браузере
├── app.py                  # FastAPI endpoints
├── route_planner.py        # Граф LRT и Dijkstra
├── train.py                # Обучение и TimeSeriesSplit
├── predict.py              # Локальный прогноз
├── data_generator.py       # Синтетические данные
├── visualize.py            # Графики и permutation importance
├── notebooks/01_eda.ipynb  # Исследовательский notebook
├── tests/                  # Smoke-тесты
├── Dockerfile              # Запуск API в контейнере
└── .github/workflows/ci.yml # Проверки при push и pull request
```

## Проверки

```powershell
python -m pytest -q
python -m py_compile app.py route_planner.py train.py predict.py visualize.py data_generator.py
```

CI автоматически запускает обучение и тесты при каждом push или pull request.

## Следующие шаги

1. Подключить реальные GTFS/GPS-данные после проверки лицензии и качества источника.
2. Добавить SHAP для объяснения отдельных прогнозов.
3. Добавить prediction intervals после выбора и валидации quantile-модели.
4. Заменить демонстрационный граф на подтверждённую схему станций и пересадок.
5. Опубликовать API после настройки секретов, мониторинга и отдельного deployment-конфига.

## Лицензия

Лицензия проекта пока не указана. Перед публичным релизом добавьте фактическую лицензию и проверьте права на материалы в `assets/`.
