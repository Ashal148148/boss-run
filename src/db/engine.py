from sqlalchemy import create_engine

engine = create_engine('sqlite:///test.sqlite', echo=True)