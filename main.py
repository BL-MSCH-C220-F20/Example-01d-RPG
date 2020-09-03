#!/usr/bin/env python3
import sys,os,json,random,re
assert sys.version_info >= (3,8), "This script requires at least Python 3.8"

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}

def get_random(s):
    r = s.split(",")
    if r.len() > 1 and all(isinstance(r, int)):
        return random.randint(r[0],r[1])
    return 0

def format_desc(description, current):
    # random
    m = re.match(r'\(random: \d,\d\)', description)
    while m:
        r = re.sub(r'\(random: (\d,\d)\))',r'\1',m.group(0))
        description = re.sub(r'\(random: \d,\d\)',get_random(r),description)
        m = re.match(r'\(random: \d,\d\)', description)
    # set
    # if and else
    # links
    description = re.sub(r'(\[\[[^\|]*)\|([^\]]*\]\])',r'\1->\2',description)
    choices = re.findall(r'\[\[[^(->)]*->[^\]]*\]\]',description)
    which_option = 1
    for c in choices:
        option = re.sub(r'\[\[([^(->)]*)->([^\]]*)\]\]',r'\1',c)
        description = description.replace(c, "[{}] {}".format(which_option,option))
        which_option += 1
    return description



# ------------------------------------------------------

def update(current, game_desc, choice):
    if choice == "":
        return current
    if choice.isdigit():
        try: 
            c = int(choice) - 1
            l = current["links"][c]
            new_current = find_passage(game_desc,l["pid"])
            if new_current:
                return new_current
        except:
            pass
    
    print("\nI don't understand that option. Please choose again:\n\n")
    return current

def render(current):
    r = format_desc(current["text"], current)
    #display
    print(r)

def get_input(current):
    choice = input("What would you like to do? (type quit to exit) ")
    choice = choice.lower()
    if choice in ["quit","q","exit"]:
        return "quit"
    return choice

# ------------------------------------------------------

def main():
    game_desc = load("rpg.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""

    while choice != "quit" and current != {}:
        current = update(current, game_desc, choice)
        render(current)
        choice = get_input(current)

    print("Thanks for playing!")




if __name__ == "__main__":
    main()