# 1. Himawari-8 (JAXA)

## Links

Registration Link: <https://www.eorc.jaxa.jp/ptree/registration_top.html>

FTP: <ftp://ftp.ptree.jaxa.jp/>

## Supported products

### L1

- Full-Disk (2 km and 5 km)

### L2

- Aerosol Property (ARP)
- Photosynthetically Available Radiation(PAR)
- Cloud Property (CLP)

## Usage

Check the help information

```
python h8_JAXA.py --help
```

```
Usage: h8_JAXA.py [OPTIONS]

  Fuctions:
      Download Himawari-8 Level 1 and Level 2 products from JAXA and save to directories
  Contact:
      xinzhang1215@gmail.com

Options:
  -s, --save_path TEXT            Directory where you want to save files.
                                  [default: ./data/H8/]

  -sd, --sdate TEXT               Beginning date of downloaded files YYYY-MM-
                                  DD_hh:mm

  -ed, --edate TEXT               Ending date of downloaded files YYYY-MM-
                                  DD_hh:mm

  -ts, --tstep INTEGER            Time step (min) between files  [default: 10]
  -p, --product [L1|ARP|CLP|PAR]  Product name in Capital. L1, ARP, CLP or PAR
                                  [default: L1]

  -r, --resolution [2km|5km]      Resolution of the L1 product. 2km or 5km
                                  [default: 5km]

  -u, --username TEXT             Username
  -pwd, --password TEXT           Password
  -d, --debug INTEGER             Debug level  [default: 0]
  --help                          Show this message and exit.
```

## Example

```
python h8_jaxa.py -p L1 -r 2km -sd <YYYY-MM-DD_HH:MM> -ed <YYYY-MM-DD_HH:MM> -u <username> -pwd <password>
```

## Structure

## L1 data

Remote directory structure:

```
/jma/netcdf
   +---/[YYYYMM]
          +---/[DD]
                 +---/[hh]
```

Saved directory structure:

```
/<save_path>
        +---/[YYYYMM]
            +---/[DD]
```

### L2 data

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

Saved directory structure:

```
/<save_path>
        +---/[YYYYMM]
            +---/[DD]
                +---/[hh]
```

# 2. Himawari (CEReS)

## Links

http://www.cr.chiba-u.jp/databases/GEO/H8_9/FD/index.html

## Supported products

### L1

| CEReS gridded data | JMA's H8, 9 band   | Pixel x Line       | gridded resolution |                              |
| ------------------ | ------------------ | ------------------ | ------------------ | ---------------------------- |
| EXT                | 01                 | Band 03 (0.64 μ m) | 24000 x 24000      | 0.005 degree (approx. 500 m) |
| VIS                | 01                 | Band 01 (0.47 μ m) | 12000 x 12000      | 0.01 degree (approx. 1km)    |
| 02                 | Band 02 (0.51 μ m) |                    |                    |                              |
| 03                 | Band 04 (0.86 μ m) |                    |                    |                              |
| SIR                | 01                 | Band 05 (1.6 μ m)  | 6000 x 6000        | 0.02 degree (approx. 2km)    |
| 02                 | Band 06 (2.3 μ m)  |                    |                    |                              |
| TIR                | 01                 | Band 13 (10.4 μ m) | 6000 x 6000        | 0.02 degree (approx. 2km)    |
| 02                 | Band 14 (11.2 μ m) |                    |                    |                              |
| 03                 | Band 15 (12.4 μ m) |                    |                    |                              |
| 04                 | Band 16 (13.3 μ m) |                    |                    |                              |
| 05                 | Band 07 (3.9 μ m)  |                    |                    |                              |
| 06                 | Band 08 (6.2 μ m)  |                    |                    |                              |
| 07                 | Band 09 (6.9 μ m)  |                    |                    |                              |
| 08                 | Band 10 (7.3 μ m)  |                    |                    |                              |
| 09                 | Band 11 (8.6 μ m)  |                    |                    |                              |
| 10                 | Band 12 (9.6 μ m)  |                    |                    |                              |

## Usage

Change the info in `h8_CEReS.py` and run it directly.

## Structure

```
....../data/H8_CEReS/<year>
```

