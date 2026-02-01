# base image
#gives us python (slim = lightweight)
FROM --platform=linux/amd64 python:3.11-slim

# set working directory inside container
#so that all commands run inside /app
WORKDIR /app

#copy dependency file
#faster rebuilds in code changes
COPY requirements.txt .

#install dependencies(fastapi, sqlalchemy..etc)
RUN pip install --no-cache-dir -r requirements.txt

#copy app code
COPY . .

#expose fastapi port
#tells docker this app listens on port 8000
EXPOSE 8000

#run the app
#starts fastapi

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


