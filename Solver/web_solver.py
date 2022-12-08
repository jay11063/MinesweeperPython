# December 7, 2022
# Jaeyoon Lee

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import keyboard
from MinesweeperAI import MinesweeperAI


def input_all(ai:MinesweeperAI):
    for i in range(5):
        elements = browser.find_elements(By.CLASS_NAME, 'open'+str(i))
        elements = list(set(elements)-set(ai.inputs))
        for e in elements:
            pos = list(map(lambda x: int(x)-1, e.get_attribute('id').split('_')))
            pos.reverse()
            ai.input({tuple(pos):i})
            ai.inputs.append(e)


def pos_id(x,y):
    return str(y)+'_'+str(x)


def main():
    levels = ['beginner-','intermediate-','']
    browser.get(f'https://minesweeperonline.com/#{levels[2]}200')
    browser.maximize_window()
    time.sleep(1)

    while True:
        ai = MinesweeperAI(30,16,99)
        win = False
        browser.find_element(By.ID, pos_id(ai.start[0], ai.start[1])).click()
        input_all(ai)

        game = True
        while game:
            to_open, flaged = ai.next_move()
            for x,y in to_open:
                tile = browser.find_element(By.ID, pos_id(x+1,y+1))
                tile.click()
                try:
                    alert = browser.switch_to.alert
                    alert.accept()
                    alert.dismiss()
                except:
                    "popup : nothing"
                str_n = tile.get_attribute('class')[-1]
                if str_n in ['h','d','k']:
                    game = False
                    print("Lose")
                    break
                n = int(str_n)
                ai.input({(x,y):n})
                if n==0:
                    input_all(ai)
            # ai.show()

            if len(to_open)==0 and len(flaged)==0:
                print('ERROR')
                game = False
            elif ai.is_win():
                print('WIN2')
                game, win = False, True
        if win:
            actions.key_down(Keys.CONTROL).perform()
            for x,y in ai.flags:
                browser.find_element(By.XPATH, f'//*[@id="{pos_id(x+1,y+1)}"]').click()
                # actions.context_click(flag).perform()
            actions.key_up(Keys.CONTROL).perform()
        browser.find_element(By.ID, 'face').click()
        time.sleep(1)
        if keyboard.is_pressed("esc"):
            break

    time.sleep(1)
    browser.quit()


if __name__=="__main__":
    browser = webdriver.Chrome("C:\JaeyoonLee\python_workspace\chromedriver.exe")
    actions = ActionChains(browser)
    main()
