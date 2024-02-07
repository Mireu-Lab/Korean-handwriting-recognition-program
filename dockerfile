FROM tensorflow/tensorflow:nightly-gpu-jupyter

RUN mkdir WorkSpace
WORKDIR WorkSpace

COPY . .

ENV PASSWORD='jupyter1234'

CMD jupyter lab --ip=0.0.0.0 --port=80 --NotebookApp.token=${PASSWORD} --allow-root
