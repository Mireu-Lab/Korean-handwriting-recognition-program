FROM tensorflow/tensorflow:nightly-gpu-jupyter

<<<<<<< Updated upstream
RUN mkdir WorkSpace
WORKDIR WorkSpace
=======
RUN mkdir /workspace
WORKDIR /workspace
>>>>>>> Stashed changes

COPY . .

ENV PASSWORD='jupyter1234'
<<<<<<< Updated upstream
=======
RUN mkdir dataset_dir
>>>>>>> Stashed changes

CMD jupyter lab --ip=0.0.0.0 --port=80 --NotebookApp.token=${PASSWORD} --allow-root
