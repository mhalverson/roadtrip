This repo will generate an interactive map of my 2018 roadtrip around the USA.

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
* `git clone https://github.com/nationalparkservice/data.git` to download the national park and national monument boundaries
* Check that we have the right folium version installed: `python -c 'import folium; print folium.__version__'` should be `>= 0.5.0+147.gcb3987a`

# Use

* `jupyter notebook master.ipynb` to start a Jupyter Notebook server
* In the Jupyter Notebook, click `Run` and see the interactive map in all its glory
* Run `python main.py` to achieve the following:
  - export the map to a file `rendered_map.html`
  - export the summary data to a file `summary_data.js`
