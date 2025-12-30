FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget unzip nmap && rm -rf /var/lib/apt/lists/*

# Install security tools
RUN wget -q https://github.com/projectdiscovery/nuclei/releases/download/v3.1.0/nuclei_3.1.0_linux_amd64.zip \
    && unzip nuclei_3.1.0_linux_amd64.zip && mv nuclei /usr/local/bin/ && rm *.zip

RUN wget -q https://github.com/projectdiscovery/subfinder/releases/download/v2.6.3/subfinder_2.6.3_linux_amd64.zip \
    && unzip subfinder_2.6.3_linux_amd64.zip && mv subfinder /usr/local/bin/ && rm *.zip

RUN wget -q https://github.com/projectdiscovery/httpx/releases/download/v1.3.7/httpx_1.3.7_linux_amd64.zip \
    && unzip httpx_1.3.7_linux_amd64.zip && mv httpx /usr/local/bin/ && rm *.zip

WORKDIR /app
COPY workers/replit_worker.py /app/main.py
RUN pip install flask requests urllib3

EXPOSE 8080
CMD ["python", "main.py"]
