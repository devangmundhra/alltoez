__author__ = 'devangmundhra'

from django.conf import settings

from py2neo import ServiceRoot, Relationship, Node

_neo4j_url = settings.NEO4J_URL
neo4j_graph = ServiceRoot(_neo4j_url).graph