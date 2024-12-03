class Player:
    # Konstruktor för att skapa en spelare med attribut: namn, servevinstprocent, antal vinster och matcher
    def __init__(self, name, serve_win_prob, wins, matches):
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches
        self.games_won = 0  # Extra attribut för framtida användning (just nu oanvänt)

    # Beräknar spelarens vinstprocent
    def win_percentage(self):
        if self.matches > 0:
            return self.wins / self.matches  # Om matcher spelats, returnera vinstprocent
        else:
            return 0  # Om inga matcher spelats, returnera 0 istället för "N/A"

    # Uppdaterar spelarens matchdata efter en match (om spelaren vunnit eller inte)
    def update_result(self, won):
        self.matches += 1  # Öka antalet spelade matcher
        if won:
            self.wins += 1  # Öka antalet vinster om spelaren vann

    # Returnerar en strängrepresentation av spelaren för enkel filhantering
    def __str__(self):
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"

    # Läser in spelare från en fil och skapar Player-objekt för varje spelare
    @staticmethod
    def read_players_from_file(filename):
        players = []
        with open(filename, "r") as f:
            lines = f.read().strip().split("\n")  # Läs alla rader i filen
            for i in range(0, len(lines), 4):  # Varje spelare representeras av 4 rader
                name = lines[i].strip()
                serve_win_prob = float(lines[i + 1].strip())
                wins = int(lines[i + 2].strip())
                matches = int(lines[i + 3].strip())
                players.append(Player(name, serve_win_prob, wins, matches))  # Skapa en ny spelare och lägg till i listan
        return players

    # Skriver tillbaka alla spelares data till en fil
    @staticmethod
    def write_players_to_file(filename, players):
        with open(filename, "w") as f:
            for player in players:
                f.write(str(player) + "\n")  # Skriv varje spelares strängrepresentation till filen

    # Visar en lista med alla tillgängliga spelare i ett tabellformat
    @staticmethod
    def display_players(players):
        print("\nAvailable players:")
        print(f"{'Number':<10} {'Name':<20} {'Wins':<10} {'Matches':<10} {'Win Percentage':<15}")
        for i, player in enumerate(players):
            print(f"{i + 1:<10} {player.name:<20} {player.wins:<10} {player.matches:<10} {player.win_percentage():.3f}")

    # Låter användaren välja en spelare från listan
    @staticmethod
    def select_player(players, prompt):
        while True:
            Player.display_players(players)  # Visa listan över spelare
            try:
                index = int(input(prompt)) - 1  # Fråga användaren om ett index
                if 0 <= index < len(players):  # Kontrollera att valet är giltigt
                    return players[index]  # Returnera vald spelare
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    # Uppdaterar resultaten för båda spelarna efter en match
    @staticmethod
    def update_match_result(player1, player2, winner_name):
        if player1.name == winner_name:  # Om spelare 1 vann
            player1.update_result(True)
            player2.update_result(False)
        elif player2.name == winner_name:  # Om spelare 2 vann
            player2.update_result(True)
            player1.update_result(False)

    # Sorterar spelare efter vinstprocent i fallande ordning
    @staticmethod
    def sort_players_by_win_percentage(players):
        return sorted(players, key=lambda p: p.win_percentage(), reverse=True)


def main():
    filename = "pd.txt"  # Filnamnet där spelardata sparas

    # Läs in spelare från fil
    players = Player.read_players_from_file(filename)

    # Låt användaren välja två spelare för en match
    player1 = Player.select_player(players, "\nSelect player 1 by number: ")
    player2 = Player.select_player(players, "\nSelect player 2 by number: ")

    # Fråga användaren vem som vann matchen
    while True:
        winner = input(f"\nWho won the match? ({player1.name} or {player2.name}): ").strip()
        if winner in [player1.name, player2.name]:  # Kontrollera att användaren skrev in ett giltigt namn
            break
        print("Invalid input. Please enter a valid name.")

    # Uppdatera matchresultaten för de två spelarna
    Player.update_match_result(player1, player2, winner)

    # Sortera spelarna baserat på deras uppdaterade vinstprocent
    players = Player.sort_players_by_win_percentage(players)

    # Visa den uppdaterade rankingen
    print("\nUpdated player rankings:")
    print(f"{'Position':<10} {'Name':<20} {'Wins':<10} {'Matches':<10} {'Win Percentage':<15}")
    for i, player in enumerate(players):
        print(f"{i + 1:<10} {player.name:<20} {player.wins:<10} {player.matches:<10} {player.win_percentage():.3f}")

    # Skriv tillbaka den uppdaterade datan till filen
    Player.write_players_to_file(filename, players)


if __name__ == "__main__":
    main()  # Starta programmet
