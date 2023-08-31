from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

from sqlalchemy import ForeignKey, relationship

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    def __repr__(self):
        return f'<Company {self.name}>'

    # Relationship to Freebies
    freebies = relationship('Freebie', back_populates='company')

    # Relationship to Devs (many-to-many)
    devs = relationship('Dev', secondary='freebies', back_populates='companies')

    
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(dev=dev, company=self, item_name=item_name, value=value)
        return new_freebie

    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f'<Dev {self.name}>'

    # Relationship to Freebies
    freebies = relationship('Freebie', back_populates='dev')

    # Relationship to Companies (many-to-many)
    companies = relationship('Company', secondary='freebies', back_populates='devs')
    
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    # ForeignKey to Dev
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    dev = relationship('Dev', back_populates='freebies')

    # ForeignKey to Company
    company_id = Column(Integer(), ForeignKey('companies.id'))
    company = relationship('Company', back_populates='freebies')

    
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'