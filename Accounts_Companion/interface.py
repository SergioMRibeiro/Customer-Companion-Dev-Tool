import tkinter as tk
from tkinter import messagebox
from .files_services import read_json, write_json
import subprocess
import re



output_back_ground_color='#fffcbc'
danger_back_ground_color='#6a3131'
primary_back_ground_color='#31557f'
output_text_widget = None
output_result_text = "Tenha uma ótima aventura Vtex :D"

########################################################
################################# Funcionalidades
########################################################




def add_vendor_to_collection(vendor_name, site, store_name, directory):
    data = read_json()

    new_vendor = {
        "vendor-name": vendor_name,
        "site": site,
        "store-name": store_name,
        "last-ws": '',
        "directory": directory
    }

    data["vendor-collection"].append(new_vendor)

    update_output_text(f"vendor-name: {vendor_name},\nsite: {site},\nstore-name: {store_name},\nlast-ws: {''},\ndirectory: {directory}\n")

    write_json(data)

def remove_vendor_from_collection(search_value):
    data = read_json()
    # Encontrar o dicionário com 'vendor-name' igual a search_value
    for vendor in data["vendor-collection"]:
        print('To chegando aqui',search_value, vendor.get('vendor-name'), search_value == vendor.get('vendor-name'))
        if vendor.get('vendor-name') == search_value:
            print('Achei o danado')
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
        return f"Vendor: {vendor}\nWorkspace: {workspace}\nAmbiente: {ambient}\nLogado com email: {email}"
    else:
        return None

def extract_app_sections(text):
    # Separar os blocos de texto por quebras de linha duplas
    sections = text.strip().split("\n\n")

    # Dicionário para armazenar os blocos
    apps_dict = {
        "edition_apps": [],
        "installed_apps": [],
        "linked_apps": []
    }

    # Identificar cada seção pelo seu cabeçalho
    for section in sections:
        if section.startswith("Edition Apps"):
            apps_dict["edition_apps"].append(section)
        elif section.startswith("Installed Apps"):
            apps_dict["installed_apps"].append(section)
        elif section.startswith("Linked Apps"):
            apps_dict["linked_apps"].append(section)
    
    # Concatenar as listas em strings
    edition_apps = "\n\n".join(apps_dict["edition_apps"])
    installed_apps = "\n\n".join(apps_dict["installed_apps"])
    linked_apps = "\n\n".join(apps_dict["linked_apps"])

    return edition_apps, installed_apps, linked_apps

def on_vendor_button_click(vendor_name, store_name):
    try:
        subprocess.check_output(f'vtex switch {vendor_name}', shell=True, stderr=subprocess.STDOUT)
        get_who_am_i()
    except subprocess.CalledProcessError as error:
        update_output_text(f"Ocorreu um erro:\n {error}")

def update_output_text(new_text):
    global output_result_text, output_text_widget
    output_result_text = new_text
    output_text_widget.config(state="normal")  # Permitir edição temporária
    output_text_widget.delete("1.0", tk.END)
    output_text_widget.insert("1.0", output_result_text)
    output_text_widget.config(state="disabled")  # Voltar ao modo de apenas leitura

def open_web_site_pull():
    print("Abrir site final")

def get_vtex_apps():
    try:
        vtex_ls_result = subprocess.check_output('vtex ls', shell=True, stderr=subprocess.STDOUT)
        decoded_result = vtex_ls_result.decode('utf-8')
        edition, installed, linked = extract_app_sections(decoded_result)
        update_output_text(f'{linked}\n\n\n{installed}\n\n\n{edition}')
    except subprocess.CalledProcessError as error:
        update_output_text(f"Ocorreu um erro:\n {error}")

def verify_existent_ws():
    try:
        ws_list_result = subprocess.check_output('vtex workspace list', shell=True, stderr=subprocess.STDOUT)
        decoded_result = ws_list_result.decode('utf-8')
        update_output_text(ws_list_result)
    except subprocess.CalledProcessError as e:
        update_output_text(f"Ocorreu um erro:\n {e.output.decode('utf-8')}")

def get_who_am_i():
    try:
        who_am_i_result = subprocess.check_output('vtex whoami', shell=True, stderr=subprocess.STDOUT)
        decoded_result = who_am_i_result.decode('utf-8')
        update_output_text(who_am_i_rules(decoded_result))
    except subprocess.CalledProcessError as e:
        update_output_text(f"Ocorreu um erro:\n {e}")

def activate_last_ws():
    print("Rodar um vtex use com o ultimo ws usado")

def on_info_button_click():
    messagebox.showinfo("Informações do Customer Companion Dev Tool", f"Versão: 0.0.1\nCriado por: Sérgio Moreira Ribeiro\ndata de criação: 19/06/2024\n\n\nÉ um prazer poder contribuir com você! Caso tenha alguma ideia de como melhorar esse programa pode me produrar pelo LinkedIn :D")

def refresh_vendor_list(root):
    vendors = read_json()
    create_vendor_select_area(root,  vendors["vendor-collection"])


########################################################
################################# Elementos da interface
########################################################

data = read_json()
vendors = data['vendor-collection']


def create_info_button(root):
    info_button = tk.Button(root, text="i", command=on_info_button_click, fg="#000000", font=("Arial", 12, "bold"), relief="flat")
    info_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

