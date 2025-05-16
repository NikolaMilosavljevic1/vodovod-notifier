import requests
from bs4 import BeautifulSoup as bs
import re
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from apscheduler.schedulers.background import BackgroundScheduler

r = requests.get(url="https://www.bvk.rs/planirani-radovi/")
text = r.text
soup = bs(text, 'html.parser')

all_notifs = []
all_opstina = []
all_paragraphs = soup.find_all("p")

for par in all_paragraphs:
    if par.get_text()[0].isdigit():
        print(f"{par.get_text()}")
        all_notifs.append(par.get_text())
        fnd = 0
        notif = all_notifs[-1].split(" ")
        for i in range(len(notif)):
            if notif[i][0:6] == 'општин':
                fnd = i+1
                break
        if fnd:
            all_opstina.append(notif[fnd:])
            all_opstina[-1] = " ".join(all_opstina[-1])

for i in range(len(all_opstina)):
    opstina = all_opstina[i].split(",")
    for j in range(len(opstina)):
        opstine_sa_i = opstina[j].split(" и ")
        opstina = opstine_sa_i
    print(opstina)
    all_opstina[i] = opstina

print(all_opstina)


#Unosenje opstina za koju zelimo da nam stizu obavestenja kada budu bili radovi

s = input("Unesite imena opstina za koje zelite da Vam stizu obavestenja, odvojeno zarezima, na cirilici-->")

opstine = s.strip().split(",")


for i in range(len(opstine)):
    opstine[i] = opstine[i].strip()

print(opstine)

ulice_za_opstine = []
for i in range(len(opstine)):
    s = input(f"Unesite imena ulica ili naselja za koje zelite da Vam stizu obavestenja za opstinu {opstine[i]}:")
    ulice = s.strip().split(",")
    for j in range(len(ulice)):
        ulice[j] = ulice[j].strip()
    ulice_za_opstine.append(ulice)

print(ulice_za_opstine)

msg_list = []
seen = []
for i in range(len(opstine)):
    for j in range(len(all_opstina)):
        for opstina in all_opstina[j]:
            if opstina == opstine[i]:
                info = soup.find("div", {"id": f"toggle-id-{j + 1}"}).text
                naziv_opstine = info.split('\n')[0]
                sve_ostalo = '<br>'.join([line.strip() for line in info.split('\n')[1:] if line.strip() != ""])
                if j in seen:
                    continue
                else:
                    seen.append(j)
                    msg_list.append(
                        f"<br><p><strong style='color: red'>{naziv_opstine}</strong><br>{sve_ostalo}</p>\n"
                    )

#print('\n'.join(msg_list))
seen = []
for ulice in ulice_za_opstine:
    for ulica in ulice:
        for i in range(len(msg_list)):
            if msg_list[i].find(ulica) != -1:
                if i not in seen: seen.append(i)
                pattern = re.escape(ulica)
                formatted_msg = msg_list[i]
                formatted_msg = re.sub(
                    pattern,
                    f"<span style='color: blue'>{ulica}</span>",
                    formatted_msg
                )
                pattern = re.escape("*Уколико имате проблема са водоснабдевањем, а не налазите се у зони извођења планираних радова, проверите да ли се ваша улица налази на списку кварова:<br>Кварови на водоводној мрежи >>")
                formatted_msg = re.sub(
                    pattern,
                    "",
                    formatted_msg
                )
                msg_list[i] = formatted_msg



msg_list_str = ""
for i in seen:
    msg_list_str += msg_list[i]

print(msg_list_str)


mail = input("Unesite mejl na koji zelite da vam stizu notifikacije-->")

