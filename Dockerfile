FROM python:2-onbuild
EXPOSE 8121
CMD [ "python", "./MetadataServer.py" ]
