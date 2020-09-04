#!/usr/bin/env python3
import sys,os,json,random,re
assert sys.version_info >= (3,8), "This script requires at least Python 3.8"

set_variables = {}


def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage_pid(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}

def find_passage_name(game_desc, name):
    for p in game_desc["passages"]:
        if p["name"] == name:
            return p
    return {}

def get_random(s):
    r = s.split(",")
    try:
        return str(random.randint(int(r[0]),int(r[1])))
    except:
        pass
    return str(0)

def format_random(description):
    m = re.search(r'\(random: \d,\d\)', description)
    while m:
        r = re.sub(r'\(random: (\d,\d)\)',r'\1',m.group(0))
        description = re.sub(r'\(random: \d,\d\)',get_random(r),description)
        m = re.search(r'\(random: \d,\d\)', description)
    return description

def format_set(description):
    v_list = re.findall("\$[^\s]+",description)
    for v in v_list:
        if v not in set_variables:
            set_variables[v] = "0"
    m = re.search(r'\(set: \$[^\s]+ to [^\)]+\)', description)
    while m:
        r = re.sub(r'\(set: (\$[^\s]+) to ([^\)]+)\)',r'\1|\2',m.group(0))
        v_parse = r.split("|")
        
        print(r)
        description = description.replace(m.group(0),"")
        m = re.search(r'\(set: \$[^\s]+ to [^\)]+\)', description)
    return description

def format_links(description):
    description = re.sub(r'(\[\[[^\|]*)\|([^\]]*\]\])',r'\1->\2',description)
    choices = re.findall(r'\[\[[^(->)]*->[^\]]*\]\]',description)
    which_option = 1
    for c in choices:
        option = re.sub(r'\[\[([^(->)]*)->([^\]]*)\]\]',r'\1',c)
        description = description.replace(c, "[{}] {}".format(which_option,option))
        which_option += 1
    return description

def format_variables(description):
    v_list = re.findall("\$[^\s]+",description)
    for v in v_list:
        if v not in set_variables:
            set_variables[v] = "0"
    print(set_variables)
    for s in set_variables:
        description = description.replace(s, set_variables[s])
    return description

def format_desc(description, current):
    description = format_random(description)
    description = format_set(description)
    # if and else
    description = format_links(description)
    description = format_variables(description)

    #remove (display: ) command for now; we'll put it back in render()
    description = re.sub(r'\(display: \"[^"]*\"\)','',description)
    return description

def format_display(description, current, game_desc):
    m = re.search(r'\(display: \"[^"]*\"\)', description)
    while m:
        d = re.sub(r'\(display: \"([^"]*)\"\)',r'\1',m.group(0))
        old_current = current
        current = find_passage_name(game_desc, d)
        if old_current == current:
            break
        render(current, game_desc)
        m = re.search(r'\(display: \"[^"]*\"\)', description)
    return current





# ------------------------------------------------------

def update(current, game_desc, choice):
    if choice == "":
        return current
    if choice.isdigit():
        try: 
            c = int(choice) - 1
            l = current["links"][c]
            new_current = find_passage_pid(game_desc,l["pid"])
            if new_current:
                return new_current
        except:
            pass
    
    print("\nI don't understand that option. Please choose again:\n\n")
    return current

def render(current, game_desc):
    r = format_desc(current["text"], current)
    print("\n\n" + r)
    current = format_display(current["text"], current, game_desc)
    return current

def get_input(current):
    choice = input("What would you like to do? (type quit to exit) ")
    choice = choice.lower()
    if choice in ["quit","q","exit"]:
        return "quit"
    return choice

# ------------------------------------------------------

def main():
    game_desc = load("rpg.json")
    current = find_passage_pid(game_desc, game_desc["startnode"])
    choice = ""

    while choice != "quit" and current != {}:
        current = update(current, game_desc, choice)
        current = render(current, game_desc)
        choice = get_input(current)

    print("Thanks for playing!")




if __name__ == "__main__":
    main()