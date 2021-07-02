# NOAA CLASS

## Link

NOAA CLASS website: https://www.avl.class.noaa.gov/saa/products/welcome

## Supported products

ABI L1 and L2 products:

Rad|CMIP|MCMIP|ACHA|ACHT|ACM|ACTP|ADP|AOD|COD|CPS|CTP|DMW|DMWV|DSI|DSR|FDC|FSC|HIE|LST|LVMP|RRQPE|RSR|SST|TPW|VAA|LVTP|DMWDIAG|DMWPQI|DMWVDIAG|DMWVPQI|AICE|AIM|AITA

## Usage

Check the help information

```
python noaa_class.py --help
```

```
Usage: noaa_class.py [OPTIONS]

Options:
  -sd, --sdate TEXT               Beginning date of downloaded files YYYY-MM-
                                  DD_hh:mm

  -ed, --edate TEXT               Ending date of downloaded files YYYY-MM-
                                  DD_hh:mm

  -p, --product [GRABIPRD]        Product name in Capital. GRABIPRD  [default:
                                  GRABIPRD]

  -c, --channel [C01|C02|C03|C04|C05|C06|C07|C08|C09|C10|C11|C12|C12|C13|C14|C15|C16]
                                  Channel name in Capital. GRABIPRD
  --dataset [Rad|CMIP|MCMIP|ACHA|ACHT|ACM|ACTP|ADP|AOD|COD|CPS|CTP|DMW|DMWV|DSI|DSR|FDC|FSC|HIE|LST|LVMP|RRQPE|RSR|SST|TPW|VAA|LVTP|DMWDIAG|DMWPQI|DMWVDIAG|DMWVPQI|AICE|AIM|AITA]
                                  Product type in Capital.  [default: ACHA]
  --satellite [G16|G17]           Product type in Capital.  [default: G16]
  --scan_mode [F|C|M1|M2]         Scan mode in Capital. F, C, M1, or M2
                                  [default: C]

  -u, --username TEXT             Username
  -pwd, --password TEXT           Password
  --help                          Show this message and exit.
```



