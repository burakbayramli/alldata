# AllData

All large data that I use for my personal projects.

## Features

* BIST 100, Istanbul Stock Exchange top 100 stock end-of-day closing
  values in CSV files, for years between 2010-2024.

* Data for a couple of blocks from GLOBE elevation data,
  https://www.ngdc.noaa.gov/mgg/topo/gltiles.html.  Sample Javascript
  (Node) code is in `showelev.js`. To run execute `node showelev.js`.
  In order to see how this data can be used via Web, see my Github
  project `burakbayramli.github.com/elev/elev.js`.

* Search index files under `skidx` for my blog under
  https://burakbayramli.github.io/

* SP 500 end-of-day close values in CSV, starting from
  2010. Incremental files are available, we keep this data up-to-date,
  new data for each day go under year/month directory as a seperate
  CSV file. They can be incrementally loaded into the sqlite database
  via a helper function.

Data for both BIST and SP 500 are loaded in to sqlite databas in two
stages, see `bist/bist.py` and `sp500/spy.py` for details. For example
`spy.db_create` will create the initial sqlite database for SP 500
data, `spy.db_load_2010` will load all data under `2010` folder. For
updates a polygon.io api key is needed, place the key in the
appropriate place, and call `spy.get_day` for that day.

In order to load the incremental CSV files into db for a whole month,
we run `spy.db_load_inc` with `year/month` combination passed as
parameters. See the code for examples and further commentary.

## TODO

- An easy way to retrieve BIST 100 daily quote data would be nice.
  Polygon.io has this feature for SP 500, one call a single JSON for
  an entire day for multiple stocks, I have not seen the equivalent
  for BIST. If someone can find it, please load up those CSV files in
  your branch, and submit a PR with the accompanying code, it will be
  merged. Relying on freemium services that require an API key (such
  as polygon.io) is not a problem.
