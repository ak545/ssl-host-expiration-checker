#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Program: SSL Host Expiration Checker from ak545
#
# Author of the original script: Andrey Klimov < ak545 at mail dot ru >
# https://github.com/ak545
#
# Current Version: 0.1.0
# Creation Date: 2021-08-12 (dd-mm-yyyy)
# Date of last changes: 2021-09-07 (dd-mm-yyyy)
#
# License:
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

from __future__ import unicode_literals

from typing import List
import os
import sys
import platform
import ssl
import socket
from datetime import datetime
import argparse
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import requests
except ImportError:
    sys.exit(
        """You need requests!
                install it from http://pypi.python.org/pypi/requests
                or run pip install requests"""
    )

try:
    from colorama import init
    from colorama import Fore, Back, Style
except ImportError:
    sys.exit(
        """You need colorama!
                install it from http://pypi.python.org/pypi/colorama
                or run pip install colorama"""
    )

# Init colorama
init(autoreset=True)

# Global constants
__version__ = "0.1.0"

# Check Python Version
if sys.version_info < (3, 6):
    print("Error. Python version 3.6 or later required to run this script")
    print("Your version:", sys.version)
    sys.exit(-1)

FR = Fore.RESET

FW = Fore.WHITE
FG = Fore.GREEN
FRC = Fore.RED
FC = Fore.CYAN
FY = Fore.YELLOW
FM = Fore.MAGENTA
FB = Fore.BLUE
FBC = Fore.BLACK

FLW = Fore.LIGHTWHITE_EX
FLG = Fore.LIGHTGREEN_EX
FLR = Fore.LIGHTRED_EX
FLC = Fore.LIGHTCYAN_EX
FLY = Fore.LIGHTYELLOW_EX
FLM = Fore.LIGHTMAGENTA_EX
FLB = Fore.LIGHTBLUE_EX
FLBC = Fore.LIGHTBLACK_EX

BLB = Back.LIGHTBLACK_EX
BLR = Back.LIGHTRED_EX
BRC = Back.RED
BG = Back.GREEN
BLG = Back.LIGHTGREEN_EX
BLC = Back.LIGHTCYAN_EX
BC = Back.CYAN
BLY = Back.LIGHTYELLOW_EX
BY = Back.YELLOW
BLW = Back.LIGHTWHITE_EX
BW = Back.WHITE
BR = Back.RESET

SDIM = Style.DIM
SNORMAL = Style.NORMAL
SBRIGHT = Style.BRIGHT
SR = Style.RESET_ALL

SEP: str = os.sep
pathname: str = os.path.dirname(os.path.abspath(__file__))

# Command line parameters
CLI = None

# SMTP options
SMTP_SERVER = os.getenv("SMTP_SERVER", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 25))

# SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
# SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # For starttls

# SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.mail.ru")
# SMTP_PORT = int(os.getenv("SMTP_PORT", 25))  # Default

# SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.yandex.ru")
# SMTP_PORT = int(os.getenv("SMTP_PORT", 465))  # For SSL

SMTP_SENDER = os.getenv("SMTP_SENDER", "root")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "P@ssw0rd")

if str(os.getenv("SMTP_CHECK_SSL_HOSTNAME")) == "0":
    SMTP_CHECK_SSL_HOSTNAME = False
else:
    SMTP_CHECK_SSL_HOSTNAME = True

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/93.0.4577.42 Safari/537.36'
}

# Telegram bot options
# Proxy for telegram
TELEGRAM_PROXIES = {}
# TELEGRAM_PROXIES = {
#     'http': 'socks5://127.0.0.1:9150',
#     'https': 'socks5://127.0.0.1:9150',
# }

# Get help from https://core.telegram.org/bots
# token that can be generated talking with @BotFather on telegram
TELEGRAM_TOKEN = '<INSERT YOUR TOKEN>'

# channel id for telegram
TELEGRAM_CHAT_ID = '<INSERT YOUR CHANNEL ID>'

# url for post request to api.telegram.org
TELEGRAM_URL = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/"


class MyParser(argparse.ArgumentParser):
    """
    Overriding the argparse.ArgumentParser class to catch parameter
    setting errors in the command line interface (CLI)
    """

    def error(self, message):
        """
        Overridden error handler
        :param message: str
        :return: None
        """
        sys.stderr.write(f'{FLR}error: {FRC}{message}\n\n')
        self.print_help()
        sys.exit(2)


