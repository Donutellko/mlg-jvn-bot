from bs4 import BeautifulSoup, Tag

import requests

from clients.gestion_client_helper import Activity

site_name = "\u006d\u0061\u006c\u0061\u0067\u0061\u002e\u0065\u0075"

URL_ONCOMING = f"https://juventud.{site_name}/es/actividades-y-programas-00001/listado-actividades/"

COMMON_HEADERS = {}
COLUMNS = {
    'Nombre', 'Programa', 'Fecha Inicio Inscripción',  # 0 1 2
    'Fecha Inicio Realización', 'Edades', 'Consulta plazas disponibles o inscríbete *'  # 3 4 5
}

COLUMN_NOMBRE = 0
COLUMN_PROGRAMA = 1
COLUMN_FECHA_INSCRIPCION = 2
COLUMN_FECHA_REALIZACION = 3
COLUMN_EDAD = 4


def get_oncoming(all: bool = False) -> [Activity]:
    """all - if should include past events and Mobility programs, not supported yet"""

    dom = get_oncoming_dom()
    activities_table = dom.select_one('table#example')
    activities_rows = activities_table.find_all('tr')[1:]
    activities = [parse_row(activity_row) for activity_row in activities_rows]
    if not all:
        activities = [a for a in activities if a.fecha is not None]

    print(f"Parsed {len(activities)} actividades")
    return activities


def parse_row(row: Tag):
    columns = row.find_all('td')
    return Activity(
        codigo=None,
        descripcion=columns[COLUMN_NOMBRE].text,
        fecha=columns[COLUMN_FECHA_REALIZACION].text,
        fechas_inscripcion=columns[COLUMN_FECHA_INSCRIPCION].text,
        plazas_libres=0,
        pago=None,
        edades=columns[COLUMN_EDAD].text,
        programa=columns[COLUMN_PROGRAMA],
    )


def get_oncoming_dom() -> BeautifulSoup:
    response = requests.request("GET", URL_ONCOMING, headers=COMMON_HEADERS)
    html_doc = response.text
    print(f"Get /oncoming, code {response.status_code}, length: {len(html_doc)}, lasted {response.elapsed}")
    return BeautifulSoup(html_doc, 'html.parser')


if __name__ == "__main__":
    activities = get_oncoming()
    print("Next activities: " + '\n'.join([a.str_oncoming() for a in activities]))

    print("end")
