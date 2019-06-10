from utils.google_calendar_api import getService

service = getService()
colors = service.colors().get(fields='event').execute()

hexcode_to_color_dict = {
    '#a4bdfc': 'LAVENDER',
    '#5484ed': 'BLUEBERRY',
    '#46d6db': 'PEACOCK',
    '#7ae7bf': 'SAGE',
    '#51b749': 'BASIL',
    '#ffb878': 'TANGERINE',
    '#fbd75b': 'BANANA',
    '#ff887c': 'FLAMINGO',
    '#dc2127': 'TOMATO',
    '#dbadff': 'GRAPE',
    '#e1e1e1': 'GRAPHITE'
}


def getColorName(hexcode):
    ''' hex code color -> name of color '''
    if hexcode in hexcode_to_color_dict:
        return hexcode_to_color_dict[hexcode]
