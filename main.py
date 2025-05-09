import requests
from bs4 import BeautifulSoup as bs
import re
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

r = requests.get(url="https://www.bvk.rs/planirani-radovi/")

text = r.text

soup = bs(text, 'html.parser')

#Pronalazenje svih obavestenja
all_paragraphs = soup.find_all("p")
all_notifs = []
all_opstina = []
for par in all_paragraphs:
    if par.get_text()[0].isdigit():
        print(f"{par.get_text()}")
        all_notifs.append(par.get_text())
        all_opstina.append(all_notifs[-1].split(" ")[-2] + " " + all_notifs[-1].split(" ")[-1])

for i in range(len(all_opstina)):
    opstina = all_opstina[i].split(" ")
    if opstina[0] == 'општина' or opstina[0] == 'општини':
        all_opstina[i] = opstina[1]
print(all_opstina)

#Unosenje opstina za koju zelimo da nam stizu obavestenja kada budu bili radovi

s = input("Unesite imena opstina za koje zelite da vam stizu obavestenja, odvojeno zarezima, na cirilici-->")

opstine = s.strip().split(",")

for i in range(len(opstine)):
    opstine[i] = opstine[i].strip()

print(opstine)

msg_list = ""
for i in range(len(opstine)):
    try:
        ind = all_opstina.index(opstine[i])
        msg_list += '<p>' + all_notifs[ind] + '</p>'
    except ValueError:
        print(ValueError())

print(msg_list)


mail = input("Unesite mejl na koji zelite da vam stizu notifikacije-->")

def send_mail(message_text):
    smtp_server = "smtp.gmail.com"
    port = 587 #for starttls
    sender_email = "vodovodnotifier"
    password = "sswz nohb wnrl pdth"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Vodovod - obavestenje"
    message["From"] = sender_email
    message["To"] = mail

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

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html1, "html")

    message.attach(part1)
    message.attach(part2)

    with SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(from_addr=sender_email, to_addrs=mail, msg=message.as_string())
if msg_list:
    send_mail(msg_list)


#na svakih 24 sata se proverava da li je doslo do promena
while True:
    time.sleep(60 * 60 * 24)
    # Pronalazenje svih obavestenja
    new_paragraphs = soup.find_all("p")
    new_notifs = []
    new_opstina = []
    for par in new_paragraphs:
        if par.get_text()[0].isdigit():
            print(f"{par.get_text()}")
            new_notifs.append(par.get_text())
            new_opstina.append(new_notifs[-1].split(" ")[-2] + " " + new_notifs[-1].split(" ")[-1])

    for i in range(len(new_opstina)):
        opstina = new_opstina[i].split(" ")
        if opstina[0] == 'општина' or opstina[0] == 'општини':
            new_opstina[i] = opstina[1]
    print(new_opstina)

    msg_list = ""

    for i in range(len(opstine)):
        ind1, ind2 = -1, -1
        for j in range(len(all_opstina)):
            if all_opstina[j] == opstine[i]:
                ind1 = j
                break
        for j in range(len(new_opstina)):
            if new_opstina[j] == opstine[i]:
                ind2 = j
                break

        #Da li postoje nove notifikacije za opstine za koje se korisnik prijavio
        if ind2 != -1 and ind1 == -1:
            msg_list += '<p>' + new_notifs[ind2] + '</p>'
        #Provera da li se razlikuju notifikacije za opstine za koje se korisnik prijavio
        elif all_notifs[ind1] != new_notifs[ind2]:
            msg_list += '<p>' + new_notifs[ind2] + '</p>'

    if msg_list:
        send_mail(msg_list)
    else:
        print("Nema novih obavestenja za vase opstine")
