# S5P-PAL

## Official Data Link

Sentinel-5P Product Algorithm Laboratory (S5P-PAL): https://data-portal.s5p-pal.com/

## Usage

The S5P-PAL [official tutorial](https://data-portal.s5p-pal.com/cat-doc) uses PySTAC to download data in a short period. It's useful for case studies.

The Python scripts in the repository support downloading both short-term and long-term TROPOMI NO2 data from S5P-PAL.

### Step 1

Get all the download links and save to one csv file named `s5p_portal_links.csv`.

You only need to install three basic Python packages  (*requests, numpy, and pandas*) to run the script:

```
python fetch_s5p_portal_links.py
```

### Step 2

Change the start_time (`st`) and end_time `et` in `subset_s5p_portal_links.py` and then run another script:

```
python subset_s5p_portal_links.py
```

It will generate a csv file like `{st:yyyymmdd}_{et:yyyymmdd}.csv`.

### Step 3

Let's take `20190601_20190831.csv`as an example.

Just type this line in the terminal to download files in parallel. Please feel free to change `-P <num>` which is for parallel downloading.

```
awk '(NR>1) {print $1, $2}' 20190601_20190831.csv | xargs -n 2 -P 2 wget --no-check-certificate -O
```

## Procedures

In case you're interested in how the scripts work, you can check the comments in `fetch_s5p_portal_links.py`.

## ~ Enjoy your study ~

