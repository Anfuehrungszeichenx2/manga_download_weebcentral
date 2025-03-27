import os.path
import urllib.request
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

wurzel_ordner = ''


def speichere_kapitel(seiten, kapitel_name):
    aktueller_ordner = wurzel_ordner + '/' + kapitel_name
    if not os.path.isdir(aktueller_ordner):
        os.makedirs(aktueller_ordner)
    else:
        return
    with open(f'{aktueller_ordner}/{len(seiten)}-seiten.txt', 'w') as outfile:
        outfile.write('\n'.join(i for i in seiten))
    for index, seite in enumerate(seiten):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        request = urllib.request.Request(seite, headers=headers)
        if 'png' in seite:
            filename = f'{aktueller_ordner}/{index+1}.png'
        elif 'jpg' in seite:
            filename = f'{aktueller_ordner}/{index+1}.jpg'
        with urllib.request.urlopen(request) as response:
            with open(filename, 'wb') as out_file:
                while True:
                    try:
                        out_file.write(response.read())
                    except Exception as e:
                        print("Irgendwas ist schief gelaufen")
                        print(e)
                        continue
                    break


def bekomme_kapitel(link, driver):
    driver.switch_to.new_window('tab')
    driver.get(link)
    name = driver.find_element('css selector',
                               '#nav-top > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > span:nth-child(2)').text
    pages = driver.find_elements('css selector', 'section.flex-1 > img')
    imgs = [page.get_attribute('src') for page in pages]
    sleep(5)
    print(imgs)
    speichere_kapitel(imgs, name)
    driver.close()


def haupt():
    global wurzel_ordner
    wurzel_ordner = 'I:\manga2'
    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://weebcentral.com/chapters/01J76XYYSBC50VG9PV4RK9KMY9")
    print("Headless Firefox Initialized")
    anime_name = driver.find_element('css selector',
                                     '#nav-top > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text
    wurzel_ordner = f'{wurzel_ordner}/{anime_name}'
    if not os.path.isdir(wurzel_ordner):
        os.makedirs(wurzel_ordner)
    chapter_button = driver.find_elements("xpath", "/html/body/main/section[1]/div/div[1]/button[1]")
    chapter_button[0].click()
    driver.implicitly_wait(3)
    chapters = driver.find_elements("css selector", ".grid-cols-2 > a")
    names = [chapter.text for chapter in chapters]
    links = [chapter.get_attribute('href') for chapter in chapters]
    for link in links:
        driver.switch_to.window(driver.window_handles[0])
        bekomme_kapitel(link, driver)
    sleep(10)
    driver.quit()


if __name__ == '__main__':
    haupt()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
