#Axel Öberg
#P Uppgift

class Player:
    def __init__(self, name, serve_win_prob, wins, matches):
        self.name = name
        self.serve_win_prob = serve_win_prob
        self.wins = wins
        self.matches = matches
        self.games_won = 0

    def win_percentage(self):
        if self.matches > 0:
            return self.wins / self.matches
        else:
            return 0  # Returnera 0 istället för "N/A"
        
    def update_result(self, won):
        self.matches += 1
        if won:
            self.wins += 1
    
    def __str__(self):
        return f"{self.name}\n{self.serve_win_prob}\n{self.wins}\n{self.matches}"
    
    def read_players_from_file(filename):
        players = []
        with open(filename, "r") as f:
            lines = f.read().strip().split("\n")
            for i in range(0, len(lines), 4):
                name = lines[i].strip()
                serve_win_prob = float(lines[i+1].strip())
                wins = int(lines[i+2].strip())
                matches = int(lines[i+3].strip())
                players.append(Player(name, serve_win_prob, wins, matches))
        return players
    
    def write_players_to_file(filename, players):
        with open(filename, "w") as f:
            for player in players:
                f.write(str(player) + "\n")

    def display_players(players):
        print("\nAvailable players:")
        print(f"{'Number':<10} {'Name':<20} {'Wins':<10} {'Matches':<10} {'Win Percentage':<15}")
        for i, player in enumerate(players):
            print(f"{i+1:<10} {player.name:<20} {player.wins:<10} {player.matches:<10} {player.win_percentage():.3f}")


    def select_player(players, prompt):
        while True:
            Player.display_players(players)  # Display players before selection
            index = int(input(prompt)) - 1
            if 0 <= index < len(players):
                return players[index]
            
    def update_match_result(player1, player2, winner_name):
        if player1.name == winner_name:
            player1.update_result(True)
            player2.update_result(False)
        elif player2.name == winner_name:
            player2.update_result(True)
            player1.update_result(False)

    def sort_players_by_win_percentage(players):
        return sorted(players, key=lambda p: p.win_percentage(), reverse=True)

def main():
    filename = "pd.txt"

    # Read players from file
    players = Player.read_players_from_file(filename)

    # Present players and let the user select two
    player1 = Player.select_player(players, "\nSelect player 1 by number: ")
    player2 = Player.select_player(players, "\nSelect player 2 by number: ")

    # Input match winner
    while True:
        winner = input(f"\nWho won the match? ({player1.name} or {player2.name}): ").strip()
        if winner in [player1.name, player2.name]:
            break
        print("Invalid input. Please enter a valid name.")

    # Update player data
    Player.update_match_result(player1, player2, winner)

    # Sort players by win percentage
    players = Player.sort_players_by_win_percentage(players)

    # Display updated rankings
    print("\nUpdated player rankings:")
    print(f"{'Position':<10} {'Name':<20} {'Wins':<10} {'Matches':<10} {'Win Percentage':<15}")
    for i, player in enumerate(players):
        print(f"{i+1:<10} {player.name:<20} {player.wins:<10} {player.matches:<10} {player.win_percentage():.3f}")

    # Save updated player data back to file
    Player.write_players_to_file(filename, players)

if __name__ == "__main__":
    main()    