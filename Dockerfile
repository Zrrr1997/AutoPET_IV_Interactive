FROM pytorch/pytorch

RUN groupadd -r algorithm && useradd -m --no-log-init -r -g algorithm algorithm

RUN mkdir -p /opt/algorithm /input /output /output/images/tumor-lesion-segmentation \
    && chown -R algorithm:algorithm /opt/algorithm /input /output

USER algorithm
WORKDIR /opt/algorithm

ENV PATH="/home/algorithm/.local/bin:${PATH}"

RUN python -m pip install --user -U pip

COPY --chown=algorithm:algorithm requirements.txt /opt/algorithm/
RUN python -m pip install monailabel
RUN python -m pip install -r requirements.txt

COPY --chown=algorithm:algorithm . /opt/algorithm/sw_infer/

WORKDIR /opt/algorithm/sw_infer/

ENTRYPOINT ["python", "-m", "process"]
 
