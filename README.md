# weather_data
Scripts of downloading weather data (satellite and reanalysis data)

## Himawari-8 (L2)

### Links

Registration Link: <https://www.eorc.jaxa.jp/ptree/registration_top.html>

FTP: <ftp://ftp.ptree.jaxa.jp/>

### Structure

Remote directory structure:

```
/pub/himawari
    +---/L2
        +---/[PRODUCT]
            +---/[VER]
                +---/[YYYYMM]
                    +---/[DD]
                        +---/[hh]
```

Local directory structure:

```
/<save_path>
    +---/L2
        +---/[PRODUCT]
            +---/[VER]
                +---/[YYYYMM]
                    +---/[DD]
                        +---/[hh]
```

### Supported L2 products

- Aerosol Property (ARP)
- Photosynthetically Available Radiation(PAR)
- Cloud Property (CLP)

### Usage

Check the help information

```
python h8_l2.py --help
```

```
Usage: h8_l2.py [OPTIONS]

  Fuctions:
      Download Himawari-8 Level 2 products from JAXA and save to directories
  Contact:
      xinzhang1215@gmail.com

Options:
  -s, --save_path TEXT         Directory where you want to save files.
                               [default: ./data/H8/]

  -sd, --sdate TEXT            Beginning date of downloaded files YYYY-MM-
                               DD_hh:mm

  -ed, --edate TEXT            Ending date of downloaded files YYYY-MM-
                               DD_hh:mm

  -ts, --tstep INTEGER         Time step (min) between files  [default: 10]
  -p, --product [ARP|CLP|PAR]  Product name in Capital. ARP, CLP or PAR
                               [default: CLP]

  -u, --username TEXT          Username
  -pwd, --password TEXT        Password
  -d, --debug INTEGER          Debug level  [default: 0]
  --help                       Show this message and exit.
```

### Example

```
python h8_l2.py -p CLP -sd <YYYY-MM-DD_HH:MM> -ed <YYYY-MM-DD_HH:MM> -u <username> -pwd <password>
```

