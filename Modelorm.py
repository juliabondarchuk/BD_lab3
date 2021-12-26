import psycopg2 as ps
from random import seed
from random import randint
import numpy as np

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from bs import Base, Session, engine



class Event_category(Base):
    __tablename__ = 'Event category'
    id_category=Column(Integer, primary_key=True)
    name=Column(String)
    parent_category_id=Column(Integer, ForeignKey('Event category.id_category'))
    parent_category = relationship("Event_category")

    def __init__(self, id_category, name, parent_category_id):
        self.id_category = id_category
        self.name = name
        self.parent_category_id = parent_category_id

    def __repr__(self):
        return "{:>5}{:>13}{:>10}" \
            .format(self.id_category, self.name, self.parent_category_id)

class Event(Base):
    __tablename__ = 'Event'
    id_event=Column(Integer, primary_key=True)
    id_category=Column(Integer, ForeignKey('Event category.id_category'))
    performer=Column(String)
    place=Column(String)
    date=Column(Date)
    category= relationship("Event_category")

    def __init__(self, id_event, id_category, performer, place, date):
        self.id_event = id_event
        self.id_category = id_category
        self.performer = performer
        self.place = place
        self.date = date

    def __repr__(self):
        return "{:>10}{:>13}{:>20}{:>30}\t\t{}" \
            .format(self.id_event, self.id_category, self.performer, self.place, self.date)

class Ticket(Base):
    __tablename__ = 'Ticket'
    id_ticket_type=Column(Integer, primary_key=True)
    id_event=Column(Integer, ForeignKey('Event.id_event'))
    name=Column(String)
    price=Column(Integer)
    rest=Column(Integer)
    event = relationship("Event")

    def __init__(self, id_ticket_type, id_event, name, price, rest):
        self.id_ticket_type = id_ticket_type
        self.id_event = id_event
        self.name = name
        self.price = price
        self.rest = rest

    def __repr__(self):
        return "{:>6}{:>13}{:>10}{:>10}{:>10}" \
            .format(self.id_ticket_type, self.id_event, self.name, self.price, self.rest)






