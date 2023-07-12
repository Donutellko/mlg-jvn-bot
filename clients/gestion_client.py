import requests
from bs4 import BeautifulSoup, Tag

from clients.gestion_client_helper import Activity

site_name = "\u006d\u0061\u006c\u0061\u0067\u0061\u002e\u0065\u0075"

URL_OCCUPATION = f"https://apps.{site_name}/inter/gca/edicion_ts/ayuda/ocupacion"
URL_ONCOMING = f"https://juventud.{site_name}/es/actividades-y-programas-00001/listado-actividades/"

COMMON_HEADERS = {}
COLUMNS = {
    'Código', 'Descripción', 'Fechas Plazo Inscripción',  # 0 1 2
    'Plazas libres', 'Reservas', 'Edad',  # 3 4 5
    'F.I.Edicion', 'Pago', 'Acciones'  # 6 7 8
}

COLUMN_DESCRIPCION = 1
COLUMN_FECHAS_INSCRIPCION = 2
COLUMN_PLAZAS_LIBRES = 3
COLUMN_RESERVAS = 4
COLUMN_EDAD = 5
COLUMN_FECHA_REALIZACION = 6
COLUMN_PAGO = 7
COLUMN_ACTIONS = 8


def get_activities(all: bool) -> [Activity]:
    dom = get_occupation_dom()
    activities_table = dom.select_one('div#content > table')
    activities_rows = activities_table.find_all('tr')[1:]
    activities = [parse_row(activity_row) for activity_row in activities_rows]
    if not all:
        activities = [a for a in activities if a.plazas_libres > 0]

    print(f"Parsed {len(activities)} activities")
    return activities


def parse_row(row: Tag):
    columns = row.find_all('td')
    return Activity(
        descripcion=columns[COLUMN_DESCRIPCION].text,
        fecha=columns[COLUMN_FECHA_REALIZACION].text,
        fechas_inscripcion=columns[COLUMN_FECHAS_INSCRIPCION].text,
        plazas_libres=int(columns[COLUMN_PLAZAS_LIBRES].text),
        pago=columns[COLUMN_PAGO].text == 'Y',
        edades=columns[COLUMN_EDAD].text,
    )


def get_occupation_dom() -> BeautifulSoup:
    response = requests.request("GET", URL_OCCUPATION, headers=COMMON_HEADERS)
    html_doc = response.text
    print(f"Get /ocupacion, code {response.status_code}, length: {len(html_doc)}, lasted {response.elapsed}")
    return BeautifulSoup(html_doc, 'html.parser')


if __name__ == "__main__":
    activities = get_activities(all=True)
    print("Next activities: " + '\n'.join([str(a) for a in activities]))

    print("end")