def process_cli():
    """
    parses the CLI arguments
    :return: dict
    """
    parser = MyParser(
        formatter_class=argparse.RawTextHelpFormatter,
        conflict_handler='resolve',
        description=(
            f"{FLBC}SSL Host Expiration Checker\n"
            f"A simple python script to display or notify a user by email and/or via Telegram\n"
            f"about the status of the SSL certificates expiration date of the host."
        ),
        usage=f"{FLB}%(prog)s{FR} [Options]",
        epilog=f"{FLBC}(c) AK545 (Andrey Klimov) 2021, e-mail: ak545 at mail dot ru",
        add_help=False
    )
    parent_group = parser.add_argument_group(
        title=f"{FLBC}Options"
    )
    parent_group.add_argument(
        "-h",
        "--help",
        action="help",
        help=f"{FLBC}Help"
    )
    parent_group.add_argument(
        "-v",
        "--version",
        action="version",
        help=f"{FLBC}Display the version number",
        version="%(prog)s version: {}".format(__version__)
    )
    parent_group.add_argument(
        "-f",
        "--file",
        help=f"{FLBC}Path to the file with the list of hosts (default is None)\n"
             f"Sample:\n"
             f"\tMyHosts.txt",
        metavar="FILE"
    )
    parent_group.add_argument(
        "-o",
        "--host",
        help=f"{FLBC}Host to check the expiration date of the ssl "
             f"certificate (default is None)\n"
             f"Sample:\n"
             f"\tgoogle.com",
        metavar="STRING"
    )
    parent_group.add_argument(
        "-c",
        "--print-to-console",
        action="store_true",
        default=False,
        help=f"{FLBC}Enable console printing (default is False)"
    )
    parent_group.add_argument(
        "-dw",
        "--days-to-warn",
        default=7,
        type=int,
        metavar="DAYS",
        help=f"{FLBC}Warn me when there are less than DAYS days left (default is 7)"
    )
    parent_group.add_argument(
        "-t",
        "--use-telegram",
        action="store_true",
        default=False,
        help=f"{FLBC}Send a warning message through the Telegram (default is False)"
    )
    parent_group.add_argument(
        "-p",
        "--proxy",
        help=f"{FLBC}Proxy link (for Telegram only, default is None)\n"
             f"Sample (for example, when the Tor browser is running):\n"
             f"\tsocks5://127.0.0.1:9150",
        metavar="URL"
    )
    parent_group.add_argument(
        "-e",
        "--email-to",
        help=f'{FLBC}Send a warning message to email address (default is None)\n'
             f'Sample:\n'
             f'\temail@mail.dot\n'
             f'Or multiple address (the addresses are separated by commas,\n'
             f'and the entire string is enclosed in double quotes):\n'
             f'\t"email1@mail.dot, email2@mail.dot, email3@mail.dot"',
        metavar="EMAIL or EMAIL'S"
    )
    parent_group.add_argument(
        "-subject",
        "--email-subject",
        help=f"{FLBC}Append custom text to the email subject (default is None)",
        metavar="STRING"
    )
    parent_group.add_argument(
        "-ssl",
        "--email-ssl",
        action="store_true",
        default=False,
        help=f"{FLBC}Send email via SSL (default is False)"
    )
    parent_group.add_argument(
        "-auth",
        "--email-auth",
        action="store_true",
        default=False,
        help=f"{FLBC}Send email via authenticated SMTP (default is False)"
    )
    parent_group.add_argument(
        "-starttls",
        "--email-starttls",
        action="store_true",
        default=False,
        help=f"{FLBC}Send email via STARTTLS (default is False)"
    )
    parent_group.add_argument(
        "-nb",
        "--no-banner",
        action="store_true",
        default=False,
        help=f"{FLBC}Do not print banner (default is False)"
    )
    return parser


def print_cli() -> None:
    """
    Print preset options to console
    :return: None
    """
    print(
        f"{FLBC}"
        f"\tPreset options\n"
        f"\t-------------------------\n"
        f"\tFile                     : {CLI.file}\n"
        f"\tHost                     : {CLI.host}\n"
        f"\tPrint to console         : {CLI.print_to_console}\n"
        f"\tDays to warn             : {CLI.days_to_warn}\n"
        f"\tUse Telegram             : {CLI.use_telegram}\n"
        f"\tProxy for Telegram       : {CLI.proxy}\n"
        f"\tEmail to                 : {CLI.email_to}\n"
        f"\tEmail subject            : {CLI.email_subject}\n" 
        f"\tEmail SSL                : {CLI.email_ssl}\n"
        f"\tEmail AUTH               : {CLI.email_auth}\n" 
        f"\tEmail STARTTLS           : {CLI.email_starttls}\n"
        f"\tPrint banner             : {CLI.no_banner}\n"
        f"\t-------------------------"
    )