def send_mail(message_text, recipient_mail):
    smtp_server = "smtp.gmail.com"
    port = 587 #for starttls
    sender_email = "vodovodnotifier"
    password = "sswz nohb wnrl pdth"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Vodovod - obavestenje"
    message["From"] = sender_email
    message["To"] = recipient_mail

    text = """\
    Postovani,

    Obavestenja vezana za radove mozete pronaci na sledecem linku:
    https://www.bvk.rs/planirani-radovi/
    """

    html1 = f"""\
        <html>
            <body>
                <p>Postovani,<br><br>
                    ispod su nova obavestenja vezanih za radove za opstine koje ste izabrali:
                    <br>
                    {message_text}
                    <br>
                    Za vise informacija, kliknite
                    <a href="https://www.bvk.rs/planirani-radovi/">ovde</a>.
                </p>
            </body>
        </html>
        """

    part1 = MIMEText(text, "plain", "utf-8")
    part2 = MIMEText(html1, "html", "utf-8")

    message.attach(part1)
    message.attach(part2)

    with SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(from_addr=sender_email, to_addrs=mail, msg=message.as_string())
if msg_list_str:
    send_mail(msg_list_str, mail)


def check_every_24_hours():
    r = requests.get(url="https://www.bvk.rs/planirani-radovi/")
    text = r.text
    soup = bs(text, 'html.parser')

    new_paragraphs = soup.find_all("p")
    new_notifs = []
    new_opstina = []
    for par in new_paragraphs:
        if par.get_text()[0].isdigit():
            print(f"{par.get_text()}")
            new_notifs.append(par.get_text())
            fnd = 0
            notif = new_notifs[-1].split(" ")
            for i in range(len(notif)):
                if notif[i][0:6] == 'општин':
                    fnd = i + 1
                    break
            if fnd:
                new_opstina.append(notif[fnd:])
                new_opstina[-1] = " ".join(new_opstina[-1])

    for i in range(len(new_opstina)):
        opstina = new_opstina[i].split(",")
        for j in range(len(opstina)):
            opstine_sa_i = opstina[j].split(" и ")
            opstina = opstine_sa_i
        print(opstina)
        new_opstina[i] = opstina

    new_msg_list = []
    new_seen = []
    for i in range(len(opstine)):
        for j in range(len(new_opstina)):
            for opstina in new_opstina[j]:
                if opstina == opstine[i]:
                    info = soup.find("div", {"id": f"toggle-id-{j + 1}"}).text
                    naziv_opstine = info.split('\n')[0]
                    sve_ostalo = '<br>'.join([line.strip() for line in info.split('\n')[1:] if line.strip() != ""])
                    if j in new_seen:
                        continue
                    else:
                        new_seen.append(j)
                        new_msg_list.append(
                            f"<br><p><strong style='color: red'>{naziv_opstine}</strong><br>{sve_ostalo}</p>\n"
                        )

    new_seen = []
    for ulice in ulice_za_opstine:
        for ulica in ulice:
            for i in range(len(new_msg_list)):
                if new_msg_list[i].find(ulica) != -1:
                    if i not in new_seen: new_seen.append(i)
                    pattern = re.escape(ulica)
                    formatted_msg = new_msg_list[i]
                    formatted_msg = re.sub(
                        pattern,
                        f"<span style='color: blue'>{ulica}</span>",
                        formatted_msg
                    )
                    pattern = re.escape(
                        "*Уколико имате проблема са водоснабдевањем, а не налазите се у зони извођења планираних радова, проверите да ли се ваша улица налази на списку кварова:<br>Кварови на водоводној мрежи >>")
                    formatted_msg = re.sub(
                        pattern,
                        "",
                        formatted_msg
                    )
                    new_msg_list[i] = formatted_msg
    new_msg_str = ""
    for i in new_seen:
        if new_msg_list[i] not in msg_list:
            new_msg_str += new_msg_list[i]

    if new_msg_str:
        send_mail(new_msg_str, mail)
    else:
        print("Nema novih obavestenja za vase opstine i ulice")


scheduler = BackgroundScheduler()
scheduler.add_job(check_every_24_hours, "interval", seconds=24*60*60)
scheduler.start()
