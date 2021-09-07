# SSL Host Expiration Checker from ak545
**ssl-check.py** - This is a python script to check expiration dates of ssl certificate registrations for your websites.


## Screenshots
![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/script0.png)
> Script. Options

![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/script1.png)
> Script in working

![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/script2.png)
> Script in working

![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/email.png)
> A sample of the email

![](https://raw.githubusercontent.com/ak545/ssl-host-expiration-checker/main/images/telegram.png)
> A sample of the Telegram message

## Description
You can install and run **ssl-check.py** to monitor your websites ssl certificate registration expiration dates. If you add this script to the task scheduler (for example, to cron, if you have Linux or to Task Scheduler, if you have Windows), then it will monitor the timeliness of updating the expiration dates for registration of ssl certificates of your websites. If the deadline for the registration of ssl certificates of your websites will soon come, the script will notify you in time (either by email or Telegram or directly in the console). If you own multiple ssl certificates for your websites, this script will also help standardize all ssl certificate expiration notifications for those websites.

## Installation
The script requires **Python version 3.6 or higher**.
Of course, you need to install it yourself first [Python](https://www.python.org/). On Linux, it is usually already installed. If not, install it, for example:

```console
$ sudo yum install python3
$ sudo dnf install python3
$ sudo apt install python3
$ sudo pacman -S python
```

For Apple macOS:

Install brew:
```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install Python:

```console
$ export PATH=/usr/local/bin:/usr/local/sbin:$PATH
$ brew install python
```

Note: [brew](https://brew.sh/)

For Microsoft Windows download the [distribution package](https://www.python.org/downloads/windows/) and install it. I recommend downloading "Download Windows x86 executable installer" if you have a 32-bit OS and "Download Windows x86-64 web-based installer" if you have a 64-bit OS. During installation, I recommend checking all options (Documentation, pip, tcl / tk and IDLE, Python test suit, py launcher, for all users (requeres elevation)).

Previously, you may need to update **pip** itself (Python module installer):
```console
$ python -m pip install --upgrade pip
```

### Installing and update dependencies
```console
$ pip install -U colorama
```
and
```console
$ pip install -U requests[socks]
```    
or
```console
$ pip install -U PySocks
```

If you are running Linux or macOS, and you plan to run the script as the current user, then additionally specify the **--user** option. In this case, the necessary dependencies will be installed into the home folder of the current system user and are available when launched from the task scheduler (cron) on behalf of this current user.

Depending on your Pyton environment, your actions will be slightly different, for example, you may need to specify the **--user** key (for **pip**) or use the **python3** and **pip3** commands instead of the **python** and **pip** commands. If you use [virtual environments](https://docs.python.org/3/library/venv.html), then most likely, you will need to do all of these actions after entering the appropriate environment.

## Usage
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

### Description of options
**-h, --help**

Help

**-v, --version**

Display the version number

**-f FILE, --file FILE**

Path to the file with the list of hosts (default is None)

The file must be encoded in **UTF-8 without BOM**, the format of the new line: **Unix (0Ah)**


#### Sample domain list file
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
mail.yandex.ru```

**-o STRING, --host STRING**

Host to check the expiration date of the ssl certificate (default is None)

**-c, --print-to-console**

Enable console printing (default is False)

**-dw DAYS, --days-to-warn DAYS**

Warn me when there are less than DAYS days left (default is 7).
How many days in advance to warn about the expiration of the ssl certificate.

**-t, --use-telegram**

Send a warning message through the Telegram (default is False)

**-p URL, --proxy URL**

Proxy link (for Telegram only), for example: socks5://127.0.0.1:9150 (default is None).

**-e EMAIL, --email-to EMAIL**

Send a warning message to email address (default is None)
Here you must specify the email address of the recipient.

**-subject STRING, --email-subject STRING**

Append custom text to the email subject (default is None). This is an additional option for --email-to.

**-ssl, --email-ssl**

Send email via SSL (default is False). This is an additional option for --email-to.

**-auth, --email-auth**

Send email via authenticated SMTP (default is False). This is an additional option for --email-to.

**-starttls, --email-starttls**

Send email via STARTTLS (default is False). This is an additional option for --email-to.

**-nb, --no-banner**

Do not print banner (default is False).
Banner is information about the script execution environment: Python version, computer name, OS name, OS release, OS version, architecture, CPU, summary table of preset options.


## Global constants in the script

Some options are inside the script. There is no point in putting them in the parameters, since you only need to configure them once, and then successfully forget about them.

You may also set environment variables of the same name for SMTP and TELEGRAM to avoid modifying the script.

### SMTP options
**SMTP_SERVER**

SMTP server address

Samples:

```python
    SMTP_SERVER = os.getenv("SMTP_SERVER", "localhost")
    # SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
```

**SMTP_PORT**

SMTP port

Samples:

```python
    # SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # For starttls
    # SMTP_PORT = int(os.getenv("SMTP_PORT", 465))  # For SSL
    SMTP_PORT = int(os.getenv("SMTP_PORT", 25))   # Default
```

**SMTP_SENDER**

Email address of the sender

Samples:

```python
    SMTP_SENDER = os.getenv("SMTP_SENDER", "user@gmail.com")
```

**SMTP_PASSWORD**

SMTP password

Samples:

```python
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "P@ssw0rd")
```

### Telegram options
**TELEGRAM_TOKEN**

Token Telegram bot

Samples:

```python
    TELEGRAM_TOKEN = 'NNNNNNNNN:NNNSSSSaaaaaFFFFFEEE3gggggQQWFFFFF01z'
```

**TELEGRAM_CHAT_ID**

Telegram Channel ID

Samples:

```python
    TELEGRAM_CHAT_ID = '-NNNNNNNNN'
```

Get help with Telegram API:
[https://core.telegram.org/bots](https://core.telegram.org/bots)
You can create a bot by talking to Telegram with [**@BotFather**](https://telegram.me/BotFather)

**TELEGRAM_URL**

Telegram API URL

Samples:

```python
    TELEGRAM_URL = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/"
```

## How to add a script to Linux cron
To do this, create a **crontab** task that will be executed, for example, every midnight on behalf of the user (creating tasks as root is not the best idea):

Suppose your Linux username is: **user**

Your home folder: **/home/user**

The folder where this script is located: **/home/user/py**

To run the script directly, run the command:
```console
$ chmod +x /home/user/py/ssl-check.py
```

Adjust in the first line of the script [Shebang (Unix)](https://en.wikipedia.org/wiki/Shebang_(Unix)), eg:

Show the path where python is located:
```console
$ which python
```
or
```console
$ which python3
```
Correction python path in Shebang:

```python
#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python
#!/usr/bin/env python3
```

Rename script:

```console
$ mv /home/user/py/ssl-check.py /home/user/py/ssl-check
```
Check script launch:

```console
$ /home/user/py/ssl-check -h
$ /home/user/py/./ssl-check -h
```
If everything is fine, run the editor **crontab**, if not, go back to setting **Shebang**:

```console
$ crontab -u user -e
```
Here **user** - is your Linux login

If you, like me, do not like vim (I have not seen a single person who is fluent in this editor, although it probably exists somewhere), you can edit the tasks in your favorite editor, for example:

```console
$ EDITOR=nano crontab -u user -e
$ EDITOR=mcedit crontab -u user -e
```
or

```console
$ VISUAL=nano crontab -u user -e
$ VISUAL=mcedit crontab -u user -e
```

In the task editor, create something like this (do not use keys **--print-to-console**):

`0 0 * * * /home/user/py/ssl-check -nb -f /home/user/data/hosts-sample.txt -t -auth -e my@email.com >/dev/null 2>&1`

or

`0 0 * * * /home/user/py/./ssl-check -nb -f /home/user/data/hosts-sample.txt -t -auth -e my@email.com >/dev/null 2>&1`


Specify the full paths to the data file and the script.

Note: [cron](https://en.wikipedia.org/wiki/Cron)

You can view created tasks for user **user** like this:

```console
$ crontab -u user -l
```
Delete all tasks from user **user**, you can:

```console
$ crontab -u user -r
```
## How to add a script to Microsoft Windows Task Scheduler
Ask for help to [documentation](https://docs.microsoft.com/en-us/windows/desktop/taskschd/schtasks)

**Sample:**

`> schtasks /Create /SC DAILY /TN "SSL Expiration Checker" /TR "'с:\ssl-check.py' -nb -t -auth -e my@email.com -f 'c:\hosts-sample.txt'" /ST 23:59`

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Restrictions
I, the author of this python script, wrote this script exclusively for my needs. No warranty is provided. You can use this script freely, without any deductions, for any purpose other than illegal.

You can make any changes to the script code and fork this script, provided that the link to [me](https://github.com/ak545) is indicated as a source of your inspiration.

## Postscriptum
- The script was tested in Microsoft Windows 10/11, Linux Fedora 34, Linux Debian 9/10/11, Linux Ubuntu Desktop 18.04/20.04/21.04, Linux CentOS 6/7, Linux Manjaro 21.0.6/21.0.7.
- Sorry for my bad English.
- The program code of the script is not perfect. But please forgive me for that.
- All recommendations given by me for Apple macOS may contain inaccuracies. Sorry, I don’t have an Apple macBook on hand (but what if someone gives it to me?).
- Glory to the E = mc &sup2; !
- I wish you all good luck!

## A final plea
It's time to put an end to Facebook. Working there is not ethically neutral: every day that you go into work, you are doing something wrong. If you have a Facebook account, delete it. If you work at Facebook, quit.

And let us not forget that the National Security Agency must be destroyed.

*(c) [David Fifield](mailto:david@bamsoftware.com)*

---

> Best regards, ak545 ( ru.mail&copy;ak545&sup2; )