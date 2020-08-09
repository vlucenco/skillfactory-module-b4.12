import sqlalchemy as sa
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


def connect_db():
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описание таблицы
    Base.metadata.create_all(engine)
    # создаем фибрику сессию
    session = sessionmaker(engine)
    return session()


def request_data():
    first_name = input("Введите ваше имя: ")
    last_name = input("Введите вашу фамилию: ")
    gender = input("Введите ваш пол. Варианты значений - Male или Female: ")
    email = input("Введите ваш адрес электронной почты: ")
    birthdate = input("Введите ваш день рождения в формате ГГГГ-ММ-ДД: ")
    height = float(input("Введите ваш рост в формате М.СС например, при росте 172см введите 1.72: "))

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )

    return user


def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()

    print("Спасибо, данные сохранены!")


if __name__ == "__main__":
    main()
