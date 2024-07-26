FROM spark:3.5.1-scala2.12-java17-ubuntu

USER root

RUN set -ex; \
    apt-get update; \
    apt-get install -y python3 python3-pip; \
    rm -rf /var/lib/apt/lists/*

# Install app dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

USER spark

# Copy app code
COPY . .

# Execute the python code
CMD ["python3", "main.py"]