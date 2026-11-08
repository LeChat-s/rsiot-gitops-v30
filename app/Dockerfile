FROM python:3.12-alpine
ARG VCS_REF=dev
LABEL org.opencontainers.image.source="https://github.com/LeChat-s/rsiot-gitops-v30"
LABEL org.opencontainers.image.title="SmartHome rules"
ENV PYTHONUNBUFFERED=1 PORT=8110 APP_VERSION=${VCS_REF}
WORKDIR /app
RUN adduser -D -u 10001 app
COPY --chown=app:app server.py /app/server.py
USER 10001
EXPOSE 8110
CMD ["python", "-u", "server.py"]
