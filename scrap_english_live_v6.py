# scraping_script.py

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tela_login import Ui_Dialog  # Importa a classe da tela de login
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QProgressDialog


# Obtém o email e a senha via PyQt5
def show_login():
    app = QtWidgets.QApplication([])  # Cria a aplicação PyQt5
    ui = Ui_Dialog()
    email_usuario, senha_usuario = ui.show_login()  # Chama a tela de login
    return email_usuario, senha_usuario

# 🔹 Obtém email e senha do usuário via PyQt5
email_usuario, senha_usuario = show_login()

# 🔹 Configuração do WebDriver
# 🔹 Configuração das opções do Chrome
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
# options.add_argument("--headless")  # Roda o Chrome sem a interface gráfica


# 🔹 Inicializa o WebDriver com as opções
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 25)

# 🔹 URL da página de login
url = "https://school.englishlive.ef.com/campus/mypage/home"
driver.get(url)

# 🔹 Preenche os campos de login
email = wait.until(EC.presence_of_element_located((By.ID, "signInName")))
senha = driver.find_element(By.ID, "signInPassword")

email.send_keys(email_usuario)
senha.send_keys(senha_usuario)

# 🔹 Clica no botão de login
botao_login = driver.find_element(By.ID, "next")
botao_login.click()

# 🔹 Aguarda o redirecionamento após login
wait.until(EC.url_changes(url))

# 🔹 Aguarda o carregamento do elemento <li>
li_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-code="Main.Course.2012"]')))
link_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.ue-menu-link')))
# link_element = li_element.find_element(By.CSS_SELECTOR, 'a.ue-menu-link')

# 🔹 Cria um hover sobre o menu
actions = ActionChains(driver)
actions.move_to_element(link_element).perform()

# 🔹 Aguarda e clica no link da tabela de progresso
td_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.ue-td.first-child.last-child[data-code="School.Progress.2012"]')))
link_element = td_element.find_element(By.TAG_NAME, 'a')
link_element.click()

# 🔹 Abre a página desejada
url_destino = "https://school.englishlive.ef.com/school/progressreport?icid=School.Progress.2012#teacher-feedback"
driver.get(url_destino)

time.sleep(10)

# 🔹 Obtém número da última página

last_page_element = driver.find_elements(By.CSS_SELECTOR, ".section.end a.num") 
last_page_number = int(last_page_element[0].text) if last_page_element else 1

# 🔹 Obtém a página atual
# active_page_element = driver.find_element(By.CSS_SELECTOR, ".num.active")
## Espera até que o elemento com a classe "num active" esteja visível
active_page_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".num.active")))
current_page = int(active_page_element.text)

# variável para armazenar os dados
dados_extraidos = []

# Cria a barra de progresso
app = QtWidgets.QApplication([])
progress = QProgressDialog("Extraindo dados...", "Cancelar", 0, last_page_number)
progress.setWindowTitle("Progresso da Extração")
progress.resize(500, 100)  # Largura 500 pixels, altura 100 pixels
progress.setWindowModality(QtCore.Qt.ApplicationModal) # Impede interação com outras janelas
progress.show()

while current_page <= last_page_number:
    time.sleep(2)

    # Aguarda até que todos os elementos estejam carregados antes de capturá-los
    # data_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.ets-pr-fb-date")))
    # title_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.ets-pr-fb-summary .ets-pr-fb-title")))
    # type_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.ets-pr-fb-type")))
    # scores_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[contains(@class, 'ets-pr-fb-score') and contains(@class, 'ets-pr-fb-passed')]/span")))
    # teacher_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ets-pr-fb-teacher")))

    # YOU CAN ALSO DO IN THIS WAY
    data_elements = driver.find_elements(By.CSS_SELECTOR, "td.ets-pr-fb-date")
    title_elements = driver.find_elements(By.CSS_SELECTOR, "td.ets-pr-fb-summary .ets-pr-fb-title")
    type_elements = driver.find_elements(By.CSS_SELECTOR, "td.ets-pr-fb-type")
    # scores_elements = driver.find_elements(By.XPATH, "//td[contains(@class, 'ets-pr-fb-score') and (contains(@class, 'ets-pr-fb-passed') or contains(@class, 'ets-pr-fb-not-passed'))]/span")
    scores_elements = driver.find_elements(By.CSS_SELECTOR, "td.ets-pr-fb-score")
    teacher_elements = driver.find_elements(By.CSS_SELECTOR, "span.ets-pr-fb-teacher")

    # Extrai os dados
    for data, titulo, tipo, nota, teacher in zip(data_elements, title_elements, type_elements, scores_elements, teacher_elements):
        dados_extraidos.append({
            "Date": data.text.replace("NEW", "").strip(),
            "Title": titulo.text,
            "Type": tipo.text,
            "Score": nota.text,
            "Teacher": teacher.text
        })

    progress.setValue(current_page) # Atualiza a barra de progresso

    if progress.wasCanceled():
        print("Extração cancelada pelo usuário.")
        break

    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.section.next a.next.icon-angle-right")))
        next_button.click()
        time.sleep(2)
    except:
        print("Última página alcançada. Encerrando navegação.")
        break

    current_page += 1

progress.close() # Fecha a barra de progresso

# 🔹 Salva os dados extraídos em CSV
# 🔹 Garante que todas as listas tenham o mesmo tamanho
# 🔹 Salva os dados extraídos em CSV
with open("ef_data.csv", mode="w", newline="", encoding="utf-8") as arquivo_csv:
    campo_nomes = ["Date", "Title", "Type", "Score", "Teacher"]
    writer = csv.DictWriter(arquivo_csv, fieldnames=campo_nomes)
    writer.writeheader()
    writer.writerows(dados_extraidos)


# 🔹 Fecha o navegador
driver.quit()