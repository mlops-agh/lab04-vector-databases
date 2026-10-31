from pgvector.sqlalchemy import Vector
from sqlalchemy import String, Integer, Float, Boolean, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

VECTOR_LENGTH = 512


class Base(DeclarativeBase):
    pass


class Images(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    # path to the image file, used to display the image after similarity search
    image_path: Mapped[str] = mapped_column(String(256))
    # output of the sentence transformer model
    image_embedding: Mapped[list[float]] = mapped_column(Vector(VECTOR_LENGTH))


class Games(Base):
    __tablename__ = "games"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256))

    # `Text` is an unbounded string in Postgres — game descriptions can run a few KB
    description: Mapped[str] = mapped_column(Text)

    windows: Mapped[bool] = mapped_column(Boolean)
    linux: Mapped[bool] = mapped_column(Boolean)
    mac: Mapped[bool] = mapped_column(Boolean)

    price: Mapped[float] = mapped_column(Float)
    game_description_embedding: Mapped[list[float]] = mapped_column(
        Vector(VECTOR_LENGTH)
    )
