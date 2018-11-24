This repo will generate interactive maps of roadtrips.

It was originally developed for my 2018 roadtrip around the USA. It was
slightly generalized for a roadtrip around New Zealand.

# Overview

Powered by [Folium](https://github.com/python-visualization/folium).

Intended for integration into my personal website:
https://github.com/mhalverson/website

# Setup

* `virtualenv env` to create a virtualenv named env that will hold our dependencies in a sandbox
* `. env/bin/activate` to activate the virtualenv
* `pip install -r requirements.txt` to install (most) of the requirements into the virtualenv
* `git clone https://github.com/python-visualization/folium.git` to download the latest version of folium to local
* `cd ./folium; pip install --user -e .; cd ..` to install the necessary development version of folium into our virtualenv
* `cd roadtrip/usa; git clone https://github.com/nationalparkservice/data.git; cd ../..` to download the national park and national monument boundaries
* Check that we have the right folium version installed: `python -c 'import folium; print folium.__version__'` should be `>= 0.5.0+147.gcb3987a`

# Use

* `jupyter notebook usa.ipynb` to start a Jupyter Notebook server
* `PYTHONPATH=. python roadtrip/usa/main.py` to export the map and summary data to files on disk
