# Appointments Service Challenge

The below exercise was created as a RESTful API using Flask, SQLAlchemy, and SQLite.  
Validation uses Cerberus.  
Swagger / OpenAPI documentation.

Basic improvements can include:
- Unit tests  
- Stronger validation checks, such as valid meeting times (future, valid start and end), meeting location and time overlap, identification of duplicate person included in meeting, duplicate person or location checks, etc.  
- Addition of model fields, such as date created, last updated, email or other unique person identifier, etc.

## SETUP

Python 3.7.2  
pip 19.2.3

pip install -r requirements.txt
python init_db.py
python run.py

## Background

You're the CEO of a tutoring startup, and you've got a problem. You're normally pretty organized, but it's been
getting more and more difficult to schedule appointments between your tutors and students as your business has grown. You decide
that it's time to leverage some of those fancy web technologies you've been hearing so much about to build a solution to this
problem in the form of an api that you will use to schedule appointments instead of writing them down with pen and paper.

## Requirements

Build a web API that is capable of creating, editing, deleting, and viewing existing Meetings. The inputs to and output of this API
should be json. The API should store these meetings in a relational database of some kind.

### Design

For this service, meetings are defined as an assembly of people, at a physical location, at a particular time. The following 3 model definitions have been defined for you as well in the [swagger.yml](./swagger.yml) file:

- Person
- Location
- Meeting

This was done in order to give you a rough idea of what we expect a "Meeting" object to look like when interacting with the api. Please note though that these objects are deliberately *unfinished* definitions. We leave it to you to decide things like what properties on these models should be required, whether some properties are unnecessary, or if there are properties that should be added. There are (probably) no wrong answers when it comes to design, but we will ask you to explain your design decisions.

#### Documentation

We strongly feel that being able to document your API is an essential part of design work. Filling in the provided [swagger.yml](./swagger.yml) file according to the [OpenAPI 3 specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md) with your endpoints and model changes would be preferred, but if you prefer documenting in some other way, that is also acceptable.

### Technical

- We prefer the use of python to build the web api
- Any relational database may be used for the API (sqlite, mysql, etc.)
- Use of common web and orm frameworks is highly encouraged.
- We expect to be able to run and test your application locally. A docker setup would be preferred, but not required. Please provide
instructions!