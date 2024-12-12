class Player:
    def __init__(self, name, serve_win_prob, wins, matches):
        self.name = name  # Namnet på spelaren
        self.serve_win_prob = serve_win_prob  # Sannolikhet att vinna en serve, mellan 0 och 1
        self.wins = wins  # Antal vunna matcher
        self.matches = matches  # Totalt antal spelade matcher

    def win_percentage(self):
        # Returnerar vinstprocenten som ett decimaltal
        # Om inga matcher spelats, undviks division med noll genom att returnera 0
        if self.matches > 0:
            return self.wins / self.matches
        return 0

    def update_result(self, won):
        # Uppdaterar spelarens statistik efter en match
        self.matches += 1  # Antalet matcher ökar alltid
        if won:  # Om spelaren vinner, öka antalet vinster
            self.wins += 1

    def __str__(self):
        # Formaterar spelarens data för att skriva till fil
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"

    @staticmethod
    def read_players_from_file(filename):
        # Läser spelarens data från en fil, där varje spelare har fyra rader information
        players = []
        with open(filename, "r") as f:
            lines = f.read().strip().split("\n")
            for i in range(0, len(lines), 4):
                name = lines[i].strip()
                serve_win_prob = float(lines[i + 1].strip())
                wins = int(lines[i + 2].strip())
                matches = int(lines[i + 3].strip())
                players.append(Player(name, serve_win_prob, wins, matches))
        return players

    @staticmethod
    def write_players_to_file(filename, players):
        # Skriver spelarens uppdaterade data tillbaka till filen
        with open(filename, "w") as f:
            for player in players:
                f.write(str(player) + "\n")

class Match:
    def __init__(self, player1, player2):
        self.player1 = player1  # Spelare 1 i matchen
        self.player2 = player2  # Spelare 2 i matchen

    def update_match_result(self, winner_name):
        # Uppdaterar resultatet för båda spelarna beroende på vem som vann
        if self.player1.name.lower() == winner_name.lower():
            self.player1.update_result(True)
            self.player2.update_result(False)
        elif self.player2.name.lower() == winner_name.lower():
            self.player2.update_result(True)
            self.player1.update_result(False)
        else:
            print("Invalid winner name. No updates made.")

    @staticmethod
    def display_players(players):
        # Visar en lista med alla spelare och deras statistik
        print("\nAvailable players:")
        print(f"{'Number':<10} {'Name':<20} {'Wins':<10} {'Matches':<10} {'Win Percentage':<15}")
        for i, player in enumerate(players):
            print(f"{i + 1:<10} {player.name:<20} {player.wins:<10} {player.matches:<10} {player.win_percentage():.3f}")

    @staticmethod
    def select_player(players, prompt):
        while True:
            try:
                Match.display_players(players)
                index = int(input(prompt)) - 1
                if 0 <= index < len(players):
                    return players[index]
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def sort_players_by_win_percentage(players):
        # Sorterar spelare baserat på vinstprocent
        return sorted(players, key=lambda player: player.win_percentage(), reverse=True)

def main():
    filename = "pd.txt"  # Filnamn som innehåller spelarens data
    try:
        players = Player.read_players_from_file(filename)  # Läser spelare från fil
    except FileNotFoundError:
        print(f"File {filename} not found. Exiting.")
        return

    # Väljer två spelare för en match
    player1 = Match.select_player(players, "\nSelect player 1 by number: ")
    player2 = Match.select_player(players, "\nSelect player 2 by number: ")

    # Låter användaren ange vem som vann matchen
    winner = input(f"\nWho won the match? ({player1.name} or {player2.name}): ").strip()
    match = Match(player1, player2)
    match.update_match_result(winner)  # Uppdaterar statistik för spelarna

    # Sorterar spelarna efter vinstprocent
    players = Match.sort_players_by_win_percentage(players)

    # Visar den uppdaterade rankingen
    print("\nUpdated player rankings:")
    print(f"{'Position':<10} {'Name':<20} {'Wins':<10} {'Matches':<10} {'Win Percentage':<15}")
    for i, player in enumerate(players):
        print(f"{i + 1:<10} {player.name:<20} {player.wins:<10} {player.matches:<10} {player.win_percentage():.3f}")

    # Skriver tillbaka den uppdaterade spelarens data till filen
    Player.write_players_to_file(filename, players)

if __name__ == "__main__":
    main()
