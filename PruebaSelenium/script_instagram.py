import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

service = Service('Drivers/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get('https://www.instagram.com')
time.sleep(5)
username_box = driver.find_element(By.NAME, 'username')
username_box.send_keys('danielreyes_952025')
time.sleep(2)
password_box = driver.find_element(By.NAME, 'password')
password_box.send_keys('123456ABC')
time.sleep(2)
password_box.send_keys(Keys.ENTER)
time.sleep(10)
search_btn = driver.find_element(By.XPATH, '(//div[@class="x1n2onr6"])[3]')
search_btn.click()
paginas = ["@elcorteingles", "@mercadona", "@carrefoures"]
resultados = {}
for pagina in paginas:
    time.sleep(5)
    input_search = driver.find_element(By.CSS_SELECTOR, ".x1lugfcp.x1hmx34t.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x5n08af.xl565be.x5yr21d.x1a2a7pz.xyqdw3p.x1pi30zi.xg8j3zb.x1swvt13.x1yc453h.xh8yej3.xhtitgo.xs3hnx8.x1dbmdqj.xoy4bel.x7xwk5j")
    input_search.send_keys(pagina)
    time.sleep(5)
    opcion_pagina = driver.find_element(By.CSS_SELECTOR, '.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3')
    opcion_pagina.click()
    time.sleep(5)
    followers = driver.find_element(By.CSS_SELECTOR, '.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd')
    followers.click()
    time.sleep(5)
    
    seguidores_modal = driver.find_element(By.CSS_SELECTOR, 'div.xyi19xy.x1ccrb07.xtf3nb5.x1pc53ja.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6 > div > div')
    print
    action_chain = ActionChains(driver)

    for _ in range(10):
        action_chain.move_to_element(seguidores_modal).click().send_keys(Keys.END).perform()
        time.sleep(2)
    
    seguidores_nombres = []
    seguidor_items = seguidores_modal.find_elements(By.CSS_SELECTOR, '.x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3')
    print(seguidor_items)
    
    for item in seguidor_items:
        try:
            username_elem = item.find_element(By.XPATH, './/div/div/div/div[2]/div/div/div/div/span/div/a/div/div/span')
            username = username_elem.text.strip()
            
            nombre_elem = item.find_element(By.XPATH, './/div/div/div/div[2]/div/div/span/span')
            try:
                nombre = nombre_elem.text.strip()
            except:
                nombre = ""
            
            if username and nombre and username.lower() != "seguir":
                seguidores_nombres.append({
                    "usuario": username,
                    "nombre": nombre
                })

            if len(seguidores_nombres) >= 50:
                break
        except Exception:
            continue

    resultados[pagina] = seguidores_nombres

    close_button = driver.find_element(By.CLASS_NAME, "_abl-")
    close_button.click()
    time.sleep(3)
    
    search_btn_s = driver.find_element(By.XPATH, '(//div[@class="x1n2onr6"])[4]')
    search_btn_s.click()
    time.sleep(5)

rows = []
for pagina, seguidores in resultados.items():
    for seguidor in seguidores:
        rows.append({
            "cuenta_consultada": pagina,
            "usuario": seguidor["usuario"],
            "nombre": seguidor["nombre"]
        })

df = pd.DataFrame(rows)
df.to_excel('seguidores_instagram.xlsx', index=False)
print("Datos guardados en 'seguidores_instagram.xlsx'")
driver.quit()