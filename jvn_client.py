from xml.dom.minidom import parseString
from html.parser import HTMLParser
from bs4 import BeautifulSoup, PageElement, Tag

import requests

from client_helper import Activity

site_name = "\u0061\u0070\u0070\u0073\u002e\u006d\u0061\u006c\u0061\u0067\u0061\u002e\u0065\u0075"

URL_OCCUPATION = f"https://{site_name}/inter/gca/edicion_ts/ayuda/ocupacion"

COMMON_HEADERS = {}
COLUMNS = {
    'Código', 'Descripción', 'Fechas Plazo Inscripción',  # 0 1 2
    'Plazas libres', 'Reservas', 'Edad',  # 3 4 5
    'F.I.Edicion', 'Pago', 'Acciones'  # 6 7 8
}

COLUMN_DESCRIPTION = 1
COLUMN_FREE_PLACES = 3
COLUMN_DATE = 6
COLUMN_PAID = 7
COLUMN_ACTIONS = 8


def get_activities(all: bool) -> [Activity]:
    dom = get_occupation_dom()
    activities_table = dom.select_one('div#content > table')
    activities_rows = activities_table.find_all('tr')[1:]
    activities = [parse_row(activity_row) for activity_row in activities_rows]
    if not all:
        activities = [a for a in activities if a.free_places > 0]

    print(f"Parsed {len(activities)} activities")
    return activities


def parse_row(row: Tag):
    columns = row.find_all('td')
    return Activity(
        description=columns[COLUMN_DESCRIPTION].text,
        date=columns[COLUMN_DATE].text,
        free_places=int(columns[COLUMN_FREE_PLACES].text),
        paid=columns[COLUMN_PAID].text == 'Y',
    )


def get_occupation_dom() -> BeautifulSoup:
    response = requests.request("GET", URL_OCCUPATION, headers=COMMON_HEADERS)
    html_doc = response.text
    print(f"Get /ocupacion, code {response.status_code}, length: {len(html_doc)}, lasted {response.elapsed}")
    return BeautifulSoup(html_doc, 'html.parser')


if __name__ == "__main__":
    activities = get_activities()
    print("Next activities: " + '\n'.join([str(a) for a in activities]))

    print("end")
