FROM python:3.11-slim

# 1) Install Java (OpenJDK) + procps (provides 'ps')
#    and clean up apt cache to minimize image size
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    procps \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Set JAVA_HOME environment variable so Spark knows where Java is
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Create and switch to the /app working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy the entire 'app' folder into /app/app
COPY app /app/app
COPY lib/ /app/lib

# Expose the port for the FastAPI app
EXPOSE 8000

# Run your FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
