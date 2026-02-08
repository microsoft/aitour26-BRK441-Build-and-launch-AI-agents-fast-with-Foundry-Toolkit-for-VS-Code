FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# Set environment variables to bypass SSL verification
ENV PIP_TRUSTED_HOST="pypi.org pypi.python.org files.pythonhosted.org"
ENV PYTHONHTTPSVERIFY=0
ENV REQUESTS_CA_BUNDLE=""
ENV CURL_CA_BUNDLE=""

ENV ENVIRONMENT=container