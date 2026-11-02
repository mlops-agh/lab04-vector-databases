from sqlalchemy.orm import Session

from db.engine import get_engine
from db.models import Games
from repositories.games import insert_games
from scripts.load_games import load_games

# Embedding is the slow part, keep N small for a quick seed.
N = 100


def main() -> None:
    engine = get_engine()

    with Session(engine) as session:
        if session.query(Games).first() is not None:
            print("Games table is not empty, skipping seeding")
            return

    insert_games(engine, load_games(N))


if __name__ == "__main__":
    main()
