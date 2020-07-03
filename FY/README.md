# FY

## Link

FY satellite data website: <http://satellite.nsmc.org.cn/portalsite/default.aspx>

Real time FTP: <<http://fy4.nsmc.org.cn/data/en/data/realtime.html>>

## Usage

1. Order data on the [website](http://satellite.nsmc.org.cn/portalsite/default.aspx) (all platforms) or using the [Toolkit](http://fy4.nsmc.org.cn/nsmc/en/data/pcclient.html) (Windows).

2. Run the script from the terminal

   ```
   $ python fy.py
   ```

   Input the requested infos ....

   ![download](https://github.com/zxdawn/weather_data/raw/master/FY/examples/download_fy.gif)

3. Check the bash script named `download_fy.sh`

   (You can change the name by `savename` in the `fy,py` script)

4. Run the bash script

   ```
   $ chmod +x download_fy.sh
   $ ./download_fy.sh
   ```

   Example of the bash script:

   ```
   #!/bin/bash
   lftp -e "mget -c ftp://AO20200701000066936:Uo6O5__j@ftp.nsmc.org.cn/*" &
   lftp -e "mget -c ftp://AO20200701000065328:0lK_rxpW@ftp.nsmc.org.cn/AO202007010000653280001/*" &
   lftp -e "mget -c ftp://AO20200701000065328:0lK_rxpW@ftp.nsmc.org.cn/AO202007010000653280002/*" &
   lftp -e "mget -c ftp://AO20200701000065328:0lK_rxpW@ftp.nsmc.org.cn/AO202007010000653280003/*" &
   ```

   ​

