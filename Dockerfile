FROM python:3.11-slim

# 1) Install Java (OpenJDK) + procps (provides 'ps')
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    procps \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=\"${JAVA_HOME}/bin:${PATH}\"

# Create and switch to the /app working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy your code into /app (including mcp_main.py, mcp_tools.py, etc.)
COPY app/ /app/app
COPY lib/ /app/lib

# Expose port 8000 only if you need it for other reasons
EXPOSE 8000

# Use python to run your MCP server code
CMD [\"python\", \"-u\", \"app/mcp_main.py\"]