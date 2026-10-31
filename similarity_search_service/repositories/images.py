from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from db.models import Images


def insert_images(engine: Engine, rows: list[tuple[str, list[float]]]) -> None:
    """Insert many (image_path, image_embedding) rows in a single transaction."""
    with Session(engine) as session:
        session.add_all(
            Images(image_path=path, image_embedding=embedding) for path, embedding in rows
        )
        session.commit()


# Note: pgvector exposes *distances*, not similarities (lower = more similar).
# To rank, sort ascending by `cosine_distance`. To filter by a similarity threshold,
# use `1 - cosine_distance > threshold`.

def find_k_images(engine: Engine, k: int, original_image: Images) -> list[Images]:
    """Order the K images by ascending cosine distance to the first image (smallest distance = most similar)."""
    with Session(engine) as session:
        # execution_options={"prebuffer_rows": True} is used to prebuffer the rows, this is useful when we want to fetch the rows in chunks and return them after session is closed
        result = session.execute(
            select(Images)
            .order_by(Images.image_embedding.cosine_distance(original_image.image_embedding))
            .limit(k),
            execution_options={"prebuffer_rows": True}
        ).scalars().all()
        return result


def find_images_with_similarity_score_greater_than(engine: Engine, similarity_score: float, original_image: Images) -> list[Images]:
    """Find images with similarity to the original above the threshold (similarity = 1 - cosine_distance)."""
    with Session(engine) as session:
        result = session.execute(
            select(Images)
            .filter((1 - Images.image_embedding.cosine_distance(original_image.image_embedding)) > similarity_score),
            execution_options={"prebuffer_rows": True}
        ).scalars().all()
        return result
