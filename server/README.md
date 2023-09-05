# Python Coding Exercise

## Prerequisites

- python 3.9
- pip
- docker

## Setting up the Server

### Local Execution

```shell
cd server
python -m venv venv
source venv/bin/activate    # linux / mac
.\venv\Scripts\activate    # windows only

pip install -r requirements.txt

cd src
uvicorn main:app --reload
```

### Docker Execution

```shell
docker build -t apiserver .

docker run -p 80:80 -it apiserver
```