def prepaire_host_list(file: str) -> List[str]:
    """
    Prepare Host List from file
    :param file: str
    :return: List
    """
    host_list = []

    with open(file, "r", encoding="utf-8", newline="\n") as hosts_to_process:
        for line in hosts_to_process:
            try:
                ss = line.strip()
                if len(ss) == 0:
                    continue
                else:
                    if len(ss) > 0:
                        host_list.append(ss)
            except Exception as e:
                err = (
                    f"Unable to parse the file with the list of hosts.\n"
                    f"Problem line\n"
                    f"\"{line.strip()}\"\n"
                    f"Error: {str(e)}"
                )
                print(f"{FLR}{err}")
                # sys.exit(1)
    return host_list


def check_cli_logic() -> None:
    """
    Check command line logic
    :return: None
    """
    global CLI
    global TELEGRAM_PROXIES

    if CLI.print_to_console and not CLI.no_banner:
        # Print banner
        if platform.platform().startswith('Windows'):
            home_path = os.path.join(os.getenv('HOMEDRIVE'),
                                     os.getenv('HOMEPATH'))
        else:
            home_path = os.path.join(os.getenv('HOME'))
        sv = str(sys.version).replace('\n', ' ')
        print(
            f"{FLBC}\tPython  : {FLC}{sv}{FLBC}\n"
            f"\tNode    : {FLC}{platform.node()}{FLBC}\n"
            f"\tHome    : {FLC}{home_path}{FLBC}\n"
            f"\tOS      : {FLC}{platform.system()}{FLBC}\n"
            f"\tRelease : {FLC}{platform.release()}{FLBC}\n"
            f"\tVersion : {FLC}{platform.version()}{FLBC}\n"
            f"\tArch    : {FLC}{platform.machine()}{FLBC}\n"
            f"\tCPU     : {FLC}{platform.processor()}{FLBC}"
        )
        print_cli()

    if (not CLI.print_to_console and (CLI.file or CLI.host)) and (
            (not CLI.use_telegram) and (not CLI.email_to)):
        print(
            f"{FLR}You must use at least one of the notification methods "
            f"(email, telegram or console)\n"
            f"Use --print-to-console or --email-to or/and --use-telegram"
        )
        sys.exit(-1)

    if CLI.email_ssl and (not CLI.email_to):
        print(
            f"{FLR}You must specify the email address of the recipient. Use the --email-to option")
        sys.exit(-1)

    if CLI.email_subject and (not CLI.email_to):
        print(
            f"{FLR}You must specify the email address of the recipient. Use the --email-to option")
        sys.exit(-1)

    if CLI.email_auth and (not CLI.email_to):
        print(
            f"{FLR}You must specify the email address of the recipient. Use the --email-to option")
        sys.exit(-1)

    if CLI.email_starttls and (not CLI.email_to):
        print(
            f"{FLR}You must specify the email address of the recipient. Use the --email-to option")
        sys.exit(-1)

    if CLI.email_starttls and CLI.email_ssl and CLI.email_to:
        print(f"{FLR}The contradiction of options. You must choose one thing: either --email-ssl or "
              f"--email-starttls or do not use either one or the other")
        sys.exit(-1)

    if CLI.file and CLI.host:
        print(
            f"{FLR}One of the parameters is superfluous. Use either --file or --host")
        sys.exit(-1)

    if CLI.proxy and (not CLI.use_telegram):
        print(f"{FLR}The proxy setting is for telegram only")
        sys.exit(-1)

    if CLI.proxy and CLI.use_telegram:
        TELEGRAM_PROXIES.clear()
        TELEGRAM_PROXIES['http'] = CLI.proxy
        TELEGRAM_PROXIES['https'] = CLI.proxy


def send_expires_telegram(expires_hosts: List[str]) -> any:
    """
    Sending a message through the Telegram bot.
    :param expires_hosts: List[str]
    :return: any
    """
    if len(expires_hosts) == 0:
        return None

    today = "{:%d.%m.%Y}".format(datetime.now())
    message = ""
    if len(expires_hosts) > 0:

        max_len_hostname = 0
        for host in expires_hosts:
            curr_len = len(host)
            max_len_hostname = curr_len if curr_len > max_len_hostname else max_len_hostname
        hl = '-' * (max_len_hostname + 6)

        # add expiring hosts
        message += f"\n<b>SSL certificates expiration date for hosts</b><pre>{today}\n"
        message += hl + "\n"
        for line in expires_hosts:
            host, day_left = line.split(';')
            s_host = host.lower().rjust(max_len_hostname + 2)
            s_days = str(day_left).ljust(4)
            str_host_item = f"{s_host} : {s_days}\n"

            message += str_host_item
        message += f"</pre>"

    if message != "":
        message += "\n"

    response = send_telegram(message)
    return response


