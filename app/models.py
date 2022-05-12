import json
from sqlite3 import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from app import db


cd_band = db.Table('cd_band',
    db.Column('cd_id', db.Integer, db.ForeignKey('cd.id'), primary_key=True),
    db.Column('band_id', db.Integer, db.ForeignKey('band.id'), primary_key=True)
)


class Band(db.Model):
    __tablename__ = 'band'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


    def get_as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}#{ "id": self.id, "name": self.name }


class CD(db.Model):
    __tablename__ = 'cd'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    bands = db.relationship('Band', secondary=cd_band, lazy='subquery',
         backref=db.backref('cds', lazy=True))

    def get_as_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}# { "id": self.id, "title": self.title, "year": self.year, "bands": self.bands }
        d['bands'] =  list(x.get_as_dict() for x in self.bands)

        return d


class DbCdLibrary:
    def all_bands(self):
        result = Band.query.all()
        result = map(lambda x: x.get_as_dict(), result)
        result = list(result)
        return result

    def create_band(self, name):
        band = Band()
        band.name = name

        """Save an instance of the model from the database."""
        try:
            db.session.add(band)
            db.session.commit()     
        except IntegrityError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise
        return band.get_as_dict()

    def get_band_by_name(self, band_name):
        return Band.query.filter(Band.name == band_name).first()




    def all(self):
        allcds = CD.query.all()

        return list(x.get_as_dict()  for x in allcds )

    def get(self, id):
        cd = CD.query.filter(CD.id == id).first()
        return cd.get_as_dict()

    def create(self, title, year, band_ids):
        cd = CD()
        cd.title = title
        cd.year = year

        bands = Band.query.filter(Band.id.in_(band_ids)).all()

        cd.bands.extend(bands)

        try:
            db.session.add(cd)
            db.session.commit()     
        except IntegrityError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise
        result = cd.get_as_dict()
        return result

    def search_by_name(self, match):
        allcds = CD.query.filter(CD.name.ilike(match)).all()
        return list(x.get_as_dict()  for x in allcds )

    def update(self, id, title, year, bands):
        item = CD.query.filter(CD.id == id).first()
        if item:
            if title:
                item.title = title
            if year:
                item.year = year
            #todo: bands
            db.session.commit()

            return item.get_as_dict()
        return None

    def delete(self, id):
        cd = CD.query.filter(CD.id == id).first()
        if cd:
            db.session.delete(cd)
            db.session.commit()
            return cd.get_as_dict()
        return None


