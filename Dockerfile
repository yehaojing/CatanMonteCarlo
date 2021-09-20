FROM python:latest

WORKDIR /CatanMonteCarlo

RUN pip install numpy
RUN pip install matplotlib
RUN pip install jupyter

ADD . .

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]