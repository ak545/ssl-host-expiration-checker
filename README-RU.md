# SSL Host Expiration Checker from ak545
**ssl-check.py** - Это python-скрипт для проверки сроков окончания регистрации ssl-сертификатов для ваших веб-сайтов.

## Скриншоты
![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/script0.png)
> Скрипт. Опции

![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/script1.png)
> Скрипт в работе

![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/script2.png)
> Скрипт в работе

![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/email.png)
> Пример email

![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/telegram.png)
> Пример Telegram сообщения


## Описание
Вы можете установить и запустить **ssl-check.py** для мониторинга сроков окончания регистрации ssl-сертификатов ваших веб-сайтов. Если вы добавите этот скрипт в планировщик заданий (например, в cron, если у вас Linux или в Task Scheduler, если у вас Windows), то он будет следить за своевременностью обновления сроков окончания регистрации ssl-сертификатов ваших веб-сайтов. Если скоро наступят сроки окончания регистрации ssl-сертификатов ваших веб-сайтов, скрипт вовремя сообщит вам об этом (или по электронной почте или по Telegram или непосредственно в консоли). Если вы владеете несколькими ssl-сертификатами для ваших веб-сайтов, этот скрипт так же поможет стандартизировать все уведомления об истечении сроков окончания регистрации ssl-сертификатов этих веб-сайтов.

