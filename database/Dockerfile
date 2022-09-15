FROM postgres:latest
ENV POSTGRES_PASSWORD=991155
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=test
COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql