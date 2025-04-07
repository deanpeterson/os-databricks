FROM python:3.11-slim

# 1) Install Java (OpenJDK) + procps (for 'ps'), then cleanup
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

# ------------------------------------------------------------------------
# 4A) Option A: Add mcp[cli] to your requirements.txt
#
#    If your requirements.txt already includes this line:
#    mcp[cli]
#    then a single pip install command is enough:
#
# RUN pip install --upgrade pip && pip install -r requirements.txt
#
# ------------------------------------------------------------------------
# 4B) Option B: Install your existing requirements + mcp[cli] in one go
#    (if you do NOT want to modify requirements.txt directly).
#    In that case, do:
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install "mcp[cli]"
# ------------------------------------------------------------------------

# 5) Copy your application code (including mcp_main.py) into /app
COPY app/ /app/app
COPY lib/ /app/lib

# 6) Expose port 8000 ONLY if you need it for something else.
#    MCP typically runs on stdio or SSE, so you might not need this.
EXPOSE 8000

# 7) Run your MCP server code
CMD ["python", "-u", "-m", "app.mcp_main"]
