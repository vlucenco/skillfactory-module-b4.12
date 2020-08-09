import sqlalchemy as sa
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)


class Athelete(Base):
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


def connect_db():
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описание таблицы
    Base.metadata.create_all(engine)
    # создаем фибрику сессию
    session = sessionmaker(engine)
    return session()


def request_data():
    return int(input("Введите идентификатор пользователя:"))


def get_closest_athelete_id_by_birthdate(birthdate: str, atheletes: map):
    user_bd = datetime.strptime(birthdate, "%Y-%m-%d")

    bd_map = {}
    for athelete in atheletes:
        bd = datetime.strptime(athelete.birthdate, "%Y-%m-%d")
        bd_map[athelete.id] = bd

    min_date_difference = None
    closest_athelete_id = None
    for key, value in bd_map.items():
        dif = abs(value - user_bd)
        if min_date_difference is None or dif < min_date_difference:
            min_date_difference = dif
            closest_athelete_id = key

    return closest_athelete_id


def find_similar_athletes(user_id):
    session = connect_db()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Пользователь с id %s не найден" % user_id)
    else:
        all_athletes = session.query(Athelete).all()
        birthday_athelete_id = get_closest_athelete_id_by_birthdate(user.birthdate, all_athletes)
        closest_athelete_by_birthdate = session.query(Athelete).filter(Athelete.id == birthday_athelete_id).first()

        closest_athelete_by_height = session.query(Athelete).filter(Athelete.height != "") \
            .order_by(func.abs(Athelete.height - user.height)).first()

        print(
            f"Ближайший атлет по дате рождения: {closest_athelete_by_birthdate.name}, дата рождения - {closest_athelete_by_birthdate.birthdate}")
        print(
            f"Ближайший атлет по росту: {closest_athelete_by_height.name}, рост - {closest_athelete_by_height.height}m")


def main():
    user_id = request_data()
    find_similar_athletes(user_id)


if __name__ == "__main__":
    main()
