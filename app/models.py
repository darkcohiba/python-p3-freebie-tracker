#!/usr/bin/env python3

from sqlalchemy import (Column, String, Integer, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///freebies.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name= Column(String())
    value = Column(Integer())
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', back_populates='freebies')
    dev_id = Column(Integer, ForeignKey('devs.id'))
    dev = relationship('Dev', back_populates='freebies')

    def __repr__(self):
        return f'<Freebie {self.item_name}, {self.value}, {self.dev.name}, {self.company.name}>'
    
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}.'
    

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    # Relationship with Freebie
    freebies = relationship('Freebie', back_populates='company')


    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, company_id=self.id, dev_id=dev.id)
        session.add(freebie)
        session.commit()
        session.close()
        return freebie
    
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()
    

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    # Relationship with Freebie
    freebies = relationship('Freebie', back_populates='dev')

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False