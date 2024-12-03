## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/assami1337/OTRPO_lab8.git
cd OTRPO_lab8
```
### 2. Установка зависимостей
Убедитесь, что у вас установлен Python 3.7 или выше. Установите зависимости:
```bash
pip install -r requirements.txt
```
### 3. Настройка переменных окружения
1. Скопируйте файл `.env.example` в `.env`:
```bash
cp .env.example .env
```
2. Откройте `.env` и заполните необходимые значения:
- `BOT_TOKEN`: токен вашего Telegram-бота.
- `SMTP_SERVER`: smtp.yandex.ru
- `SMTP_PORT`: 465
- `SMTP_LOGIN`: ваш email.
- `SMTP_PASSWORD`: пароль приложения для SMTP.

### 4. Запуск бота
```bash
python main.py
```
Теперь бот доступен для взаимодействия в Telegram.
