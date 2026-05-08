FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system appgroup \
	&& adduser --system --ingroup appgroup appuser

COPY --chown=appuser:appgroup app.py .

USER appuser:appgroup

EXPOSE 8080

CMD ["python", "app.py"]
