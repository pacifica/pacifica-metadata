FROM python:2-onbuild
EXPOSE 8080
CMD [ "python", "./MetadataServer.py" ]
