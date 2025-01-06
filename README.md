# AllData

All large data that I use for my personal projects.

* BIST 100, Istanbul Stock Exchange top 100 stock day closing values,
  for years between 2010-2024.

* Data for certain blocks from GLOBE elevation data, https://www.ngdc.noaa.gov/mgg/topo/gltiles.html.
  Sample Javascript (Node) code is in `showelev.js`. To run execute `node showelev.js`

* Search index files for my blog under https://burakbayramli.github.io/

* SP 500 daily close values starting from 2010. This is being kepy up-to-date,
  updates for each day go under year/month directory as a seperate CSV file.


Data for both BIST and SP 500 are loaded in two stages, see `bist/bist.py` and
`sp500/spy.py` for details. For example `spy.db_create` will create the initial
sqlite database, `db_load_2010` will load all data under `2010` folder. For
updates get a Polygon.io key, and call `get_day` for that day. In order to
load the incremental CSV files for a whole month, run `db_load_inc` with
`year/month` combination.