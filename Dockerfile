FROM python:3.11-slim

# 1) Install Java (OpenJDK) + procps (for Spark) and clean up
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    procps \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Set JAVA_HOME so Spark knows where Java is
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# 3) Switch to /app as our working directory
WORKDIR /app

# 4) Copy requirements.txt first so Docker can cache pip installs
COPY requirements.txt /app/

# 5) Install dependencies.
#    Make sure your `requirements.txt` includes:
#    mcp[cli], uvicorn, starlette, pyspark, etc. as needed for your project
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 6) Copy the rest of your code into /app
COPY app/ /app/app
COPY lib/ /app/lib

# 7) Expose port 8000 for SSE/HTTP
EXPOSE 8000

# 8) Run Uvicorn with the module path to your Starlette app
CMD ["uvicorn", "app.mcp_main:app", "--host", "0.0.0.0", "--port", "8000"]