def send_telegram(message: str) -> any:
    """
    Sending a message through the Telegram bot.
    :param message: str
    :return: any
    """
    params = {'chat_id': TELEGRAM_CHAT_ID, 'parse_mode': 'html', 'text': message}
    if len(TELEGRAM_PROXIES) > 0:
        response = requests.post(TELEGRAM_URL + 'sendMessage', data=params, proxies=TELEGRAM_PROXIES,
                                 headers=REQUEST_HEADERS)
    else:
        response = requests.post(TELEGRAM_URL + 'sendMessage', data=params,
                                 headers=REQUEST_HEADERS)
    return response


def send_expires_email(expires_hosts: List[str]) -> None:
    """
    Preparing the contents of an email to send.
    :return: None
    """
    if len(expires_hosts) == 0:
        return

    email_to_list = []
    if ',' in CLI.email_to:
        tmp_list = CLI.email_to.split(',')
        for email in tmp_list:
            s_email = email.strip()
            if s_email != '':
                email_to_list.append(s_email)
    else:
        email_to_list = [CLI.email_to]

    for email_to in email_to_list:

        msg = MIMEMultipart("alternative")
        msg['From'] = SMTP_SENDER
        msg['To'] = email_to

        subject = "SSL certificates expiration date for hosts"
        if CLI.email_subject:
            subject = subject + ": " + CLI.email_subject
        msg['Subject'] = subject

        body_text = "SSL certificates expiration date for hosts\n%BODY%"
        body_html = """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <style type="text/css">
            table{
                font-family: monospace; 
                color:#fff;
                border-color: #0c64c9 !important; 
                background-color: #0c7bc9 !important; 
                padding: 50px; 
            }
        </style>        
        </head>
        <html>
          <body marginwidth="0" marginheight="0" leftmargin="0" topmargin="0" 
          style="
          font-family: monospace; 
          margin:0; 
          padding:0; 
          min-width: 100%; 
          -webkit-text-size-adjust:none; 
          -ms-text-size-adjust:none;">
          
            <div style="
            font-family: monospace;
            width: auto; 
            margin: 50px; 
            display: inline-block;
            ">
            %BODY%
            </div>
            
          </body>
        </html>
        """

        today = "{:%d.%m.%Y}".format(datetime.now())

        # For part plain
        host_list_txt = ""

        max_len_hostname = 0
        for host in expires_hosts:
            curr_len = len(host)
            max_len_hostname = curr_len if curr_len > max_len_hostname else max_len_hostname
        hl = '-' * (max_len_hostname + 6)

        if len(expires_hosts) > 0:
            # add expiring hosts
            host_list_txt += "\nSSL certificates expiration date for hosts\n"
            host_list_txt += f'Check date: {today}\n'
            host_list_txt += f'{hl}\n'
            for line in expires_hosts:
                host, day_left = line.split(';')
                s_host = host.lower().rjust(max_len_hostname + 2)
                s_days = str(day_left).ljust(4)
                str_host_item = f"{s_host} : {s_days}\n"
                host_list_txt += str_host_item
            host_list_txt += "\n"
        body_text = body_text.replace("%BODY%", host_list_txt)

        # For part html
        host_list = ""
        if len(expires_hosts) > 0:
            # add expiring hosts
            host_list += "<br>\n<b>SSL certificates expiration date for hosts</b><br>\n<pre>"
            host_list += f'Check date: {today}\n'
            host_list += f'{hl}\n'
            host_list += f'<table>\n'
            for line in expires_hosts:
                host, day_left = line.split(';')
                s_host = host.lower()
                s_host = f'<a href="https://{s_host}" style="color:#fff; text-decoration:none">{s_host}</a>'
                s_days = str(day_left)
                str_host_item = f"<tr><td>{s_host}</td><td>{s_days}</td></tr>\n"
                host_list += str_host_item
            host_list += f'</table>\n'
            host_list += f"</pre>"
        body_html = body_html.replace("%BODY%", host_list)

        part_plain = MIMEText(body_text, "plain")
        part_html = MIMEText(body_html, "html")

        msg.attach(part_plain)
        msg.attach(part_html)

        message = msg.as_string()
        send_email(email_to, message)


