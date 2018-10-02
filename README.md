This repo will generate an interactive map of my 2018 roadtrip around the USA.

# Overview

Powered by [Folium](https://github.com/python-visualization/folium).

# Setup

* `virtualenv env` to create a virtualenv named env that will hold our dependencies in a sandbox
* `. env/bin/activate` to activate the virtualenv
* `pip install -r requirements.txt` to install (most) of the requirements into the virtualenv
* `git clone https://github.com/python-visualization/folium.git` to download the latest version of folium to local
* `cd ./folium; pip install --user -e .; cd ..` to install the necessary development version of folium into our virtualenv
* `git clone https://github.com/nationalparkservice/data.git` to download the national park and national monument boundaries
* Check that we have the right folium version installed: `python -c 'import folium; print folium.__version__'` should be `>= 0.5.0+147.gcb3987a`

# Use

* `jupyter notebook master.ipynb` to start a Jupyter Notebook server
* In the Jupyter Notebook, click `Run` and see the interactive map in all its glory
* Export the map to a file by the following means:
  - uncomment the line `m.save(...)` in the Notebook OR
  - run `python main.py <filename>` in the shell
