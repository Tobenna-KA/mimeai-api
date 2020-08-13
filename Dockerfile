#FROM python:3.7.2
#
#ENV FLASK_APP server.py
#
#ENV FLASK_ENV development
#
#WORKDIR /usr/src/app
#
#FROM continuumio/miniconda3
#
#RUN conda create -n env python=3.6
#
#RUN echo "source activate env" > ~/.bashrc
#
#ENV PATH /opt/conda/envs/env/bin:$PATH
#
## copy requirements.txt
#COPY ./requirements.txt /usr/src/app/requirements.txt
#
#COPY . .
#
#RUN pip install --no-cache-dir -r requirements.txt
#
#EXPOSE 5000
#
#CMD ["python", "-m", "flask", "run"]

FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml


# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

COPY . .
RUN pip install -r requirements.txt

# Make sure the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
EXPOSE 5000

CMD ["conda", "run", "-n", "myenv"]
CMD ["conda", "run", "-n", "myenv", "python", "-m", "flask", "run"]