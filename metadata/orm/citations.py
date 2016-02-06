#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class Citations(PacificaModel):
    product_id = IntegerField(default=-1, primary_key=True)
    article_title = TextField(default="")
    journal_id = IntegerField(default=-1)
    journal_volume = IntegerField(default=-1)
    journal_issue = IntegerField(default=-1)
    page_range = CharField(default="")
    abstract_text = TextField(default="")
    xml_text = TextField(default="")
    pnnl_clearance_id = CharField(default="")
    doi_reference = CharField(default="")

