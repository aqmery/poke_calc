import re

class PokemonCalc:
    def __init__(self):
        self.pds_rare = []
        self.all_pokemon = []
        self.missing_shinies = []
        self.missing_pokemon = []
        self.counts = []
        self.stars = [["1:shinySparkles:", 5.5], ["2:shinySparkles:", 5.5], ["3:shinySparkles:", 6], ["4:shinySparkles:", 9],
                ["5:shinySparkles:", 45], ["UB:shinySparkles:", 55], ["Paradox:Sparkles:", 55], ["1ðŸŒŸ", 0.5], ["2ðŸŒŸ", 0.5],
                ["3ðŸŒŸ", 1], ["4ðŸŒŸ", 4], ["5ðŸŒŸ", 40], ["UBðŸŒŸ", 50], ["ParadoxðŸŒŸ", 50]]
        self.star_names = [self.stars[i][0] for i in range(len(self.stars))]
        self.global_dex = {}
        self.current_dex = {}


    def load(self):
        with open("pds_rare.txt", "r") as pds_file:
            for i in pds_file:
                stripped_line = i.strip()
                if len(stripped_line) < 1 or stripped_line[0] == "-" or stripped_line == "Mudae" \
                        or stripped_line == "BOT" or stripped_line[:3] == "â€”":
                    continue
                else:
                    self.pds_rare.append(stripped_line)
        self.pds_rare.reverse()
        with open("pokemon.txt") as pkm_file:
            for i in pkm_file:
                stripped_line = i.strip()
                self.all_pokemon.append(stripped_line)
            self.all_pokemon.reverse()

    def create_pokedex(self):
        temp = []
        star_names = [star[0] for star in self.stars]
        for i in self.all_pokemon:
            temp.append(i)
            if any(star in i for star in star_names):
                self.global_dex[temp[-1]] = temp[:-1]
                temp.clear()


    def get_current_pokedex(self):
        temp = []
        for i in self.pds_rare:
            temp.append(i)
            for star in self.stars:
                if star[0] in i:
                    self.current_dex[temp[-1]] = temp[:-1], star[1]
                    temp.clear()


    def get_missing_shinies(self):
        owned_shinies = []
        regex = r"(:\w+:) ([\w:.'Ã©bÃ©-]+) :shinySparkles:"
        for values, value in self.current_dex.values():
            for item in values:
                match = re.search(regex, item)
                if match:
                    owned_shinies.append(match.group(2))
        for i in self.all_pokemon:
            if i in self.star_names:
                continue
            if i not in owned_shinies:
                self.missing_shinies.append(i)
        self.missing_shinies.reverse()

    def get_missing_pokemon(self):
        owned_pokemon= []
        regex = r"(:\w+:) ([\w:.'Ã©bÃ©-]+)"
        for values, value in self.current_dex.values():
            for item in values:
                match = re.search(regex, item)
                if match:
                    owned_pokemon.append(match.group(2))
        for i in self.all_pokemon:
            if i in self.star_names:
                continue
            if i not in owned_pokemon:
                self.missing_pokemon.append(i)
        self.missing_pokemon.reverse()


    def count_rolls(self):
        for values, value in self.current_dex.values():
            temp = []
            for i in values:
                if i[-1].isdigit():
                    if i == ":porygon2: Porygon2":
                        continue
                    amount = int(i.split("x")[-1].strip())
                    temp.append((amount-1)* value)
            self.counts.append(sum(temp))


    def print_list(self, lst: list):
        newstring = ""
        for i in range(len(lst)):
            newstring += lst[i]
            if i != len(lst) - 1:
                newstring += ", "
        return newstring


    def release_commands(self, shiny = False):
        pass


    def settings(self):
        pass


    def print_lines(self, print_lenght = 20):
        print(f"total amount of missing pokemon: {len(self.missing_pokemon)}/{int(len(self.all_pokemon)-len(self.star_names)/2)}, "
              f"total amount of missing shinies: {len(self.missing_shinies)}/{int(len(self.all_pokemon)-len(self.star_names)/2)}\n")
        
        print(f"missing shinies: {self.print_list(self.missing_shinies[:print_lenght])}\n")
        print(f"missing pokemon: {self.print_list(self.missing_pokemon[:print_lenght])}\n")

        print(f"total rolls: {sum(self.counts)}")
        print(f"4* rolls: {sum(self.counts[9:10])},   5* rolls: {sum(self.counts[10:11])},   UB rolls: {sum(self.counts[11:12])},   paradox rolls: {sum(self.counts[12:])}\n")
        print(f"total normal hidden rolls: {sum(self.counts[9:12])}")
        
        print(f"rolls from shinies: {sum(self.counts[0:6])}")
        print(f"rolls from non-shinies: {sum(self.counts[6:])}\n")


if __name__ == "__main__":
    calc = PokemonCalc()
    calc.load()
    calc.create_pokedex()
    calc.get_current_pokedex()
    calc.get_missing_shinies()
    calc.get_missing_pokemon()
    calc.count_rolls()
    calc.print_lines()