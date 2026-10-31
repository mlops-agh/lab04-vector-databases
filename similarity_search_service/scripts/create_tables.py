from db.engine import get_engine
from db.models import Base


def main() -> None:
    Base.metadata.create_all(get_engine())


if __name__ == "__main__":
    main()
