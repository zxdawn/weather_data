'''
FUNCTION:
    Scraping historical lightning images from Blitzortung website:
        https://www.blitzortung.org/

UPDATE:
    Xin Zhang:
       02/28/2021: Basic
'''

import os
import click
import pandas as pd
import urllib.request
from PIL import Image
from tqdm import tqdm

# -------------------------------------------------------
@click.command()
@click.option(
    '--save_path',
    '-s',
    default='./figs/',
    help='Directory where you want to save figures.',
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
    '--region',
    '-r',
    type=click.Choice(['earth', 'eu', 'oc', 'us', 'as', 'sa', 'af']),
    default='earth',
    help='''
            Region name of lightning view. \n
            'earth': Overview map \n
            'eu': Europe \n
            'oc': Oceania \n
            'us': North America \n
            'as': Asia \n
            'sa': South America \n
            'af': Africa \n
         ''',
    show_default=True,
)

def main(save_path,
         sdate, edate,
         region):
    '''
    \b
    Fuctions:
        Scarping lightning location images from Blitzortung and overlay on background image
    Contact:
        xinzhang1215@gmail.com
    '''
    # set basic urls for website
    base_url = 'https://www.blitzortung.org/en/History'
    bg_url = f'{base_url}/Backgrounds/image_b_{region}.png'

    # get image urls
    dates = pd.date_range(start=sdate.replace('_', ' '),
                          end=edate.replace('_', ' '),
                          freq='5Min')
    urls = dates.strftime(f'{base_url}/%Y/%m/%d/%H/%M/image_b_{region}.png')
    savenames = dates.strftime(f'{save_path}/%Y%m%d/%Y%m%d_%H%M.png')

    # download the background first
    bg_savename = f'{save_path}/bg_{region}.png'
    urllib.request.urlretrieve(bg_url, bg_savename)
    bg = Image.open(bg_savename).convert('RGBA')

    # download the transparent png file and
    #   overlay it on the background downloaded before
    for index, url in enumerate(tqdm(urls, desc='total progress')):
        savename = savenames[index]
        # create directory
        if not os.path.exists(os.path.dirname(savename)):
            os.makedirs(os.path.dirname(savename))

        if not os.path.exists(savename):
            urllib.request.urlretrieve(url, savename)
            fg = Image.open(savename)
            Image.alpha_composite(bg, fg.convert('RGBA')).save(savename, 'PNG')
        else:
            continue


if __name__ == '__main__':
    main()