## Инсталляция
Для работы скрипта необходим **Python версии 3.6 или выше**.
Разумеется, необходимо сперва установить сам [Python](https://www.python.org/). В Linux он обычно уже установлен. Если нет, установите его, например:

```console
$ sudo yum install python3
$ sudo dnf install python3
$ sudo apt install python3
$ sudo pacman -S python
```

Для Apple macOS:
    
Установите brew:

```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Установите Python:

```console
$ export PATH=/usr/local/bin:/usr/local/sbin:$PATH
$ brew install python
```

Примечание: [brew](https://brew.sh/index_ru)

Для Microsoft Windows скачайте [дистрибутив](https://www.python.org/downloads/windows/) и установите его. Я рекомендую скачивать "Download Windows x86 executable installer" если у вас 32-х битная ОС и "Download Windows x86-64 web-based installer" если у вас 64-х битная ОС. Во время установки рекомендую отметить все опции (Documentation, pip, tcl/tk and IDLE, Python test suit, py launcher, for all users (requeres elevation)).

Предварительно, возможно понадобится обновить сам **pip** (установщик модулей Python):

```console
$ python -m pip install --upgrade pip
```

### Установка и обновление зависимостей
```console
$ pip install -U colorama
```
и
```console
$ pip install -U requests[socks]
```
или
```console
$ pip install -U PySocks
```
Если Вы работаете под управлением Linux или macOS, и запуск скрипта планируете производить от имени текущего пользователя, то дополнительно указывайте опцию **--user**. В этом случае необходимые зависимости будут устанавливаться в домашнюю папку текущего пользователя системы и доступны при запуске из планировщика задач (cron) от имени этого текущего пользователя.

В зависимости от вашего Pyton окружения, ваши действия будут немного иными, например, возможно, вам потребуется указать ключ **--user** (для **pip**) или вместо команд **python** и **pip** использовать команды **python3** и **pip3**. Если вы используете [виртуальные окружения](https://docs.python.org/3/library/venv.html), то скорее всего, все эти действия вам необходимо будет сделать после входа в соответствующее окружение.

## Использование
```console
$ ssl-check.py -h

usage: ssl-check.py [Options]

SSL Host Expiration Checker
A simple python script to display or notify a user by email and/or via Telegram
about the status of the SSL certificates expiration date of the host.

Options:
  -h, --help            Help
  -v, --version         Display the version number
  -f FILE, --file FILE  Path to the file with the list of hosts (default is None)
                        Sample:
                                MyHosts.txt
  -o STRING, --host STRING
                        Host to check the expiration date of the ssl certificate (default is None)
                        Sample:
                                google.com
  -c, --print-to-console
                        Enable console printing (default is False)
  -dw DAYS, --days-to-warn DAYS
                        Warn me when there are less than DAYS days left (default is 7)
  -t, --use-telegram    Send a warning message through the Telegram (default is False)
  -p URL, --proxy URL   Proxy link (for Telegram only, default is None)
                        Sample (for example, when the Tor browser is running):
                                socks5://127.0.0.1:9150
  -e EMAIL or EMAIL'S, --email-to EMAIL or EMAIL'S
                        Send a warning message to email address (default is None)
                        Sample:
                                email@mail.dot
                        Or multiple address (the addresses are separated by commas,
                        and the entire string is enclosed in double quotes):
                                "email1@mail.dot, email2@mail.dot, email3@mail.dot"
  -subject STRING, --email-subject STRING
                        Append custom text to the email subject (default is None)
  -ssl, --email-ssl     Send email via SSL (default is False)
  -auth, --email-auth   Send email via authenticated SMTP (default is False)
  -starttls, --email-starttls
                        Send email via STARTTLS (default is False)
  -nb, --no-banner      Do not print banner (default is False)

(c) AK545 (Andrey Klimov) 2021, e-mail: ak545 at mail dot ru
```

### Описание опций
**-h, --help**

Помощь

**-v, --version**
    
Показать номер версии

**-f FILE, --file FILE**

Путь к файлу со списком хостов (по умолчанию Нет)

Файл должен быть в кодировке **UTF-8 без ВОМ**, формат новой строки: **Unix (0Ah)**

#### Пример файла со списком доменов
```bash
# Host Group 1
google.com
google.ru
youtube.com
facebook.com
twitter.com
microsoft.com
github.com

# Host Group 2
livejournal.com
teletype.in
habr.com
codepen.io
mail.ru
yandex.ru
mail.yandex.ru
```

**-o STRING, --host STRING**

Хост для проверки срока действия ssl-сертификата (по умолчанию Нет)

**-c, --print-to-console**

Включить печать в консоли (по умолчанию False)

**-dw DAYS, --days-to-warn DAYS**

Предупредить меня, когда осталось меньше чем ДНЕЙ (по умолчанию 7)
За сколько дней предупреждать об окончании срока действия ssl-сертификата.

**-t, --use-telegram**

Отправить предупреждающее сообщение через Telegram (по умолчанию False)

**-p URL, --proxy URL**

Ссылка на прокси (только для Telegram), например: socks5://127.0.0.1:9150 (по умолчанию None).

**-e EMAIL, --email-to EMAIL**

Отправить предупреждение на адрес электронной почты (по умолчанию Нет). Здесь необходимо указать email адрес получателя.

**-subject STRING, --email-subject STRING**

Добавить свой текст в тему email-письма (по умолчанию Нет). Это дополнительная опция для --email-to.

**-ssl, --email-ssl**

Отправить email-письмо по протоколу SSL (по умолчанию False). Это дополнительная опция для --email-to.

**-auth, --email-auth**

Отправлять email-письмо через SMTP с авторизацией (по умолчанию False). Это дополнительная опция для --email-to.

**-starttls, --email-starttls**

Отправить email-письмо по протоколу STARTTLS (по умолчанию False). Это дополнительная опция для --email-to.

**-nb, --no-banner**

Не печатать баннер (по умолчанию False).
Баннер, это информация о среде исполнения скрипта: версия Python, имя компьютера, имя ОС, релиз ОС, версия ОС, архитектура, ЦПУ, сводная таблица предустановленных опций.


## Глобальные константы в скрипте
Часть опций находится внутри срипта. Нет никакого смысла выносить их в параметры, так как настроить их требуется всего один раз, после чего успешно о них забыть. 

### Параметры SMTP
**SMTP_SERVER**

адрес SMTP сервера

Примеры:

```python
    SMTP_SERVER = os.getenv("SMTP_SERVER", "localhost")
    # SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")    
```

**SMTP_PORT**

SMTP порт

Примеры:
    
```python
    # SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # Для starttls
    # SMTP_PORT = int(os.getenv("SMTP_PORT", 465))  # Для SSL
    SMTP_PORT = int(os.getenv("SMTP_PORT", 25))   # По умолчанию
```

**SMTP_SENDER**

Email адрес отправителя

Примеры:

```python
    SMTP_SENDER = os.getenv("SMTP_SENDER", "user@gmail.com")
```

**SMTP_PASSWORD**

SMTP пароль

Примеры:

```python
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "P@ssw0rd")
```

### Параметры Telegram
**TELEGRAM_TOKEN**

Токен Telegram бота

Примеры:

```python
    TELEGRAM_TOKEN = 'NNNNNNNNN:NNNSSSSaaaaaFFFFFEEE3gggggQQWFFFFF01z'
```

**TELEGRAM_CHAT_ID**

Идентификатор канала Telegram

Примеры :

```python
    TELEGRAM_CHAT_ID = '-NNNNNNNNN'
```

Получить помощь по API Telegram: 
[https://core.telegram.org/bots](https://core.telegram.org/bots)
Создать бота можно пообщавшись в Telegram с [**@BotFather**](https://telegram.me/BotFather)

**TELEGRAM_URL**

Telegram API URL

Примеры:

```python
    TELEGRAM_URL = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/"
