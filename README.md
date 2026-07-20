# Проект примера автотестов
### Установка и настройка виртуального окружения
```bash
python3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
### Makefile
- `make lint` - использовать линтер ruff
### pre-commit
- Чтобы использовать pre-commit хук:
```bash
pip install pre-commit
pre-commit install
```
### Allure
- Установка аллюра со scoop:
```shell
scoop install allure
```
- Запуск аллюр отчета локально
```bash
allure serve allure-results
```

### Assertions
```python
expected = "Что ожидаем"
assertion = "Что на самом деле пришло"
# Слева всегда фактическое значение, справа ожидаемое, потом сообщение
assert assertion == expected, "Сообщение, которое выведется при ошибке сравнения"

from hamcrest import assert_that, equal_to

assert_that(  # Тот же порядок
    assertion,
    equal_to(expected),
    "Сообщение, которое выведется при ошибке сравнения",
)
```
