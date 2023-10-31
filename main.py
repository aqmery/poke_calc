def load():
    pds_rare = []
    all_pokemon = []
    with open("pds_rare.txt", "r") as file1:
        for i in file1:
            stripped_line = i.strip()
            if len(stripped_line) < 1 or stripped_line[0] == "-" or stripped_line == "Mudae" \
                    or stripped_line == "BOT" or stripped_line[:3] == "â€”":
                continue
            else:
                pds_rare.append(stripped_line)
    pds_rare.reverse()
    with open("pokemon.txt") as file2:
        for i in file2:
            stripped_line = i.strip()
            all_pokemon.append(stripped_line)
        all_pokemon.reverse()
    stars = [["1:shinySparkles:", 5.5], ["2:shinySparkles:", 5.5], ["3:shinySparkles:", 6], ["4:shinySparkles:", 9],
            ["5:shinySparkles:", 45], ["UB:shinySparkles:", 55], ["Paradox:Sparkles:", 55], ["1ðŸŒŸ", 0.5], ["2ðŸŒŸ", 0.5],
            ["3ðŸŒŸ", 1], ["4ðŸŒŸ", 4], ["5ðŸŒŸ", 40], ["UBðŸŒŸ", 50], ["ParadoxðŸŒŸ", 50]]
    return pds_rare, all_pokemon, stars

def create_pokedex(all_pokemon: list, stars: list):
    pokedex = {}
    temp = []
    star_names = [star[0] for star in stars]
    for i in all_pokemon:
        temp.append(i)
        if any(star in i for star in star_names):
            pokedex[temp[-1]] = temp[:-1]
            temp.clear()
    return pokedex

def get_current_pokedex(pds_rare: list, stars: list):
    current_dex = {}
    temp = []
    for i in pds_rare:
        temp.append(i)
        for star in stars:
            if star[0] in i:
                current_dex[temp[-1]] = temp[:-1], star[1]
                temp.clear()
    return current_dex

def get_missing_shinies(current_dex: dict, global_dex: dict):
    owned_shinies ,all_pokemon ,missing_shinies = [], [], []
    for values, value in current_dex.values():
        for item in values:
            if ":shinySparkles:" in item:
                owned_shinies.append(item.split(":shinySparkles:")[0].split(":")[-1].strip())
    for values in global_dex.values():
        for item in values:
            all_pokemon.append(item)
    for i in all_pokemon:
        if i not in owned_shinies:
            missing_shinies.append(i)
    missing_shinies.reverse()
    return missing_shinies

def get_missing_pokemon(current_dex: dict, global_dex: dict):
    owned_pokemon, missing_pokemon, all_pokemon = [], [], []
    for values, value in current_dex.values():
        for item in values:
            if not ":shinySparkles:" in item:
                owned_pokemon.append(item.split(":")[-1].strip())
    for values in global_dex.values():
        for item in values:
            all_pokemon.append(item)
    for i in all_pokemon:
        if i not in owned_pokemon:
            missing_pokemon.append(i)
    missing_pokemon.reverse()
    return missing_pokemon

def count_rolls(current_dex: dict):
    rolls = []
    for values, value in current_dex.values():
        temp = []
        for i in values:
            if i[-1].isdigit():
                if i == ":porygon2: Porygon2":
                    continue
                amount = int(i.split("x")[-1].strip())
                temp.append(amount * value)
        rolls.append(sum(temp))
    return rolls

def print_list(lst: list):
    newstring = ""
    for i in range(len(lst)):
        newstring += lst[i]
        if i != len(lst) - 1:
            newstring += ", "
    return newstring

def release_commands():
    pass

def settings():
    pass

def prints(missing_shinies: list, missing_pokemon: list, counts: list):
    print(f"missing shinies: {print_list(missing_shinies)}")
    print(f"missing pokemon: {print_list(missing_pokemon)}")
    print(f"rolls: {counts}")

def main():
    pds_rare, all_pokemon, stars = load()
    global_dex = create_pokedex(all_pokemon, stars)
    current_dex = get_current_pokedex(pds_rare, stars)
    missing_shinies = get_missing_shinies(current_dex, global_dex)
    missing_pokemon = get_missing_pokemon(current_dex, global_dex)
    counts = count_rolls(current_dex)
    prints(missing_shinies, missing_pokemon, counts)


if __name__ == "__main__":
    main()