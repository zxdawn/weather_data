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

   ​

