import re

import requests

urls = [
    'https://www.alternate.de/ZOTAC/GeForce-RTX-3060-TWIN-EDGE-OC-Grafikkarte/html/product/1715299',
    'https://www.alternate.de/GIGABYTE/GeForce-RTX-3060-EAGLE-OC-12G-Grafikkarte/html/product/1723539'
]

for url in urls:
    # Get the content of the URL
    response = requests.get(url)

    # Check the response for it's content
    if response.text.find('Auf Lager') != -1:
        print('Hit! Ist auf Lager')
    elif response.text.find('Artikel kann derzeit nicht gekauft werden') != -1:
        print('Kein Hit! Nicht verfügbar!')
    else:
        print('Content nicht erkannt!')
