FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/src/app
RUN pip install onfleet

# the default command test the onfleet library
CMD [ "python", "test/test_onfleet.py" ]

# Run the image by running: docker-compose up --build
# Watch the test results by docker-compose logs