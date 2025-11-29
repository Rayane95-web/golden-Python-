#!/usr/bin/env python3
import json, os, sys, random, time, getpass
from datetime import datetime, timedelta

DATA_FILE = "data.json"

# ----- Terminal colors -----
PURPLE = "\033[95m"
RESET0 = "\033[0m"
LIGHT_GREEN = "\033[92m"
LIGHT_RED = "\033[91m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

# ----- Load / save data -----
def load_data():
    if not os.path.exists(DATA_FILE):
        print("Data file not found! Please make sure data.json exists.")
        sys.exit()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ----- Banner -----
def print_styled_text(text):
    alphabet = {
        'P': ["  ____  ", " |  _ \\ ", " | |_) |", " |  __/ ", " |_|    "],
        'Y': [" __   __", " \\ \\ / /", "  \\ V / ", "   | |  ", "   |_|  "],
        'T': ["  _____ ", " |_   _|", "   | |  ", "   | |  ", "   |_|  "],
        'H': ["  _   _ ", " | | | |", " | |_| |", " |  _  |", " |_| |_|"],
        'O': ["   ___  ", "  / _ \\ ", " | | | |", " | |_| |", "  \\___/ "],
        'N': ["  _   _ ", " | \\ | |", " |  \\| |", " | |\\  |", " |_| \\_|"]
    }
    text = text.upper()
    for row in range(5):
        line = ""
        for ch in text:
            line += alphabet.get(ch, [" " * 8])[row] + "  "
        print(f"{PURPLE}{line}{RESET0}")
    print(f"{CYAN}Dev: Sicario      Instagram: 9attos.2{RESET0}\n")

# ----- Quiz helpers -----
def ask_mcq(qdict):
    print("\n" + qdict["q"])
    for i, choice in enumerate(qdict["choices"]):
        print(f"  {chr(65+i)}) {choice}")
    while True:
        ans = input("Your answer (A/B/C/D): ").strip().upper()
        if ans in ["A","B","C","D"]:
            return ans == qdict["answer"].upper()
        print("Please enter A/B/C/D.")

def run_quiz(qbank, credits_cost):
    total = len(qbank)
    score = 0
    qlist = qbank.copy()
    random.shuffle(qlist)
    for q in qlist:
        correct = ask_mcq(q)
        if correct:
            print(f"{YELLOW}Correct!{RESET0}")
            score += 1
        else:
            print(f"{LIGHT_RED}Wrong. Answer was {q['answer']}{RESET0}")
        time.sleep(0.3)
    print(f"\nScore: {score}/{total}")
    return credits_cost

# ----- Admin panel -----
def list_questions(data, level):
    qlist = data["questions"].get(level, [])
    if not qlist:
        print("No questions.")
        return
    for i, q in enumerate(qlist, 1):
        print(f"{i}) {q['q']} Answer: {q['answer']}")

def add_question(data, level):
    qtext = input("Enter question text: ")
    choices = [input(f"Choice {c}: ") for c in ["A","B","C","D"]]
    ans = ""
    while ans not in ["A","B","C","D"]:
        ans = input("Correct answer (A/B/C/D): ").upper()
    data["questions"].setdefault(level, []).append({"q":qtext,"choices":choices,"answer":ans})
    save_data(data)
    print("Added question.")

def edit_question(data, level):
    qlist = data["questions"].get(level, [])
    if not qlist:
        print("No questions.")
        return
    list_questions(data, level)
    try:
        idx = int(input("Which question number to edit? ")) - 1
        q = qlist[idx]
    except:
        print("Invalid input.")
        return
    newq = input(f"New question text (blank to keep) [{q['q']}]: ")
    if newq: q['q'] = newq
    for i in range(4):
        c = input(f"Choice {chr(65+i)} (blank to keep) [{q['choices'][i]}]: ")
        if c: q['choices'][i] = c
    ans = input(f"Correct answer (A/B/C/D) [{q['answer']}]: ").upper()
    if ans in ["A","B","C","D"]: q['answer'] = ans
    save_data(data)
    print("Edited.")

def delete_question(data, level):
    qlist = data["questions"].get(level, [])
    if not qlist:
        print("No questions.")
        return
    list_questions(data, level)
    try:
        idx = int(input("Which question number to delete? ")) - 1
        qlist.pop(idx)
        save_data(data)
        print("Deleted.")
    except:
        print("Invalid input.")

def edit_codes(data):
    print(data["access_codes"])
    k = input("Which code to edit (USER/VIP/ADMIN): ").upper()
    if k in data["access_codes"]:
        data["access_codes"][k] = input("New code: ")
        save_data(data)
        print("Updated.")

def edit_support_message(data):
    print(data.get("support_message",""))
    msg = input("New support message: ")
    if msg:
        data["support_message"] = msg
        save_data(data)
        print("Updated.")

def change_admin_credentials(data):
    user = input("New username (blank to keep): ").strip()
    pwd = getpass.getpass("New password (blank to keep): ").strip()
    if user: data["admin_credentials"]["username"] = user
    if pwd: data["admin_credentials"]["password"] = pwd
    save_data(data)
    print("Updated admin credentials.")

