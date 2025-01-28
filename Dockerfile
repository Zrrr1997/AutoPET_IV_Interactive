#FROM python:3.9-slim
FROM pytorch/pytorch

RUN groupadd -r user && useradd -m --no-log-init -r -g user user

RUN mkdir -p /opt/app /input /output \
    && chown user:user /opt/app /input /output

USER user
WORKDIR /opt/app

ENV PATH="/home/user/.local/bin:${PATH}"

RUN python -m pip install -U pip

COPY --chown=user:user requirements.txt /opt/app/
RUN python -m pip install monailabel
RUN python -m pip install -r requirements.txt


COPY --chown=user:user . /opt/app/sw_infer/
WORKDIR /opt/app/sw_infer/
 
