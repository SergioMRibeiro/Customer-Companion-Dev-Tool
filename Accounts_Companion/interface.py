import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess
import re

current_path = os.getcwd()

file_path = os.path.join(current_path, 'Accounts_Companion', 'configs.json')

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def extrair_informacoes(string):
    rules = r"Logged into (\S+) as (\S+) at (\S+) workspace (\S+)"
    result = re.search(rules, string)
    if result:
        # Grupos capturados pelas expressões regulares
        vendor = result.group(1)
        email = result.group(2)
        ambient = result.group(3)
        workspace = result.group(4)
        
        # Retorna as informações capturadas
        return vendor, email, ambient, workspace
    else:
        return None

def on_button_click(vendor_name, store_name):
    messagebox.showinfo("Vendor Information", f"Vendor Name: {vendor_name}\nStore Name: {store_name}")

def test_function():
    try:
        saida1 = subprocess.check_output('vtex whoami', shell=True, stderr=subprocess.STDOUT)
        saida_decodificada1 = saida1.decode('utf-8')
        print(extrair_informacoes(saida_decodificada1))

        saida2 = subprocess.check_output('vtex ls', shell=True, stderr=subprocess.STDOUT)
        saida_decodificada2 = saida2.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Ocorreu um erro:", e.output.decode('utf-8'))
        

data = read_json(file_path)
vendors = data['vendor-collection']

def run_interface():
    # SECTION window config
    root = tk.Tk()
    root.title("Customer Companion Dev Tool")
    root.geometry("600x575")
    # !SECTION window config
    
    # SECTION Seletor de vendor
    for index, vendor in enumerate(vendors):
        vendor_name = vendor['vendor-name']
        store_name = vendor['store-name']
        
        button_text = f"{vendor_name}\n{store_name}"
        vendor_select_button = tk.Button(root, text=button_text, command=lambda vn=vendor_name, sn=store_name: on_button_click(vn, sn))
        vendor_select_button.place(x=10, y=10 + (index * 59), width=142, height=49)
    # !SECTION Seletor de vendor

    # SECTION Elementos de teste
    label = tk.Label(root, text="Bem-vindo à Ferramenta de Clientes!")
    label.place(x=10, y=10 + (len(vendors) * 59) + 20)  # Colocar o rótulo abaixo dos botões

    quitBtn = tk.Button(root, text="Fechar", command=root.quit)
    quitBtn.place(x=10, y=10 + (len(vendors) * 59) + 60)  # Colocar o botão "Fechar" abaixo do rótulo

    test_command = lambda: test_function()
    teste_btn = tk.Button(root, text="Teste algo aqui", command=test_command)
    teste_btn.place(x=10, y=10 + (len(vendors) * 59) + 100)
    # !SECTION Elementos de teste

    root.mainloop()

if __name__ == "__main__":
    run_interface()