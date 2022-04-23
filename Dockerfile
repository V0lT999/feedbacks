FROM python:3.7
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install -r requirements.txt
# run app

ENV TOKEN ${TOKEN}

CMD ["python", "main.py"]