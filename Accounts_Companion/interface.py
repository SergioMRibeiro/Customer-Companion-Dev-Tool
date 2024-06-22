import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess
import re

current_path = os.getcwd()

file_path = os.path.join(current_path, 'Accounts_Companion', 'configs.json')

########################################################
################################# Funcionalidades
########################################################

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def write_json(data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def add_vendor_to_collection(vendor_name, site, store_name, directory):
    data = read_json(file_path)

    new_vendor = {
        "vendor-name": vendor_name,
        "site": site,
        "store-name": store_name,
        "last-ws": '',
        "directory": directory
    }

    data["vendor-collection"].append(new_vendor)

    write_json(data)

def remove_vendor_from_collection(search_value):
    # Ler o JSON atual
    data = read_json(file_path)

    # Encontrar o dicionário com 'vendor-name' igual a search_value
    for vendor in data["vendor-collection"]:
        if vendor.get('vendor-name') == search_value:
            data["vendor-collection"].remove(vendor)
            break  # Parar o loop assim que o primeiro fornecedor for removido

    # Escrever de volta no arquivo JSON
    write_json(data)

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
    add_vendor_to_collection(file_path, 'novovendor', 'novosite.com', 'nomesite2', 'none', 'none')
    
    # try:
    #     saida1 = subprocess.check_output('vtex whoami', shell=True, stderr=subprocess.STDOUT)
    #     saida_decodificada1 = saida1.decode('utf-8')
    #     print(who_am_i_rules(saida_decodificada1))

    #     saida2 = subprocess.check_output('vtex ls', shell=True, stderr=subprocess.STDOUT)
    #     saida_decodificada2 = saida2.decode('utf-8')
    # except subprocess.CalledProcessError as e:
    #     print("Ocorreu um erro:", e.output.decode('utf-8'))

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

def on_info_button_click():
    messagebox.showinfo("Informações do Customer Companion Dev Tool", f"Versão: 0.0.1\nCriado por: Sérgio Moreira Ribeiro\ndata de criação: 19/06/2024\n\n\nÉ um prazer poder contribuir com você! Caso tenha alguma ideia de como melhorar esse programa pode me produrar pelo LinkedIn :D")
    print("Botão 'i' clicado!")


########################################################
################################# Elementos da interface
########################################################

data = read_json(file_path)
vendors = data['vendor-collection']

output_result_text = 'Tenha uma ótima aventura Vtex :D'
output_back_ground_color='#fffcbc'

def create_refresh_content_button(root):
    # TODO Tranformar essa função em um frame para comportar os botões de atualizar vendor e fechar
    refresh_content_button = tk.Button(root, text="Sair", command=root.quit, font=("Arial", 9, "normal"),  bg='#6a3131', foreground='#ffffff')
    refresh_content_button.grid(row=2, column=0, columnspan=3, sticky="w")

def create_info_button(root):
    info_button = tk.Button(root, text="i", command=on_info_button_click, fg="#000000", font=("Arial", 12, "bold"), relief="flat")
    info_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

def create_vendor_select_area(root):
    vendor_select_area_frame = tk.Frame(root)
    vendor_select_area_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
    vendor_select_area_frame.grid_rowconfigure(0, weight=0)
    vendor_select_area_frame.grid_columnconfigure(0, weight=1)

    for index, vendor in enumerate(vendors):
        vendor_name = vendor['vendor-name']
        store_name = vendor['store-name']
        button_text = f"{vendor_name}\n{store_name}"
        vendor_select_button = tk.Button(vendor_select_area_frame, text=button_text, command=lambda vn=vendor_name, sn=store_name: on_button_click(vn, sn))
        vendor_select_button.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

def create_informative_controls(root):
    informative_btn_frame = tk.LabelFrame(root, text="Acesso aos Informativos", padx=10, pady=10)
    informative_btn_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    informative_btn_frame.grid_rowconfigure(0, weight=1)
    informative_btn_frame.grid_columnconfigure(0, weight=1)

    primary_info_btn = tk.Button(informative_btn_frame, text="Informações básicas", command=basic_info_pull)
    primary_info_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    get_vtex_apps_btn = tk.Button(informative_btn_frame, text="Apps instalados", command=get_vtex_apps)
    get_vtex_apps_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    verify_existent_ws_btn = tk.Button(informative_btn_frame, text="Verificar ws existente", command=basic_info_pull)
    verify_existent_ws_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    who_am_i_btn = tk.Button(informative_btn_frame, text="Verificar agora", command=get_who_am_i)
    who_am_i_btn.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    activate_last_ws_btn = tk.Button(informative_btn_frame, text="Ativar ultimo WS", command=get_vtex_apps)
    activate_last_ws_btn.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

def create_creation_area(root):
    creation_area_frame = tk.LabelFrame(root, text="Criar e Deletar Vendor's", padx=10, pady=10)
    creation_area_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    creation_area_frame.grid_rowconfigure(0, weight=0)
    creation_area_frame.grid_columnconfigure(0, weight=1)

    vendor_input_label = tk.Label(creation_area_frame, text="Vendor *")
    vendor_input_label.grid(row=0, column=0, padx=5, pady=5, sticky="w", columnspan=2)

    vendor_input = tk.Entry(creation_area_frame, width=1)
    vendor_input.grid(row=1, column=0, padx=5, pady=0, sticky="ew", columnspan=2)

    store_name_input_label = tk.Label(creation_area_frame, text="Nome da loja")
    store_name_input_label.grid(row=2, column=0, padx=5, pady=5, sticky="w", columnspan=2)

    store_name_input = tk.Entry(creation_area_frame, width=1)
    store_name_input.grid(row=3, column=0, padx=5, pady=0, sticky="ew", columnspan=2)

    store_home_page_input_label = tk.Label(creation_area_frame, text="URL final da loja")
    store_home_page_input_label.grid(row=4, column=0, padx=5, pady=5, sticky="w", columnspan=2)

    store_home_page_input = tk.Entry(creation_area_frame, width=1)
    store_home_page_input.grid(row=5, column=0, padx=5, pady=0, sticky="ew", columnspan=2)

    directory_input_label = tk.Label(creation_area_frame, text="Pasta raiz do projeto")
    directory_input_label.grid(row=6, column=0, padx=5, pady=5, sticky="w", columnspan=2)

    directory_input = tk.Entry(creation_area_frame, width=1)
    directory_input.grid(row=7, column=0, padx=5, pady=0, sticky="ew", columnspan=2)


    # btn ações
    quitBtn = tk.Button(creation_area_frame, text="Deletar Vendor", command=lambda: remove_vendor_from_collection('novovendor2'), bg='#6a3131', foreground='#ffffff')
    quitBtn.grid(row=8, column=0, padx=5, pady=10, sticky="ew")

    teste_btn = tk.Button(creation_area_frame, text="Teste algo aqui", command=lambda: add_vendor_to_collection(
        vendor_input.get(),
        store_home_page_input.get(),
        store_name_input.get(),
        directory_input.get()
    ), bg='#31557f', foreground='#ffffff')
    
    teste_btn.grid(row=8, column=1, padx=5, pady=10, sticky="ew")

def create_info_display(root):
    info_display_frame = tk.LabelFrame(root, text="Informações", padx=10, pady=10)
    info_display_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

    info_display_frame.grid_rowconfigure(0, weight=1)
    info_display_frame.grid_columnconfigure(0, weight=1)

    output_color_frame = tk.Frame(info_display_frame, bg=output_back_ground_color)
    output_color_frame.grid(row=0, column=0, sticky="nsew")


    # output_text = tk.Label(output_color_frame, text=output_result_text, bg=output_back_ground_color)
    # output_text.grid(column=0, row=0)

    # Uso do widget Text para exibir texto interativo e selecionável
    output_text = tk.Text(output_color_frame, bg=output_back_ground_color, wrap="word", relief="flat")
    output_text.insert("1.0", output_result_text)
    output_text.config(state="disabled")  # Faz o texto ser apenas leitura
    output_text.grid(column=0, row=0, sticky="n", padx=10, pady=10)

def run_interface():
    root = tk.Tk()
    root.title("Customer Companion Dev Tool")
    root.geometry("800x600")

    root.grid_columnconfigure(0, weight=1, minsize=150)
    root.grid_columnconfigure(1, weight=1, minsize=250)
    root.grid_columnconfigure(2, weight=2, minsize=400)

    create_info_button(root)
    create_vendor_select_area(root)
    create_informative_controls(root)
    create_creation_area(root)
    create_info_display(root)
    create_refresh_content_button(root)

    root.mainloop()

if __name__ == "__main__":
    run_interface()