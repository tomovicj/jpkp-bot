from bs4 import BeautifulSoup
import requests
import datetime
import time



key = ""    #Telegram bot private key
chat_id = ""    #Telegram chat id

debuging = False


if debuging == False:
    with open("last.txt", "w") as f:
        now = datetime.datetime.now()
        current = now.strftime("%d-%m-%Y %H:%M")
        f.write(current)

def sendNotification(text):
    response = requests.get(f"https://api.telegram.org/bot{key}/sendMessage?chat_id={chat_id}&text={text}")
    
    if response.status_code == 200:
        print("poruka poslata!")
    else:
        print("Greska pri GET REQUESTU kod slanja poruke!")


def checkDate(date):
    with open("last.txt", "r") as f:
        last = f.read()
    date_time = date.split(" ")
    date = date_time[0].split("-")
    time = date_time[1].split(":")
    last_date_time = last.split(" ")
    last_date = last_date_time[0].split("-")
    last_time = last_date_time[1].split(":")

    d1 = datetime.datetime(int(last_date[2]), int(last_date[1]), int(last_date[0]), int(last_time[0]), int(last_time[1]))
    d2 = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
    d = d1 < d2

    if d == True:
        with open("last.txt", "w") as f:
            f.write(f"{date[0]}-{date[1]}-{date[2]} {time[0]}:{time[1]}")
    return d


def main():
    page = requests.get("http://www.jpkp.rs/")


    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find(id="ctl00_ContentPlaceHolder1_grid_vesti")
    rows = table.find_all("tr")

    for row in reversed(rows):  #It uses reversed to check from oldest entry to newest entry so it can sand multiple messages insted of only the latest one
        
        obavestenje = row.find_all("span", string="ОБАВЕШТЕЊЕ")


        if len(obavestenje) > 0:

            date = row.find("font", size="2").text
            
            if checkDate(date) == True:

                textDiv = row.find("div", class_="div_sadrzaj_vesti_prosiri")
                try:
                    text = (textDiv.text.strip())
                except: pass
            
                sendNotification(text)

            # else:
            #     print("nema novih obavestenja")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(900)