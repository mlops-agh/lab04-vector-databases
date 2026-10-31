import numpy as np
from sqlalchemy.orm import Session

from db.engine import get_engine
from db.models import VECTOR_LENGTH, Images
from repositories.images import find_k_images, insert_images

N = 100
K = 10


def main() -> None:
    engine = get_engine()

    # idempotent: skip seeding if the table already contains images
    with Session(engine) as session:
        if session.query(Images).first() is not None:
            print("Images table is not empty, skipping seeding")
            return

    insert_images(
        engine,
        [(f"image_{i}.jpg", np.random.rand(VECTOR_LENGTH).tolist()) for i in range(N)],
    )

    # Select first image from the table.
    with Session(engine) as session:
        image = session.query(Images).first()

    # Find the 10 most similar images to the first image.
    for similar in find_k_images(engine, K, image):
        print(similar.id, similar.image_path)


if __name__ == "__main__":
    main()
