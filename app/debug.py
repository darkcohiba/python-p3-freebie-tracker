#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

    company = Company(name="Flatiron", founding_year=2025)
    session.add(company)
    session.commit()

    company2 = Company(name="Acre", founding_year=2005)
    session.add(company2)
    session.commit()

    company3 = Company(name="Thirma", founding_year=2012)
    session.add(company3)
    session.commit()

    dev = Dev(name="Alice")
    session.add(dev)
    session.commit()

    dev2 = Dev(name="Ninfa")
    session.add(dev2)
    session.commit()

    freebie = Freebie(item_name="T-shirt", value=10, company_id=company.id, dev_id=dev.id)
    session.add(freebie)
    session.commit()

    oldest = Company.oldest_company(session)
    print(oldest)

    company.give_freebie( dev, "T-shirt", 10)
    company.give_freebie( dev, "Mug", 5)

    # print(dev.received_one("T-shirt"))  #  True
    # print(dev.received_one("Mug"))  #  True
    # print(dev.received_one("Sticker"))  # False


    print(dev.give_away(dev2, freebie))  # True
    print(dev.give_away(dev2, freebie))  # False

    companies = session.query(Company).all()
    for company in companies:
        print(company)

    devs = session.query(Dev).all()
    for dev in devs:
        print(dev)

    freebies = session.query(Freebie).all()
    for freebie in freebies:
        print(freebie)

    session.close()
    # import ipdb; 
    # ipdb.set_trace()
