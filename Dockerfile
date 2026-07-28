FROM python:3.11-slim

WORKDIR /app

RUN pip install mlflow pandas scikit-learn psycopg2-binary

COPY mlruns ./mlruns

EXPOSE 1234

CMD ["mlflow","models","serve","-m","/app/mlruns/1/models/m-2a4c27becbe64ac2b4e509ac2a34c155/artifacts","-p","1234","--host","0.0.0.0","--no-conda"]