class Model:
    def __init__(self):
        #self.con = None
        #self.con = ps.connect(host="localhost", database="postgres", user="postgres", password="123")
        self.session = Session()
        #self.con = engine.connect()


    def get_event(self):
        return self.session.query(Event).order_by(Event.id_event.asc()).all()



    def get_event_category(self):
        return self.session.query(Event_category).order_by(Event_category.id_category.asc()).all()


    def get_ticket(self):
        return self.session.query(Ticket).order_by(Ticket.id_ticket_type.asc()).all()

    def delete_tk(self, table, name, value):
        self.session.query(Ticket).filter_by(id_ticket_type=value).delete()
        self.session.commit()
        return 1

    def delete_ev(self, table, name, value):
        if name!='id_event':
            return 0
        else:
            self.session.query(Ticket).filter_by(id_event=value).delete()
            self.session.query(Event).filter_by(id_event=value).delete()
            self.session.commit()
            return 1

    def check_id_evcat(self, id, name, parent):
        try:
            n=self.session.query(Event_category).filter_by(id_category=id).all()
            nl=len(n)
            return nl
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return -1

    def check_name_evcat(self, id, name1, parent):
        try:
            n=self.session.query(Event_category).filter_by(name=name1).all()
            nl=len(n)
            return nl
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return -1


    def check_parent_evcat(self, id, name, parent):
        if parent==0:
            return 0
        try:
            n=self.session.query(Event_category).filter_by(id_category=parent).all()
            nl=len(n)
            return nl
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return -1


    def insert_event_category(self, id, name, parent):
        try:
            one = Event_category(id_category=id, name=name, parent_category_id=parent)
            self.session.add(one)
            self.session.commit()
            return 1
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0


    def check_id_ev(self, id_ev, id_cat, performer, place, date):
        try:
            n=self.session.query(Event).filter_by(id_event=id_ev).all()
            nl=len(n)
            return nl
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return -1

    def insert_event(self, id_ev, id_cat, performer, place, date):
        try:
            one = Event(id_event=id_ev, id_category=id_cat, performer=performer, place=place, date=date)
            self.session.add(one)
            self.session.commit()
            return 1
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0

    def check_id_tk(self, id_tk, id_ev, name,price,rest):
        try:
            n=self.session.query(Ticket).filter_by(id_ticket_type=id_tk).all()
            nl=len(n)
            return nl
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return -1


    def insert_ticket(self, id_tk, id_ev, name,price,rest):
        try:
            one = Ticket(id_ticket_type=id_tk, id_event=id_ev, name=name, price=price, rest=rest)
            self.session.add(one)
            self.session.commit()
            return 1
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0

    def update_event_category(self, id, name, parent):
        try:
            self.session.query(Event_category).filter_by(id_category=id) \
                .update({Event_category.name: name, Event_category.parent_category_id: parent})
            self.session.commit()
            return 1
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0

    def update_event(self, id_ev, id_cat, performer, place, date):
        try:
            self.session.query(Event).filter_by(id_event=id_ev) \
                .update({Event.id_category: id_cat, Event.performer: performer, Event.place: place, Event.date: date})
            self.session.commit()
            return 1
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0

    def update_ticket(self, id_tk, id_ev, name,price,rest):
        try:
            self.session.query(Ticket).filter_by(id_ticket_type=id_tk) \
                .update({Ticket.id_event: id_ev, Ticket.name: name, Ticket.price: price, Ticket.rest: rest})
            self.session.commit()
            return 1
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0





    def generate_ev_cat(self, n):
        i=int(n)
        while i>0:
            cur=self.con.cursor()
            cur.execute("SELECT MAX(\"id category\") from public.\"Event category\"")
            n=cur.fetchone()
            str=f"INSERT INTO public.\"Event category\" VALUES ({n[0]+1}, chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int), (RANDOM()*({n[0]}-1)+1::integer));"
            cur.execute(str)
            self.con.commit()
            cur.close()
            i=i-1
        return 1
    def check_id_evcat_r(self, id, name, parent):
        cur=self.con.cursor()
        str=f"select count(*) from public.\"Event category\" where \"id category\"={id};"""
        try:
            cur.execute(str)
            n=cur.fetchone()
            cur.close()
            return n[0]
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return -1
    def generate_ev(self, n):
        i=int(n)
        j=1
        while i>0:
            cur=self.con.cursor()
            cur.execute("SELECT MAX(\"id category\") from public.\"Event category\"")
            max_cat=cur.fetchone()
            cur.execute("SELECT MAX(\"id event\") from public.\"Event\"")
            max_ev=cur.fetchone()
            seed(1)
            q=0
            id_cat=0
            while q<=0:
                id_cat=randint(j, max_cat[0])
                q=self.check_id_evcat_r(id_cat, 1, 1)
                j=j+1
            varchar='qwertyuiop'
            str=f"INSERT INTO public.\"Event\" VALUES ({max_ev[0]+1}, {id_cat}, chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int), chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int), timestamp \'2022-01-10 00:00:00\' + random() * (timestamp \'2023-01-20 00:00:00\' - timestamp \'2022-01-10 00:00:00\'));"
            cur.execute(str)
            self.con.commit()
            cur.close()
            i=i-1
        return 1

    def check_id_ev_r(self, id_ev):
        cur=self.con.cursor()
        str=f"select count(*) from public.\"Event\" where \"id event\"={id_ev};"""
        try:
            cur.execute(str)
            n=cur.fetchone()
            cur.close()
            return n[0]
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return -1
    def generate_tk(self, n):
        i=int(n)
        j=1
        while i>0:
            cur=self.con.cursor()
            cur.execute("SELECT MAX(\"id ticket type\") from public.\"Ticket\"")
            max_tk=cur.fetchone()
            cur.execute("SELECT MAX(\"id event\") from public.\"Event\"")
            max_ev=cur.fetchone()
            seed(1)
            q=0
            id_ev=0
            while q<=0:
                id_ev=randint(j, max_ev[0])
                q=self.check_id_ev_r(id_ev)
                j=j+1
            str=f"INSERT INTO public.\"Ticket\" VALUES ({max_tk[0]+1}, {id_ev}, chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int), (RANDOM()*(1000-100)+100::integer), (RANDOM()*(500-5)+5::integer));"
            cur.execute(str)
            self.con.commit()
            cur.close()
            i=i-1
        return 1
    def search1(self,t1, a1, str1,t2, a2, max2, min2, t3,a3,str3,key):
        cur=self.con.cursor()
        str=f"select * from public.\"{t1}\" as one inner join public.\"{t3}\" as two on one.\"{key}\"=two.\"{key}\" where one.{a1} LIKE \'{str1}\' and {min2}<one.{a2} and one.{a2}<{max2} and two.{a3} LIKE \'{str3}\'"
        print(str)
        try:
            cur.execute(str)
            rows = cur.fetchall()
            cur.close()
            return rows
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0
    def search2(self, t1, a1, max1, min1,t2, a2, max2, min2, t3,a3,dt31,dt32,key):
        cur=self.con.cursor()
        str=f"select * from public.\"{t1}\" as one inner join public.\"{t3}\" as two on one.\"{key}\"=two.\"{key}\" where {min1}<one.{a1} and one.{a1}<{max1} and {min2}<one.{a2} and one.{a2}<{max2} and two.{a3} BETWEEN \'{dt31}\' AND \'{dt32}\'"
        print(str)
        try:
            cur.execute(str)
            rows = cur.fetchall()
            cur.close()
            return rows
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0
    def search3(self, t1, a1, str1,t2, a2, str2, t3,a3,max3, min3,key, key2):
        cur=self.con.cursor()
        str=f"select * from public.\"{t1}\" as one inner join public.\"{t2}\" as two on one.\"{key}\"=two.\"{key}\" inner join public.\"{t3}\" as three on two.\"{key2}\"=three.\"{key2}\" where one.{a1} LIKE \'{str1}\' and two.{a2} LIKE \'{str2}\' and {min3}<three.{a3} and three.{a3}<{max3}"
        print(str)
        try:
            cur.execute(str)
            rows = cur.fetchall()
            cur.close()
            return rows
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            return 0
