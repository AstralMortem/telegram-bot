# TELEGRAM BOT
Для виконнаня ТЗ було обрано відпоівдний стек технології з силками на їх документацію, якою я часто користувавася

Стек:
* База Данних
    * [PostgreSQL](https://www.postgresql.org/docs/)
* Бекенд:
    * [FastAPI](https://fastapi.tiangolo.com/tutorial/)
    * [Aiogram](https://docs.aiogram.dev/en/dev-3.x/)
    * [SocketIO for Python](https://python-socketio.readthedocs.io/en/stable/)
    * [sqlalchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
    * [pydantic](https://docs.pydantic.dev/latest/api/base_model/)
    * [Python3.12](https://www.python.org/)
* Фронтенд:
    * [VueJS](https://vuejs.org/guide/introduction.html)
    * [TailwindCSS](https://tailwindcss.com/docs/installation)
    * [Pinia](https://pinia.vuejs.org/introduction.html)
    * [Node + npm](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
    * [SocketIO](https://socket.io/docs/v4/)
    * [VueTG](https://vue-tg.pages.dev/)
* Деплой:
    * [Docker](https://docs.docker.com/manuals/)

## BACKEND

Створення середовища розробки за допомогою пакетного менеджера Poetry
```
poetry new backend
```
-----
#### Створюємо структуру проекту

Створюємо файл config.py в якому будуть основні налаштування серверу. Використовуючи бібліотеку `pydantic-settings` створюємо клас `Settings()` та викликаємо його. В ньому через .env передамо серкертний токен бота, налаштування БД та інше.

В головному файлі `app.py` ініціюємо бота aiogram, диспечера, websocketIO та FastAPI. Для зєднання з сервером телеграм та ботом, я вибрав метод через [webhooks](https://core.telegram.org/bots/webhooks), коли бот не запитує сервер кожні 5с. 'чи є нові данні?', а ми надаєм серверу телеграм шлях, по якому він нам надсилатиме нові данні при їх зміні. 
Для цього створив функцію lifespan яка викликається кожного разу при запуску сервера бекенду, де встановив шлях до вебхуку.
```
@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
    await init_db()
    yield

    await bot.session.close()
    logging.info("Bot stopped")
```

а в FastAPI визначив webhook route

```
@app.post(settings.WEBHOOK_PATH)
async def webhook(request: Request):
    telegram_update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, telegram_update)
```

З мінусів:
* Telegram вимагає щоб хост мав SSL сертифікати і зєднання було через https протокол, при деплоїнгу це не проблема, при локальній розробці використовува тунелі через `ngrok`
---

Далі створив папку db де у файлі 
* `connect.py` - Створив асинхрону сесію з БД
* `models.py` - Описав таблиці в БД за допомогою sqlalchemy ORM
* `schema.py` - Описав серіалізатори для кожної моделі ORM, використовуючи Pydantic

`models.py` - в даному проекті лише 2 таблиці:
* `users` - Зберігає користувача телеграм, такі поля:
    * `id` - User Telegram ID
    * `usernam` - Telegram username
    * `silver_amount`
    * `gold_amount`
    * `image_url` - User profile picture path
    * `created_at` 
    * `is_active`

* `gold_transaction` - Зберігає кожну транзакцію яку зробив користувач, такі поля:
    * `id`
    * `total_gold` - загальна к-ть золота в додатку, по дефолту 1ККК
    * `gold_price` - нова ціна золота розрахована через BoundingCurve 
    * `old_gold_price` - ціна золота з якою провелась транзакція
    * `user_id` - id користувача
    *  `type` - тип транзакції(`+` якщо покупка, `-` якщо продажа)
    *  `created_at`

`connect.py` - містить функцію init_db(), якщо БД пуста, ми створюємо першу транзакцію в якій к-ть золота в додатку 1ККК, а його ціна 1. 

---
Створив файл `services.py` - в цьому файлі створені класи які працюють з моделями ОRM та вхідними даними. Дані сервіси викликатимуться в роутерах методом dependecy injection.

`UserService` - клас який працює з користувачами

* `get_users()` - отримати всіх користувачів з пагінацією

* `get_user(id)` - отримати конкретного користувача

* `create_user(data)` - створити нового користувача


`GoldService` - сервіс по роботі з транзакціями


* `get_last_gold()` - метод, який отримує з Таблиці останню транзакцію, для того щоб отримати останню ціну за золото та їх к-ть.

* `buy_gold(user_id, amount)` - метод в якому користувач купляє золото. Отримуємо користувача та к-ть срібла, перевіряємо чи є в користувача така к-ть. Створюємо нову транзакцію з новою к-тю золота, та новою ціною вирахуваною за методом bounding curve, також оновлюємо к-ть золота та срібла користувача.

* `sell_gold(user_id, amount)`* - аналогічно як і `buy_gold` але ми отримуємо золото а не срібло, та зменшуємо к-ть золота в додатку і в користувача.

* `bounding_curve_price(amount)` - функція яка розраховує нову ціну золота 
---
### Bounding Curve
Крива зв’язку – це математична концепція, яка використовується для опису зв’язку між ціною та пропозицією активу.
При створенні алгоритму використовував [цю статтю](https://yos.io/2018/11/10/bonding-curves/)
Для алгоритму було вирішено використовувати експоненціальний закон, провівши аналіз отримав таку формулу

$P = P_0 * e^{k(S-S_0)}$, $k = {1 \over S_0}$

де $S_0$ - початкова к-ть токенів, $P_0$ - початкова ціна токена,
$P$ - нова ціна токена, $S$ - нова к-ть токенів

Наприклад якщо користувач хоче купити 10 токенів а початкова к-ть токенів 100, то $S= 100 + 10 = 110$, якщо продати 10, то $S = 100 - 10 = 90$

Для агресивнішого росту ціни активу, можна скорегувати коефіцієнт $k$, збільшивши чисельник, наприклад для $S_0 = 1000000000$, оптимальни коефіцієнт $k = { 100000\over S_0}$

функція на Python:

```
def bounding_curve_price(self, amount):
        k = settings.BOUNDING_CURVE_KOEF / settings.INITIAL_GOLD_SUPPLY
        result = settings.INITIAL_GOLD_PRICE * math.exp(
            k * (amount - settings.INITIAL_GOLD_SUPPLY)
        )
        return round_decimal(result, 4)
```
---

далі створив папку routers де налаштував роутери для FastAPI та бота.
Для FastAPI налаштовані різні шляхи, наприклад коли користувач хоче купити золото, він надстлає POST запит на шлях /buy_gold
```
@api_router.post("/buy_gold")
async def buy_gold(service: gold_service, data: GoldBody):
    gold, user = await service.buy_gold(data.user_id, data.amount)
    await sio.emit("gold:get", gold.model_dump_json())
    await sio.emit("user:current", user.model_dump_json())
    return user
```
де ми, використовуючи сервіс вираховуємо нову ціну, к-ть золота та оновлюємо користувача, використовуючи WebSocketIO, надсилаємо нові данні користувача та золота для всіх хто зєднаний з цим вебсокетом. Вебсокет описаний в `utils.py`
Для бота налаштована лише команда /start, при якій відкривається наш застосунок, та працює Middleware на реєстрацію користувача описаний в `utils.py`

## FRONTEND

Для фронтенд технології було орано VueJS. Ініціював новий проект за допомогою npm
```
npm create vite@latest frontend -- --template vue
```
Даний фронтенд має 2 екрани:
* `HomeView` - на якому ціна та к-ть золотих токенів. Список користувачів з їхнім статком, та 2 кнопки купити та продати
* `UserView` - на якому інформація про користувача, його статок, скільки в нього золота та срібла.

Для отримання данних з бекенду використовува `axios` та `socket.io-client`, описані в директорії `plugins/`

Для збереження користувачів та транзакцій, використовува state manager `Pinia`. в `stores/gold.ts` описаний state для золота, кожний компонент якому потрібно отримати данні по золоту звертається сюди. Аналогічно з користувачами описаними в `stores/users.ts`

В самих store описані методи які отримують данні з бекенду, а також для всіх метод `bindEvents()` який викликається після ініціалізації в корeневій сторінці `App.vue`. В цьому методі описане зєднання з вебсокетом, та дії при отриманні відповідного сигналу з серверу.

Вебсокет використовується для того, щоб в реальному часі отримувати данні по к-ті токенів та їхній ціні.

## Deploy
Для деплоїнгу сервісів було вирішено використовувати Docker compose.
Створив папку Docker а в кожній папці на кожний сервіс Dockerfile. 
В Dockerfile - прописав як скомпілювати чи запустити сервіс.

В загалом 4 сервіси:
* `backend` - сервер бекенду
* `frontend` - сервер фронтенду
* `db` - PostgreSQL
* `reverse-proxy` - Реверс-проксі на traefik, для того щоб на одном домені був доступ до різних сервісів. Також швидке отримання сертифікатів для https


