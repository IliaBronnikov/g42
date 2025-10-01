FROM python:3.13-slim

WORKDIR /app

COPY normalize_contacts.py /app/
COPY input_data.csv /app/

RUN pip install --no-cache-dir phonenumbers dateparser

CMD ["python", "normalize_contacts.py"]