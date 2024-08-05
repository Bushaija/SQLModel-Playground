import sqlmodel as sql 

class Team(sql.SQLModel, table=True):
    id: int | None = sql.Field(default = None, primary_key=True)
    name: str = sql.Field(index=True)
    headquarters: str

class Hero(sql.SQLModel, table=True):
    id: int | None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    secret_name: str
    age: int | None = sql.Field(default = None, index=True)
    team_id: int | None = sql.Field(default=None, foreign_key="team.id")

# create db engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = sql.create_engine(sqlite_url, echo=False)

# create db and tables
def create_db_and_tables():
    sql.SQLModel.metadata.create_all(engine)

# Code above omitted 👆
def create_heroes():
    with sql.Session(engine) as session:
        team_preventers = Team(name="preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            team_id=team_z_force.id
        )
        hero_spider_boy = Hero(
            name="Spider-Boy",
            secret_name="Pedro Parqueador",
            team_id=None
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id
        )
        session.add(hero_deadpond)
        session.add(hero_spider_boy)
        session.add(hero_rusty_man)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_spider_boy)
        session.refresh(hero_rusty_man)

        print("Created hero: ", hero_deadpond)
        print("Created hero: ", hero_rusty_man)
        print("Created_hero: ", hero_spider_boy)





# select all heroes
def select_heroes():
    with sql.Session(engine) as session:
        statement = sql.select(Hero,Team).join(Team, isouter=True)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero: ", hero, "Team: ", team)

# select a limited number of heroes
def select_limited_heroes():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)

# select an offsetted limited heroes
def select_offset_limited_heroes():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).offset(3).limit(3)
        results = session.exec(statement).all()
        print("Heroes: ", results)

# exactly one hero
def get_exactly_one_hero():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        print("unique hero: ", results.one())

# .get()
def get_hero_by_id():
    with sql.Session(engine) as session:
        hero = session.get(Hero, 1)
        print(hero)

'''
    .get(): method of session object
    .one() and .first(): methods of session.exec() returned object
        - session.get(Model_object, _id)
        - session.exec(statement).one()
        - session.exec(statment).first()
'''


# filter user
def filter_hero():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).where(sql.col(Hero.age) == 48)
        results = session.exec(statement)
        print([result for result in results])

# list of hero object
def list_hero_object():
    with sql.Session(engine) as session:
        statement = sql.select(Hero)
        results = session.exec(statement).all()
        print(results)

# update some heroes
def update_hero():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        hero.age = 17
        session.add(hero)
        session.commit()
        session.refresh(hero)
        print(hero)

# delete hero
def delete_hero():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print("Deleted hero: ", hero)
        session.delete(hero)
        session.commit()

        statement = sql.select(Hero).where(Hero.name == "Spider-Boy")
        hero = session.exec(statement).first()
        if hero is None:
            print("There's not hero named: Spider-Body")

def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()
    #select_limited_heroes()
    #select_offset_limited_heroes()
    #update_hero()
    #delete_hero()

if __name__ == "__main__":
    main()