def admin_panel(data):
    while True:
        print("\n***** ADMIN PANEL *****")
        print("1) View question banks")
        print("2) Add question")
        print("3) Edit question")
        print("4) Delete question")
        print("5) Edit access codes")
        print("6) Edit support message")
        print("7) Change admin credentials")
        print("0) Back")
        choice = input("Choice: ").strip()
        if choice=="1":
            lvl = input("Bank (USER/VIP/ADMIN): ").upper()
            list_questions(data, lvl)
        elif choice=="2":
            lvl = input("Bank (USER/VIP/ADMIN): ").upper()
            add_question(data,lvl)
        elif choice=="3":
            lvl = input("Bank (USER/VIP/ADMIN): ").upper()
            edit_question(data,lvl)
        elif choice=="4":
            lvl = input("Bank (USER/VIP/ADMIN): ").upper()
            delete_question(data,lvl)
        elif choice=="5":
            edit_codes(data)
        elif choice=="6":
            edit_support_message(data)
        elif choice=="7":
            change_admin_credentials(data)
        elif choice=="0":
            break
        input("Press Enter to continue...")
    return data

# ----- Credits handling -----
def check_credits(data, level):
    user = data["users"][level]
    now = datetime.now()
    last = user.get("last_reset")
    if last:
        last_time = datetime.fromisoformat(last)
        if now - last_time >= timedelta(days=1):
            user["credits"] = 100 if level=="USER" else 10000
            user["last_reset"] = now.isoformat()
            save_data(data)
    else:
        user["last_reset"] = now.isoformat()
        save_data(data)
    return user["credits"]

# ----- Main Menu -----
def main_menu(data, access):
    while True:
        print_styled_text("PYTHON")
        credits = check_credits(data, access) if access in ["USER","VIP"] else "-"
        print(f"{YELLOW}Access: {access} | Credits: {credits}{RESET0}\n")
        print(f"{LIGHT_GREEN}1) Best Python websites{RESET0}")
        print(f"{LIGHT_GREEN}2) Take Quiz{RESET0}")
        print(f"{LIGHT_GREEN}3) Support me{RESET0}")
        if access=="VIP":
            print(f"{LIGHT_GREEN}4) Join Sicario Team{RESET0}")
            print(f"{LIGHT_GREEN}5) Exit{RESET0}")
        elif access=="ADMIN":
            print(f"{LIGHT_GREEN}4) Admin Panel{RESET0}")
            print(f"{LIGHT_GREEN}5) Exit{RESET0}")
        else:
            print(f"{LIGHT_GREEN}4) Exit{RESET0}")

        choice = input(f"{PURPLE}Choose option: {RESET0}").strip()
        if choice=="1":
            print(f"{CYAN}1) Python Docs\n2) Real Python\n3) freeCodeCamp\n4) W3Schools\n5) Codecademy{RESET0}")
            input("Press Enter to return...")
        elif choice=="2":
            if access in ["USER","VIP"]:
                if credits<10:
                    print(f"{LIGHT_RED}Not enough credits! Wait or upgrade.{RESET0}")
                    input("Press Enter...")
                    continue
                data["users"][access]["credits"] -=10
                save_data(data)
            qlist = data["questions"].get(access,[])
            run_quiz(qlist,10)
            input("Press Enter to return...")
        elif choice=="3":
            print(data.get("support_message",""))
            input("Press Enter to return...")
        elif choice=="4" and access=="VIP":
            print("To join Sicario team, post a video and tag me on Instagram #Sicario golden python")
            input("Press Enter to continue...")
        elif choice=="4" and access=="ADMIN":
            uname = input("Admin username: ")
            pwd = getpass.getpass("Admin password: ")
            cred = data.get("admin_credentials",{})
            if uname==cred.get("username") and pwd==cred.get("password"):
                admin_panel(data)
            else:
                print("Wrong admin credentials.")
                input("Press Enter...")
        elif (access=="VIP" and choice=="5") or (access=="ADMIN" and choice=="5") or (access!="VIP" and access!="ADMIN" and choice=="4"):
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

# ----- Start App -----
def start_app():
    data = load_data()
    print_styled_text("PYTHON")
    print("Login via:\n1) Access code\n2) Admin username/password")
    method = input("Method 1 or 2 : ").strip()
    access = None
    if method=="1":
        code = input("Enter code: ").strip()
        for k,v in data["access_codes"].items():
            if code==v:
                access = k
        if not access:
            print("Wrong code. Exiting.")
            sys.exit()
    else:
        uname = input("Username: ")
        pwd = getpass.getpass("Password: ")
        cred = data.get("admin_credentials",{})
        if uname==cred.get("username") and pwd==cred.get("password"):
            access="ADMIN"
        else:
            print("Wrong credentials. Exiting.")
            sys.exit()
    print(f"{LIGHT_GREEN}Access granted: {access}{RESET0}")
    main_menu(data, access)

if __name__=="__main__":
    start_app()
