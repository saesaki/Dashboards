# Программа: Дашборд для анализа погоды в Комсомольске-на-Амуре

## Описание
Данный проект представляет собой дашборд для визуализации погодных данных с использованием Python и библиотеки Dash.
Программа отображает графики температуры, давления, облачности и розы ветров для выбранного города на основе данных из CSV-файла.

## Основные функции
- **Таблица данных**: Вывод исходных данных в виде таблицы.
- **График температуры и давления**: Линейный график изменения температуры или давления в течение времени.
- **Круговая диаграмма облачности**: Визуализация частоты различных уровней облачности.
- **Роза ветров**: График направления и средней скорости ветра в разное время суток.
- **Выбор города и параметров**: Интерактивный выбор города и временного интервала с помощью Dropdown и RadioItems.

## Установка и запуск
### Требования:
- Python 3.11+
- Установленные библиотеки:
  - pandas
  - plotly
  - dash

### Установка зависимостей:
```bash
pip install pandas plotly dash
```

### Запуск приложения:
```bash
python main.py
```

## Структура кода
- **main.py** – основной файл программы с определением интерфейса и логики обратного вызова (callback).
- **data.csv** – CSV-файл с погодными данными.

## Как использовать
1. Запустите программу.
2. В браузере откроется страница с дашбордом.
3. Выберите город из выпадающего списка.
4. Используйте переключатели для отображения температуры, давления или облачности.
5. Просмотрите графики изменений температуры и давления за день и вечер.
6. Постройте розу ветров, выбрав время суток (день или вечер).

## Источник данных
CSV-файл с названием data.csv находится в директории проекта


## Запуск на сервере

```bash
sudo ufw allow 8050
source venv/bin/activate
python3 Dashboards/main.py
```


