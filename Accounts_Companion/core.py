# meu_projeto/core.py
from Accounts_Companion.interface import run_interface
from .files_services import check_and_create_config_file


def main():
    check_and_create_config_file()
    print("Ainda em desenvolvimento")
    run_interface()

if __name__ == "__main__":
    main()