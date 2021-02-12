#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
author = Jean-Damien Généro
date = 2021-02-06
"""

from ..app import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

class Type(db.Model):
	__tablename__ = "type"
	typeID = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	typelabel = db.Column(db.Text)
	# subtype = db.relationship("Subtype")
	subtype_tp = db.relationship('Subtype', backref='type')
	
	def __init__(self, typeID, typelabel):
		self.typeID = typeID
		self.typelabel = typelabel

class Subtype(db.Model):
	__tablename__ = "subtype"
	subtypeID = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
	st_label = db.Column(db.Text)
	st_type_fk = db.Column(db.Integer, db.ForeignKey('type.typeID'))
	type_essai = db.relationship('Type', back_populates='subtype_tp')

	def __init__(self, subtypeID, st_label, st_type_fk):
		self.subtypeID = subtypeID
		self.st_label = st_label
		self.st_type_fk = st_type_fk
		
		