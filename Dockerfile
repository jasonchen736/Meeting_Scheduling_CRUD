FROM python:3.6-alpine

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./AppointmentsCRUD AppointmentsCRUD

RUN python AppointmentsCRUD/init_db.py

EXPOSE 5000

CMD cd AppointmentsCRUD && python run.py
