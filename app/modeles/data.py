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
	mono_fk = db.Column(db.Integer, db.ForeignKey('monography.monoID'))
	type_essai = db.relationship('Type', back_populates='subtype_tp')
	mono_essai = db.relationship('Monography', back_populates='subtype_mono')

	def __init__(self, subtypeID, st_label, st_type_fk):
		self.subtypeID = subtypeID
		self.st_label = st_label
		self.st_type_fk = st_type_fk

class Monography(db.Model):
	__tablename__ = "monography"
	monoID = db.Column(db.Text, unique=True, nullable=False, primary_key=True)
	filename = db.Column(db.Text)
	monotitle = db.Column(db.Text)
	subtype_mono = db.relationship('Subtype', backref='subtype')

	def __init__(self, monoID, filename, monotitle):
		self.monoID = monoID
		self.filename = filename
		self.monotitle = monotitle

class Inventory(db.Model):
	__tablename__ = "inventory"
	inventoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
	inventoryTXT = db.Column(db.Text)
	inventory_mono = db.Column(db.Integer)
	inventory_type = db.Column(db.Integer)
	inventory_subtype = db.Column(db.Text)

	def __init__(self, inventoryID, inventoryTXT, inventory_mono, inventory_type, inventory_subtype):
		self.inventoryID = inventoryID
		self.inventoryTXT = inventoryTXT
		self.inventory_mono = inventory_mono
		self.inventory_type = inventory_type
		self.inventory_subtype = inventory_subtype

