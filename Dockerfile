FROM python:3.11-slim

WORKDIR /app

RUN pip install mlflow pandas scikit-learn psycopg2-binary

COPY mlruns ./mlruns

EXPOSE 1234

CMD ["mlflow","models","serve","-m","/app/mlruns/2/models/m-9bff99f755e6463ea2c824588694466a/artifacts","-p","1234","--host","0.0.0.0","--no-conda"]
