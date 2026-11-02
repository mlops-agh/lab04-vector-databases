from typing import Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from tqdm import tqdm

from db.models import Games
from embeddings.embedder import generate_embeddings

BATCH_SIZE = 100


def insert_games(engine: Engine, dataset) -> None:
    with Session(engine) as session:
        pending = 0
        for game in tqdm(dataset):
            description = game["detailed_description"] or ""
            # windows/linux/mac are platform flags (True/False), not missing-data signals:
            # don't gate the insert on them or you discard most of the dataset
            if not (game["name"] and description and game["price"] is not None):
                continue

            session.add(
                Games(
                    name=game["name"],
                    description=description,
                    windows=game["windows"],
                    linux=game["linux"],
                    mac=game["mac"],
                    price=game["price"],
                    game_description_embedding=generate_embeddings(description),
                )
            )
            pending += 1
            if pending == BATCH_SIZE:
                session.commit()
                pending = 0
        session.commit()


def find_game(
    engine: Engine,
    game_description: str,
    windows: Optional[bool] = None,
    linux: Optional[bool] = None,
    mac: Optional[bool] = None,
    price: Optional[float] = None,
) -> Optional[Games]:
    game_embedding = generate_embeddings(game_description)

    query = select(Games).order_by(
        Games.game_description_embedding.cosine_distance(game_embedding)
    )

    # `is not None`, not truthiness: price=0 means "free games only"
    if price is not None:
        query = query.filter(Games.price <= price)
    if windows:
        query = query.filter(Games.windows.is_(True))
    if linux:
        query = query.filter(Games.linux.is_(True))
    if mac:
        query = query.filter(Games.mac.is_(True))

    with Session(engine) as session:
        return session.execute(
            query.limit(1), execution_options={"prebuffer_rows": True}
        ).scalar_one_or_none()