def create_vendor_select_area(root, vendor_collection):
    # Remove os widgets existentes antes de recriar
    for widget in root.grid_slaves(row=0, column=0):
        widget.destroy()

    vendor_select_area_frame = tk.Frame(root)
    vendor_select_area_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
    vendor_select_area_frame.grid_rowconfigure(0, weight=0)
    vendor_select_area_frame.grid_columnconfigure(0, weight=1)

    for index, vendor in enumerate(vendor_collection):
        vendor_name = vendor['vendor-name']
        store_name = vendor['store-name']
        button_text = f"{vendor_name}\n{store_name}"
        vendor_select_button = tk.Button(vendor_select_area_frame, text=button_text, command=lambda vn=vendor_name, sn=store_name: on_vendor_button_click(vn, sn))
        vendor_select_button.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

def create_informative_controls(root):
    informative_btn_frame = tk.LabelFrame(root, text="Acesso aos Informativos", padx=10, pady=10)
    informative_btn_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    informative_btn_frame.grid_rowconfigure(0, weight=1)
    informative_btn_frame.grid_columnconfigure(0, weight=1)

    primary_info_btn = tk.Button(informative_btn_frame, text="Abrir site final", command=open_web_site_pull, state='disable')
    primary_info_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    get_vtex_apps_btn = tk.Button(informative_btn_frame, text="Apps instalados", command=get_vtex_apps)
    get_vtex_apps_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    verify_existent_ws_btn = tk.Button(informative_btn_frame, text="Verificar ws existente", command=verify_existent_ws)
    verify_existent_ws_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    who_am_i_btn = tk.Button(informative_btn_frame, text="Verificar ambiente atual", command=get_who_am_i)
    who_am_i_btn.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    activate_last_ws_btn = tk.Button(informative_btn_frame, text="Ativar ultimo WS", command=get_vtex_apps, state='disable')
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
    deletar_vendor_btn = tk.Button(creation_area_frame, text="Deletar Vendor", command=lambda:( remove_vendor_from_collection(vendor_input.get()), refresh_vendor_list(root)), bg=danger_back_ground_color, foreground='#ffffff')
    deletar_vendor_btn.grid(row=8, column=0, padx=5, pady=10, sticky="ew")

    create_vendor_btn = tk.Button(creation_area_frame,
        text="Salvar Vendor", 
        command=lambda: (add_vendor_to_collection(
                vendor_input.get(),
                store_home_page_input.get(),
                store_name_input.get(),
                directory_input.get(),
            ),
                refresh_vendor_list(root)
            ), 
        bg=primary_back_ground_color,
        foreground='#ffffff')
    
    create_vendor_btn.grid(row=8, column=1, padx=5, pady=10, sticky="ew")

def create_info_display(root):
    global output_text_widget

    # Configuração do frame principal
    info_display_frame = tk.LabelFrame(root, text="Informações", padx=10, pady=10)
    info_display_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)

    info_display_frame.grid_rowconfigure(0, weight=1)
    info_display_frame.grid_columnconfigure(0, weight=1)


    # Configuração do frame de cor de fundo
    output_color_frame = tk.Frame(info_display_frame, bg=output_back_ground_color)
    output_color_frame.grid(row=0, column=0, sticky="nsew")
    output_color_frame.grid_rowconfigure(0, weight=1)
    output_color_frame.grid_columnconfigure(0, weight=1)
    
    scrollbar = tk.Scrollbar(output_color_frame)
    scrollbar.grid(row=0, column=1, sticky="ns")
    

    # Configuração do widget de texto
    output_text_widget = tk.Text(output_color_frame, wrap="word", relief="flat", bg=output_back_ground_color, yscrollcommand=scrollbar.set)
    output_text_widget.insert("1.0", output_result_text)
    output_text_widget.config(state="disabled")  # Faz o texto ser apenas leitura
    output_text_widget.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
    
    scrollbar.config(command=output_text_widget.yview)

def create_quit_and_refresh_content_button(root):    
    quit_and_refresh_container = tk.Frame(root)
    quit_and_refresh_container.grid(row=2, column=0, pady=10, columnspan=3, sticky="w")
    
    refresh_content_button = tk.Button(quit_and_refresh_container, text="Sair", command=root.quit, font=("Arial", 9, "normal"),  bg=danger_back_ground_color, foreground='#ffffff')
    refresh_content_button.grid(row=0, column=0, padx=10, sticky="w")

    refresh_content_button = tk.Button(quit_and_refresh_container, text="Atualizar lista de vendor", command=lambda: refresh_vendor_list(root), font=("Arial", 9, "normal"),  bg=primary_back_ground_color, foreground='#ffffff')
    refresh_content_button.grid(row=0, column=1, padx=10, sticky="w")

def run_interface():
    root = tk.Tk()
    root.title("Customer Companion Dev Tool")
    root.geometry("900x600")

    root.grid_columnconfigure(0, weight=1, minsize=150)
    root.grid_columnconfigure(1, weight=1, minsize=250)
    root.grid_columnconfigure(2, weight=2, minsize=400)

    create_info_button(root)
    create_vendor_select_area(root, data["vendor-collection"])
    create_informative_controls(root)
    create_creation_area(root)
    create_info_display(root)
    create_quit_and_refresh_content_button(root)

    root.mainloop()

if __name__ == "__main__":
    run_interface()