# Blitzortung

## Links

https://www.blitzortung.org/

## Supported images

[Historical Maps](https://www.blitzortung.org/en/historical_maps.php)

## Usage

Check the help information

```
python blitzortung.py --help
```

```
Usage: blitzortung.py [OPTIONS]

  Fuctions:
      Scarping lightning location images from Blitzortung and overlay on background image
  Contact:
      xinzhang1215@gmail.com

Options:
  -s, --save_path TEXT            Directory where you want to save figures.
                                  [default: ./figs/]

  -sd, --sdate TEXT               Beginning date of downloaded files YYYY-MM-
                                  DD_hh:mm

  -ed, --edate TEXT               Ending date of downloaded files YYYY-MM-
                                  DD_hh:mm

  -r, --region [earth|eu|oc|us|as|sa|af]
                                  Region name of lightning view.
                                  
                                  'earth': Overview map
                                  
                                  'eu': Europe
                                  
                                  'oc': Oceania
                                  
                                  'us': North America
                                  
                                  'as': Asia
                                  
                                  'sa': South America
                                  
                                  'af': Africa   [default: earth]

  --help                          Show this message and exit.
```

