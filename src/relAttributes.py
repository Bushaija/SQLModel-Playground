import sqlmodel as sql

class Team(sql.SQLModel, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    headquarters: str
    heroes: list["Hero"] = sql.Relationship(back_populates="team")

class Hero(sql.SQLModel, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    secret_name: str
    age: int|None = sql.Field(default=None, index=True)
    team_id: int|None = sql.Field(default=None, foreign_key="team.id")
    team: Team|None = sql.Relationship(back_populates="heroes")

# setup the db engine
sqlite_file_name="database2.db"
sqlite_url=f"sqlite:///{sqlite_file_name}"
engine = sql.create_engine(sqlite_url, echo=False)

# create db and tables
def create_db_tables():
    sql.SQLModel.metadata.create_all(engine)

# create heros
def create_heroes_v1():
    with sql.Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id)
        hero_rusty = Hero(name="Rusty-man", secret_name="Tommy Sharp", age=48, team_id=team_preventers.id)
        hero_spider=Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty)
        session.add(hero_spider)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty)
        session.refresh(hero_spider)

        print("Created hero: ", hero_deadpond)
        print("Created hero: ", hero_rusty)
        print("Created hero: ", hero_spider)

# create instance with relationship attributes
def create_heroes_v2():
    with sql.Session(engine) as session:
         team_preventers = Team(
             name="Preventers",
             headquarters="Sharp Tower"
         )
         team_z_force = Team(
             name="Z-Force",
             headquarters="Sister Margaret's Bar"
         )

         hero_deadpond = Hero(
             name="Deadpond",
             secret_name="Dive Wilson",
             team=team_preventers
         )
         hero_rusty = Hero(
             name="Rusty-Man",
             secret_name="Tommy Sharp",
             team=team_preventers
         )
         hero_spider = Hero(
             name="Spider-Boy",
             secret_name="Pedro Parqueador",
             team=team_z_force
         )
         session.add(hero_deadpond)
         session.add(hero_rusty)
         session.add(hero_spider)
         session.commit()

         session.refresh(hero_deadpond)
         session.refresh(hero_rusty)
         session.refresh(hero_spider)
         
         print("Created hero:", hero_deadpond)
         print("Created hero:", hero_rusty)
         print("Created hero:", hero_spider)

def create_heroes_v3():
    with sql.Session(engine) as session:
        hero_black_lion = Hero(
            name="Black Lion",
            secret_name="Trevor Challa",
            age=35
        )
        hero_sure_e = Hero(
            name="Princess Sure-E",
            secret_name="Sure-E",
        )

        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e]
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print("Team Wakaland: ", team_wakaland)

def select_hero():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_spider = results.one()
        print("hero_spider: ", hero_spider)

def select_hero_team():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_spider = results.one()
        print("Spider's team: ", hero_spider.team)

# get a list of relationship objects
def select_list_heroes():
    with sql.Session(engine) as session:
        statement = sql.select(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        team_preventers = results.one()
        print("Preventers heros", team_preventers.heroes)

# remove relationships
def update_heroes():
    with sql.Session(engine) as session:
        statement = sql.select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_spider =results.one()
        hero_spider.team_id = None
        session.add(hero_spider)
        session.commit()
        session.refresh(hero_spider)
        print("Spider-Boy without team: ", hero_spider)
        


def main():
    #create_db_tables()
    #create_heroes_v1()
    #create_heroes_v2()
    #create_heroes_v3()
    #select_hero_team()
    #select_list_heroes()
    update_heroes()

if __name__ == "__main__":
    main()
