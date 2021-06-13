#do all the imports
import requests
import bs4
import tkinter as tk
import plyer
import time
import datetime
import threading

#get html data of website
def get_html_data(url) :
    data = requests.get(url)
    return data

#parsing html and extracting data
def get_corona_detail():
    url = "https://www.mygov.in/covid-19/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="information_row").find_all("div", class_="iblock_text")
    all_details = ""
    for block in info_div:
        count = (block.find("span", class_="icount").get_text())
        text = (block.find("div", class_="info_label").get_text())
        # print(text +": "+count)
        all_details = (((all_details + text + " : " + count))).replace(" ", "") + "\n"

    return (all_details)

#function used to refresh the data from the website0
def refresh() :
    new_data = get_corona_detail()
    print("Refreshing..")
    mainLabel['text'] = new_data

#function for notifying
def notify_me() :
    while True:
        plyer.notification.notify(
            title = "Covid-19 Cases in India",
            message = get_corona_detail(),
            timeout = 10,
        )
        time.sleep(180)

#creating gui :

root = tk.Tk()
root.geometry("900x800")
root.iconbitmap("img.png")
root.title("Covid-19 Data Tracker")
root.configure(background = 'white')
f = ("poppins",25,"bold")



mainLabel = tk.Label(root,text = get_corona_detail(),font = f, bg = 'white')
mainLabel.pack()

reBtn = tk.Button(root, text = "Refresh", font =f, relief = 'solid', command = refresh)
reBtn.pack()

#create new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()

root.mainloop()