def send_email(email_to: str, message: str) -> None:
    """
    Sending a email to the recipient
    :param email_to: str
    :param message: str
    :return: None
    """
    server = None
    context = None
    # Try to log in to server and send email
    try:
        if CLI.email_ssl or CLI.email_starttls:
            # Create a secure SSL context
            context = ssl.create_default_context()
            context.check_hostname = SMTP_CHECK_SSL_HOSTNAME
            if CLI.email_ssl:
                server = smtplib.SMTP_SSL(
                    host=SMTP_SERVER,
                    port=SMTP_PORT,
                    context=context
                )
            context.verify_mode = ssl.CERT_REQUIRED

        if server is None:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        if CLI.email_starttls:
            server.starttls(context=context)  # Secure the connection

        server.ehlo()  # Can be omitted
        if CLI.email_auth:
            server.login(SMTP_SENDER, SMTP_PASSWORD)
        server.sendmail(SMTP_SENDER, email_to, message)
    except Exception as e:
        # Print any error messages to stdout
        print(f"{FLR}{e}")
    finally:
        server.quit()


def main() -> None:
    """
    Main function
    :return: None
    """
    check_cli_logic()
    hostname = []
    expires_hosts = []

    if CLI.file:
        # Source data from the file list of the hosts
        file = CLI.file.strip()
        if not Path(file).is_file():
            print(f"{FLR}File {FLY}{file}{FLR} not found")
            sys.exit(-1)

        # Prepaire hosts list
        hostname = prepaire_host_list(CLI.file)

    if CLI.host:
        # Source data as one host
        hostname = [CLI.host.strip()]

    if len(hostname) == 0:
        print(f"{FLR}There is nothing to process. At least one host is required")
        sys.exit(-1)

    max_len_hostname = 0
    for host in hostname:
        curr_len = len(host)
        max_len_hostname = curr_len if curr_len > max_len_hostname else max_len_hostname

    port = 443

    s_host = 'Hosts'.rjust(max_len_hostname + 8)
    s_days = 'Days left'.ljust(20)
    print(
        f"{FLBC}{s_host}",
        f"{FLBC}{s_days}",
    )

    s_host = '-'*(max_len_hostname + 8)
    s_days = '-'*20
    print(
        f"{FLBC}{s_host}",
        f"{FLBC}{s_days}",
    )

    for i, host in enumerate(hostname):
        first_line = '' if i == 0 else '\n'

        if '#' in host:
            s_host = host.replace('#', '').strip().rjust(max_len_hostname + 8)
            s_days = ' ' * 20
            print(
                f"{first_line}{FLG}{s_host}",
                f"{FLBC}{s_days}",
            )
            continue

        data = None
        try:
            context = ssl.create_default_context()
            with socket.create_connection(address=(host, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    data = ssock.getpeercert()
        except Exception as e:
            s_host = host.lower().rjust(max_len_hostname + 8)
            s_days = f'Error: {str(e)}'
            print(
                f"{FLR}{s_host}",
                f"{FRC}{s_days}",
            )
            continue

        if data is None:
            s_host = host.lower().rjust(max_len_hostname + 8)
            s_days = f'Error: ssock.getpeercert() return None'
            print(
                f"{FLR}{s_host}",
                f"{FRC}{s_days}",
            )
            continue
        else:
            dt_now = datetime.now()
            sdt = data.get('notAfter')
            dt = datetime.strptime(sdt, "%b %d %H:%M:%S %Y GMT")
            dt_delta = dt - dt_now

            is_expiried = dt_delta.days <= CLI.days_to_warn
            row_color = f'{FRC}' if is_expiried else f'{FLBC}'

            if is_expiried:
                expires_hosts.append(f'{host.lower()};{dt_delta.days}')

            s_host = host.lower().rjust(max_len_hostname + 8)
            s_days = str(dt_delta.days).ljust(20)
            print(
                f"{row_color}{s_host}",
                f"{row_color}{s_days}",
            )

    if len(expires_hosts) > 0:
        if CLI.use_telegram:
            res = send_expires_telegram(expires_hosts)
            if res:
                if res.status_code != 200:
                    print(f"{FLR}{res.text}")

        if CLI.email_to:
            send_expires_email(expires_hosts)
    print(f"{SR}")


if __name__ == "__main__":
    print(f"{SR}")

    # Parsing command line
    parser = process_cli()
    CLI = parser.parse_args(sys.argv[1:])
    main()

