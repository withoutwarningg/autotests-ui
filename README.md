# UI Automation Project

Учебно-тренировочный проект UI-автоматизации на **Python + Playwright +
pytest + Allure**, построенный на паттерне **Page Object**. В качестве
объекта тестирования — [saucedemo.com](https://www.saucedemo.com/), демо
интернет-магазин, специально сделанный командой Sauce Labs для практики
автоматизации (стабильный, с документированными тестовыми пользователями).

## Архитектура

```
tests/  (что проверяем)
  │  вызывает методы Page Object, работает только с бизнес-действиями
  ▼
pages/  (Page Object)
  │  LoginPage, InventoryPage, CartPage, CheckoutStepOnePage,
  │  CheckoutStepTwoPage, CheckoutCompletePage — каждый инкапсулирует
  │  локаторы и действия ОДНОЙ страницы, наследуется от BasePage
  ▼
BasePage
  │  общее для всех страниц: открытие по относительному пути, локаторы
  ▼
Playwright (Page) → saucedemo.com
```

Тесты не содержат ни одного CSS/`data-test`-селектора и ни одного вызова
Playwright API напрямую — только вызовы методов Page Object
(`login_page.login(...)`, `inventory_page.add_to_cart(...)`,
`cart_page.checkout()` и т.д.). Это и есть смысл паттерна: поменяется
вёрстка страницы — правки только в одном файле в `pages/`, тесты не
трогаем.

### Структура репозитория

```
autotests-ui/
├── config/
│   └── settings.py          # UI_BASE_URL / UI_TIMEOUT_MS из переменных окружения
├── pages/
│   ├── base_page.py         # BasePage — общий фундамент
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py     # CheckoutStepOnePage/TwoPage/CompletePage
├── tests/
│   ├── conftest.py          # фикстуры: browser_context_args, login_page, logged_in_page
│   ├── data/
│   │   └── users.py         # тестовые пользователи saucedemo (dataclass)
│   └── ui/
│       ├── test_login.py            # позитив + параметризованный негатив
│       ├── test_inventory.py        # каталог, сортировка, корзина
│       └── test_checkout.py         # полный флоу оформления заказа
├── pytest.ini
├── requirements.txt
├── .env.example
└── README.md
```

## Tech Stack

- **Python 3.11+**
- **Playwright** (sync API) — управление браузером
- **pytest** + **pytest-playwright** — раннер, фикстуры `page`/`browser`,
  CLI-флаги (`--headed`, `--browser`, `--slowmo` и т.д.) из коробки
- **Allure** — отчётность
- **python-dotenv** — конфигурация через `.env`

## Установка

```bash
git clone https://github.com/withoutwarningg/autotests-ui.git
cd autotests-ui
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium    # или: playwright install --with-deps chromium
```

Конфигурация не обязательна — по умолчанию тесты идут на
`https://www.saucedemo.com`. При необходимости скопируйте `.env.example`
в `.env` и переопределите `UI_BASE_URL` / `UI_TIMEOUT_MS`.

## Запуск тестов

```bash
pytest                          # весь набор, headless, Chromium
pytest --headed                 # с открытым окном браузера (флаг pytest-playwright)
pytest --browser firefox        # другой браузер (chromium/firefox/webkit)
pytest -m smoke                 # только smoke-подмножество
pytest -m "regression and not negative"
pytest tests/ui/test_login.py -v
```

Allure-результаты пишутся в `reports/allure-results/`. Просмотр отчёта
(нужен установленный [Allure CLI](https://allurereport.org/docs/install/)):

```bash
allure serve reports/allure-results
```

## Маркеры pytest

| Маркер | Смысл |
|---|---|
| `smoke` | минимальный набор, покрывающий основные happy-path сценарии |
| `regression` | более широкий набор (сортировки, доп. сценарии корзины/чекаута) |
| `negative` | ошибки, валидация форм, граничные случаи |

## Тестовые пользователи

Все данные официально задокументированы прямо на странице логина
saucedemo.com (не секрет), пароль у всех один — `secret_sauce`:

| Пользователь | Поведение |
|---|---|
| `standard_user` | обычный, всё работает |
| `locked_out_user` | залогиниться нельзя, показывается ошибка |
| `problem_user` | логинится, но есть визуальные баги в каталоге |
| `performance_glitch_user` | логинится с искусственной задержкой |
| `error_user` | логинится, но есть баги в отдельных действиях |
| `visual_user` | логинится, визуальные отличия от эталона |

## Расширение фреймворка

- Новая страница сайта → новый файл в `pages/` по образцу существующих
  (наследник `BasePage`), локаторы — константы класса, действия — методы.
- Новые тестовые пользователи/данные → `tests/data/`, не хардкодить
  логины/пароли в тестах.
- Кросс-браузерный прогон в CI: `pytest --browser chromium --browser firefox`
  (pytest-playwright поддерживает несколько `--browser` флагов за один запуск).

## Project status

Learning UI Automation with Python + Playwright.
