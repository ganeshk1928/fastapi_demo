FROM public.ecr.aws/amazonlinux/amazonlinux:2

# INSTALL APP DEPENDENCIES
RUN yum update -y
RUN yum install -y python3.9 python3.9-devel shadow-utils

RUN yum install -y make gzip tar gcc openssl-devel bzip2-devel libffi-devel shadow-utils

RUN curl -O https://www.python.org/ftp/python/3.9.8/Python-3.9.8.tgz
RUN ls -lh
RUN tar -xvzf Python-3.9.8.tgz
RUN cd Python-3.9.8 && ls -la && ./configure --enable-optimizations && make altinstall
RUN rm -f Python-3.9.8.tgz

RUN groupadd --gid 1000 demouser \
    && useradd --home-dir /home/demouser --create-home --uid 1000 \
    --gid 1000 --shell /bin/bashsh --skel /dev/null demouser && \
    chown -R demouser:demouser /home/demouser

WORKDIR /home/demouser/app

COPY main.py main.py
COPY script.sh script.sh
COPY requirements.txt requirements.txt

RUN pip3.9 install -r requirements.txt

ENV PYTHONPATH='/home/demouser/app'

USER demouser

CMD [ "uvicorn main:app --reload" ]