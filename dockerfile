FROM tensorflow/tensorflow:nightly-gpu-jupyter

RUN mkdir /workspace
WORKDIR /workspace

COPY . .

ENV PASSWORD='jupyter1234'
RUN mkdir dataset_dir

CMD jupyter lab --ip=0.0.0.0 --port=80 --NotebookApp.token=${PASSWORD} --allow-root
