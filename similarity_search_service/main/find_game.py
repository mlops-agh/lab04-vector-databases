from db.engine import get_engine
from db.models import Games
from repositories.games import find_game


def print_game(game: Games | None) -> None:
    if game is None:
        print("No matching game found")
        return
    print(f"Game: {game.name}")
    print(f"Description: {game.description}")
    print("-" * 10)


def main() -> None:
    engine = get_engine()

    print_game(
        find_game(engine, "This is a game about a hero who saves the world", price=10)
    )
    print_game(find_game(engine, game_description="Home decorating", price=20))
    print_game(find_game(engine, game_description="Home decorating", mac=True, price=5))


if __name__ == "__main__":
    main()