```


## Как добавить скрипт в Linux cron
Для этого создайте **crontab** задачу, которая будет выполняться, например, каждую полночь от имени пользователя (создавать задачи от имени root не лучшая идея):

Предположим, ваш логин в Linux: **user**

Ваша домашняя папка: **/home/user**

Папка, где находится этот скрипт: **/home/user/py**

Чтобы запускать скрипт напрямую, выполните команду:
    
```console
$ chmod +x /home/user/py/ssl-check.py
```

Скорректируйте в первой строке скрипта [Шебанг (Unix)](https://ru.wikipedia.org/wiki/%D0%A8%D0%B5%D0%B1%D0%B0%D0%BD%D0%B3_(Unix)), например:

Показать путь, где расположен python:
    
```console
$ which python
```
или
```console
$ which python3
```
    
Коррекция пути python в Шебанг:

```python
#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python
#!/usr/bin/env python3
```

Переименуйте скрипт:

```console
$ mv /home/user/py/ssl-check.py /home/user/py/ssl-check
```

Проверьте запуск скрипта:

```console
$ /home/user/py/ssl-check -h
$ /home/user/py/./ssl-check -h
```

Если всё нормально, запустите редактор **crontab**, если нет, вернитесь к настройке **Шебанг**:

```console
$ crontab -u user -e
```
Здесь **user** - это ваш логин в Linux


Если вы, как и я не любите vim (я не видел ни одного человека, в совершенстве владеющего этим редактором, хотя, наверное, он где-то есть), вы можете редактировать задачи в вашем любимом редакторе, например, так:

```console
$ EDITOR=nano crontab -u user -e
$ EDITOR=mcedit crontab -u user -e
```
или
```console
$ VISUAL=nano crontab -u user -e
$ VISUAL=mcedit crontab -u user -e
```

В файле задач создайте примерно такую запись (не используйте ключи **--print-to-console**):

`0 0 * * * /home/user/py/ssl-check -nb -f /home/user/data/hosts-sample.txt -t -auth -e my@email.com >/dev/null 2>&1`

или

`0 0 * * * /home/user/py/./ssl-check -nb -f /home/user/data/hosts-sample.txt -t -auth -e my@email.com >/dev/null 2>&1`

Указывайте полные пути к файлу данных и скрипту.

Примечание: [cron](https://ru.wikipedia.org/wiki/Cron)

Посмотреть созданные задачи для пользователя **user** можно так:

```console
$ crontab -u user -l
```

Удалить все задачи пользователя **user** можно так:

```console
$ crontab -u user -r
```


## Как добавить скрипт в Планировщик заданий Microsoft Windows
Обратитесь за помощью к [документации](https://docs.microsoft.com/en-us/windows/desktop/taskschd/schtasks)

**Пример:**

`> schtasks /Create /SC DAILY /TN "SSL Expiration Checker" /TR "'с:\ssl-check.py' -nb -t -auth -e my@email.com -f 'c:\hosts-sample.txt'" /ST 23:59`

## Лицензия
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Ограничения
Я, автор этого python-скрипта, написал этот скрипт исключительно для своих нужд. Никаких гарантий не предоставляется. Вы можете использовать этот скрипт свободно, без каких либо отчислений, в любых целях, кроме противоправных.

Вы можете вносить любые правки в код скрипта и делать форк этого скрипта при условии указания ссылки на [меня](https://github.com/ak545), как источника вашего вдохновения.

## Постскриптум
- Работа скрипта проверялась в Microsoft Windows 10/11, Linux Fedora 34, Linux Debian 9/10/11, Linux Ubuntu Desktop 18.04/20.04/21.04, Linux CentOS 6/7, Linux Manjaro 21.0.6/21.0.7.
- Программный код скррипта не идеален. Но прошу простить меня за это. 
- Все рекомендации данные мной для Apple macOS могут содержать в себе неточности. Простите, у меня нет под рукой Apple macBook (но вдруг, кто-то подарит мне его?).
- Да здравствует E = mc&sup2; !
- Желаю всем удачи!

## Последняя просьба
Пришло время положить конец Facebook. Работа там не является нейтральной с этической точки зрения: каждый день, когда вы идете туда на работу, вы делаете что-то не так. Если у вас есть учетная запись Facebook, удалите ее. Если ты работаешь в Facebook, увольняйся.

И давайте не будем забывать, что Агентство национальной безопасности должно быть уничтожено.

*(c) [David Fifield](mailto:david@bamsoftware.com)*

---

> Best regards, ak545 ( ru.mail&copy;ak545&sup2; )