'''
FUNCTION:
    Download Himawari-8 JAXA data using one script

UPDATE:
    Xin Zhang:
       06/25/2020: support L2 data
       01/31/2021: support L1 data
'''

import os
import sys
import click
import ftplib
import ntpath
from tqdm import tqdm
from glob import glob
from datetime import datetime
from datetime import timedelta


def files_list(d1, d2, tstep, product, resolution):
    '''
    Generate filenames by time step
    https://stackoverflow.com/questions/
        39298054/generating-15-minute-time-interval-array-in-python
    '''
    files = []
    step = timedelta(minutes=tstep)
    seconds = (d2-d1).total_seconds()

    # generate basenames
    for i in range(0, int(seconds), int(step.total_seconds())):
        files.append(d1 + timedelta(seconds=i))

    # get all files from sdate to edate by tstep
    if product != 'L1':
        files = [date.strftime('%Y%m/%d/%H/') +
                 f'*H08_{date.strftime("%Y%m%d_%H%M")}_*_FLDK*nc'
                 for date in files]
    elif resolution == '2km':
        files = [date.strftime('%Y%m/%d/') +
                 f'*H08_{date.strftime("%Y%m%d_%H%M")}_*_FLDK.06001_06001.nc'
                 for date in files]
    else:
        files = [date.strftime('%Y%m/%d/') +
                         f'*H08_{date.strftime("%Y%m%d_%H%M")}_*_FLDK.02401_02401.nc'
                         for date in files]
    return files


def downloadFiles(ftp, source, product, file, destination, debug):
    '''
    Download files of newest version
    '''
    if product != 'L1':
        # omit 'bet' version
        files = [os.path.basename(f) for f in ftp.nlst(source+product) if os.path.basename(f).isdigit()]
        # get the newest version
        version = sorted(files, key=lambda x: float(x))[-1]
        data_dir = os.path.dirname(source+product+'/'+version+'/'+file)
    else:
        data_dir = os.path.dirname(source+file)

    try:
        ftp.cwd(data_dir)
    except OSError:
        pass
    except ftplib.error_perm:
        print(f'Error: could not change to {data_dir}')
        return 0

    filename = ntpath.basename(file)
    try:
        filename = ftp.nlst(filename)[0]
        ftp.sendcmd('TYPE I')
        filesize = ftp.size(filename)

        # download data
        with open(os.path.dirname(destination)+'/'+filename, 'wb') as f:
            # set progress bar
            with tqdm(total=filesize, unit_scale=True, desc=filename, miniters=1,
                      file=sys.stdout, leave=False) as pbar:
                def file_write(data):
                    pbar.update(len(data))
                    f.write(data)
                ftp.retrbinary('RETR ' + filename, file_write)

            if debug > 0:
                print('    Downloaded')

    except:
        print('Error: File could not be downloaded ' + filename)
        return 0

    return 1


# -------------------------------------------------------
@click.command()
@click.option(
    '--save_path',
    '-s',
    default='./data/H8/',
    help='Directory where you want to save files.',
    show_default=True
)

@click.option(
    '--sdate',
    '-sd',
    help='''
            Beginning date of downloaded files
            YYYY-MM-DD_hh:mm
         '''
)

@click.option(
    '--edate',
    '-ed',
    help='''
            Ending date of downloaded files
            YYYY-MM-DD_hh:mm
         '''
)

@click.option(
    '--tstep',
    '-ts',
    default=10,
    help='Time step (min) between files',
    show_default=True
)

@click.option(
    '--product',
    '-p',
    type=click.Choice(['L1', 'ARP', 'CLP', 'PAR']),
    default='L1',
    help='''
            Product name in Capital.
            L1, ARP, CLP or PAR
         ''',
    show_default=True,
)

@click.option(
    '--resolution',
    '-r',
    type=click.Choice(['2km', '5km']),
    default='5km',
    help='''
            Resolution of the L1 product.
            2km or 5km
         ''',
    show_default=True,
)

@click.option(
    '--username',
    '-u',
    help='Username',
    show_default=True
)

@click.option(
    '--password',
    '-pwd',
    help='Password',
    show_default=True
)

@click.option(
    '--debug',
    '-d',
    default=0,
    help='Debug level',
    show_default=True
)


def main(save_path,
         sdate, edate, tstep,
         product, resolution,
         username, password,
         debug):
    '''
    \b
    Fuctions:
        Download Himawari-8 Level 1 and Level 2 products from JAXA and save to directories
    Contact:
        xinzhang1215@gmail.com
    '''
    # get the base url
    server = 'ftp.ptree.jaxa.jp'  # JAXA data server

    if product == 'L1':
        source = '/jma/netcdf/' # Level 1
    else:
        source = '/pub/himawari/L2/' # Level 2

    # get the list of datetime from sdate to edate by day
    d1 = datetime.strptime(sdate, '%Y-%m-%d_%H:%M')
    d2 = datetime.strptime(edate, '%Y-%m-%d_%H:%M')

    # get filenames based on dates
    files = files_list(d1, d2, tstep, product, resolution)

    # log into the server
    ftp = ftplib.FTP(server)
    ftp.login(username, password)

    save_path = os.path.join(save_path, "")
    for file in tqdm(files, desc='total progress'):
        # iterate and download files
        filename = ntpath.basename(file)
        destination = os.path.join(save_path+file)

        # create directory
        if not os.path.exists(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))

        if debug > 0:
            print('Downloading ' + filename + ' ...')

        if glob(destination+filename):
            if debug > 0:
                print(filename + ' exists ...')
            continue

        file_exist = downloadFiles(ftp, source, product, file, destination, debug)

        # # skip following steps if file isn't found
        # if not file_exist:
        #     continue


if __name__ == '__main__':
    main()
