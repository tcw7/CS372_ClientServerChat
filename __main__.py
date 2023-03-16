# reference:
# [Python modules and packages](https://realpython.com/python-modules-packages/#the-module-search-path)

import src

CLIENT_PROMPT = "Start client? [y/n]: "
SERVER_PROMPT = "Start server? [y/n]: "
EXIT_MESSAGE = "No option selected. Exiting..."

def main():
    choice = input(SERVER_PROMPT)
    if choice == 'y':
        print("Starting server...")
        src.Server().run()
        exit(0)
    choice = input(CLIENT_PROMPT)
    if choice == 'y':
        print("Starting client...")
        src.Client().run()
        exit(0)
    print(EXIT_MESSAGE)
    exit(0)

if __name__=="__main__":
    main()