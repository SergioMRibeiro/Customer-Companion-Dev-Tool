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


def who_am_i_rules(string):
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
        print(who_am_i_rules(saida_decodificada1))

        saida2 = subprocess.check_output('vtex ls', shell=True, stderr=subprocess.STDOUT)
        saida_decodificada2 = saida2.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Ocorreu um erro:", e.output.decode('utf-8'))

def basic_info_pull():
    print("infomações básicas: blá blá blá")

def get_vtex_apps():
    print("rodar vtex ls e listar apps")

def verify_existent_ws():
    print("rodar vtex worksapce list")

def get_who_am_i():
    try:
        who_am_i_result = subprocess.check_output('vtex whoami', shell=True, stderr=subprocess.STDOUT)
        saida_decodificada1 = who_am_i_result.decode('utf-8')
        print(who_am_i_rules(saida_decodificada1))
    except subprocess.CalledProcessError as e:
        print("Ocorreu um erro:", e.output.decode('utf-8'))

def activate_las_ws():
    print("Rodar um vtex use com o ultimo ws usado")

data = read_json(file_path)
vendors = data['vendor-collection']

def run_interface():
    # SECTION window config
    root = tk.Tk()
    root.title("Customer Companion Dev Tool")
    root.geometry("600x575")
    # !SECTION window config
    
    # SECTION Seletor de vendor (x = 152 + 20 = 172) (y = indefinido )
    for index, vendor in enumerate(vendors):
        vendor_name = vendor['vendor-name']
        store_name = vendor['store-name']
        
        button_text = f"{vendor_name}\n{store_name}"
        vendor_select_button = tk.Button(root, text=button_text, command=lambda vn=vendor_name, sn=store_name: on_button_click(vn, sn))
        vendor_select_button.place(x=10, y=10 + (index * 59), width=142, height=49)
    # !SECTION Seletor de vendor

    # SECTION controle de informativos
    informative_btn_frame = tk.LabelFrame(root, text="Acesso aos Informativos", padx=10, pady=10)
    informative_btn_frame.place(x=172, y=00, width=186, height=210)

    primary_info_btn = tk.Button(informative_btn_frame, text="Informações básicas", command=basic_info_pull)
    primary_info_btn.grid(row=0, column=0, padx=0, pady=5, sticky="w")

    get_vtex_apps_btn = tk.Button(informative_btn_frame, text="Apps instalados", command=get_vtex_apps)
    get_vtex_apps_btn.grid(row=1, column=0, padx=0, pady=5, sticky="w")

    verify_existent_ws_btn = tk.Button(informative_btn_frame, text="Verificar ws existente", command=basic_info_pull)
    verify_existent_ws_btn.grid(row=2, column=0, padx=0, pady=5, sticky="w")

    who_am_i_btn = tk.Button(informative_btn_frame, text="Verificar agora", command=get_who_am_i)
    who_am_i_btn.grid(row=3, column=0, padx=0, pady=5, sticky="w")
    
    activate_last_ws_btn = tk.Button(informative_btn_frame, text="Ativar ultimo WS", command=get_vtex_apps)
    activate_last_ws_btn.grid(row=4, column=0, padx=0, pady=5, sticky="w")
    
    # !SECTION controle de informativos

    # SECTION Elementos de teste
    test_frame = tk.LabelFrame(root, text="Área de Teste", padx=10, pady=10)
    test_frame.place(x=172, y=220, width=172, height=150)

    label = tk.Label(test_frame, text="Bem-vindo à Ferramenta de Clientes!")
    label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    quitBtn = tk.Button(test_frame, text="Fechar", command=root.quit)
    quitBtn.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    teste_btn = tk.Button(test_frame, text="Teste algo aqui", command=test_function)
    teste_btn.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    # !SECTION Elementos de teste

    root.mainloop()

if __name__ == "__main__":
    run_interface()