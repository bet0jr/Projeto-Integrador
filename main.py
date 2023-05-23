import tkinter as tk
import time
from playwright.sync_api import sync_playwright

class App:
    def __init__(self):
        self.create_interface()

    def download_notes(self):
        cnpj = self.input_cnpj.get()
        password = self.input_password.get()
        date = self.input_date.get()
        print(date)
        formated_date = f'01/{date}'

        with sync_playwright() as p:

            # Cria o navegador
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Redirecionar para o site
            page.goto('https://nfse-ararangua.atende.net/')

            # Faz Login
            page.locator('xpath=/html/body/div[1]/div[2]/span[3]/input').fill(cnpj)
            page.locator('xpath=/html/body/div[1]/div[2]/span[5]/div/input').fill(password)
            page.locator('xpath=/html/body/div[1]/div[2]/span[6]/button').click()

            # Navega até a pagina das notas fiscais
            page.locator('xpath=/html/body/div[1]/div/div[1]/a[1]').click()
            time.sleep(5)
            page.goto('https://nfse-ararangua.atende.net/?rot=1&aca=1#!/sistema/66')
            page.bring_to_front()
            page.locator('xpath=//*[@id="estrutura_logo_menu"]').click()
            page.locator('xpath=//*[@id="estrutura_menu_conjuntos"]/ul/li[3]/div').click()
            page.locator('xpath=//*[@id="estrutura_menu_conjuntos"]/ul/li[3]/ul/li/div').click()
            page.locator('xpath=//*[@id="conteudo_66079_1063_1"]/div/span/fieldset/div/div/span[2]/article').click()
            page.locator('xpath=//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input').fill(formated_date)
            page.locator('xpath=//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[2]/span/div/div/table/tbody/tr[2]/td[1]/select').select_option(value='competencia')
            page.locator('xpath=//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[2]/span/div/div/table/tbody/tr[2]/td[3]/input').fill(date)
            page.locator('span[name="consultar"]').click()
            time.sleep(5)
            page.locator('xpath=//*[@id="conteudo_66020_101_1"]/article/div[1]/header/div[2]/table/tbody/tr[1]/td[1]/button').click()
            page.locator('xpath=//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[2]/div[2]/span[11]').click()
            page.locator('xpath=//*[@id="context_menu"]/table/tbody/tr[3]/td/span').click()
            page.locator('xpath=//*[@id="estrutura_container_sistema"]/div[4]/section/footer/button[1]').click()


    def format_date(self, event):
        date = self.input_date.get()
        
        if event.keysym.lower() == "backspace": return

        if len(date) == 2:
            date += '/'

        self.input_date.delete(0, 'end')
        self.input_date.insert(0, date)

    def format_cnpj(self, event):
        text = self.input_cnpj.get().replace(".", "").replace("-", "")[:15]
        new_text = ""

        if event.keysym.lower() == "backspace": return
        
        for index in range(len(text)):
            
            if not text[index] in "0123456789": continue
            if index in [1, 4]: new_text += text[index] + "."
            elif index == 7: new_text += text[index] + "/"
            elif index == 12: new_text += text[index] + "-"
            else: new_text += text[index]

        self.input_cnpj.delete(0, "end")
        self.input_cnpj.insert(0, new_text)

    def on_click_date(self, event):
        if self.input_date.get() == 'mm/aaaa':
            self.input_date.delete(0, 'end')

    def create_interface(self):
        window = tk.Tk()
        window.configure(bg='black')
        window.title("Download Notas Fiscais")
        window.geometry('800x600')
        window.resizable(0, 0)

        logo_path = tk.PhotoImage(file='images/logo.png')
        logo = tk.Label(window, image=logo_path, bg='black')
        logo.place(x=0, y=0)
        
        label_cnpj = tk.Label(window, text='CNPJ:', fg='white', bg='black')
        label_cnpj.place(x=475, y=150)

        self.input_cnpj = tk.Entry(window, bd=0)
        self.input_cnpj.place(x=475, y=175, width=170, height=25)
        self.input_cnpj.bind('<KeyRelease>', self.format_cnpj)

        label_password = tk.Label(window, text='Password:', fg='white', bg='black')
        label_password.place(x=475, y=210)

        self.input_password = tk.Entry(window, bd=0, show='*')
        self.input_password.place(x=475, y=235, width=170, height=25)

        label_date = tk.Label(window, text='Data:', fg='white', bg='black')
        label_date.place(x=475, y=270)

        self.input_date = tk.Entry(window)
        self.input_date.place(x=475, y=295, width=170, height=25)
        self.input_date.insert(0, 'mm/aaaa')
        self.input_date.bind('<KeyRelease>', self.format_date)
        self.input_date.bind('<Button-1>', self.on_click_date)

        button_execute = tk.Button(window, text='Fazer download', bg='gray', bd=0, command=self.download_notes)
        button_execute.place(x=475, y=350, width=170, height=25)
        window.mainloop()

app = App()