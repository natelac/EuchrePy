FROM python:latest
ENV WDIR=/app
WORKDIR ${WDIR}
COPY . ${WDIR}
# Install euchre package locally since not published to PyPI
RUN ["pip3", "install", "."]
EXPOSE 6000/tcp
# Unsure how heartbeats work completely still, assuming needs exposed
EXPOSE 5999/udp
CMD ["euchre-server"]
