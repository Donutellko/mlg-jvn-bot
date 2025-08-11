from bs4 import BeautifulSoup, Tag
import requests
from typing import List, Dict, Optional, Any
import traceback
from datetime import datetime, date

from clients.gestion_client_helper import Activity

site_name = "\u006d\u0061\u006c\u0061\u0067\u0061\u002e\u0065\u0075"

URL_LISTADO = f"https://juventud.{site_name}/es/actividades-y-programas-00001/listado-actividades/"
URLS = {
    'BIJ': f"https://juventud.{site_name}/es/actividades-y-programas-00001/banco-de-iniciativas-juveniles/talleres-bij-banco-de-iniciativas-juveniles/index.html",
    'Alterna en tu Ocio': f"https://juventud.malaga.eu/es/actividades-y-programas-00001/ocio/alterna-en-tu-ocio/#!tab2",
    'Jovenes y Naturaleza': f"https://juventud.{site_name}/es/actividades-y-programas-00001/ocio/jovenesynaturaleza/#!tab2",
}

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


def get_oncoming(all: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch and parse activities from multiple URLs

    Args:
        all: if should include past events and Mobility programs

    Returns:
        List of objects containing {name, error, entries, url}
    """
    results = []
    current_date = date.today()

    # Process each URL in URLS dictionary
    for name, url in URLS.items():
        result = {
            'name': name,
            'error': None,
            'entries': [],
            'url': url
        }

        try:
            dom = get_dom(url)
            activities_table = dom.select_one('table')
            if activities_table:
                activities_rows = activities_table.find_all('tr')[1:]
                activities = [parse_row(activity_row) for activity_row in activities_rows]
                if not all:
                    # Filter activities with valid inscription dates that are not in the past
                    activities = [a for a in activities if a.fecha is not None and
                                 is_inscription_date_valid(a.fechas_inscripcion, current_date)]
                result['entries'] = activities
            else:
                result['error'] = "No activities table found"
        except Exception as e:
            result['error'] = f"Error parsing {name}: {str(e)}"
            print(f"Error parsing {name} from {url}: {traceback.format_exc()}")

        results.append(result)

    print(f"Parsed {sum(len(r['entries']) for r in results)} actividades from {len(results)} sources")
    return results


def is_inscription_date_valid(inscription_date_str: str, current_date: date) -> bool:
    """
    Check if the inscription start date is valid (not in the past)

    Args:
        inscription_date_str: String containing the inscription date information
        current_date: Current date for comparison

    Returns:
        True if the inscription date is valid or can't be parsed, False if it's in the past
    """
    try:
        # Common date format in the data is DD/MM/YYYY
        if inscription_date_str and ":" in inscription_date_str:
            date_parts = inscription_date_str.split(':')
            if len(date_parts) >= 2:
                start_date_str = date_parts[1].strip().split(' ')[0]  # Extract the date part
                start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
                return start_date >= current_date
        return True  # If we can't parse the date, include the activity
    except Exception:
        # If there's any error parsing the date, include the activity
        return True


def parse_row(row: Tag) -> Activity:
    columns = row.find_all('td')
    return Activity(
        codigo=None,
        descripcion=columns[COLUMN_NOMBRE].text,
        fecha=columns[COLUMN_FECHA_REALIZACION].text,
        fechas_inscripcion=columns[COLUMN_FECHA_INSCRIPCION].text,
        plazas_libres=-1,
        pago=None,
        edades=columns[COLUMN_EDAD].text,
        programa=columns[COLUMN_PROGRAMA].text,
    )


def get_dom(url: str) -> BeautifulSoup:
    """Get and parse HTML from a URL"""
    response = requests.request("GET", url, headers=COMMON_HEADERS)
    html_doc = response.text
    print(f"Get {url}, code {response.status_code}, length: {len(html_doc)}, lasted {response.elapsed}")
    return BeautifulSoup(html_doc, 'html.parser')


if __name__ == "__main__":
    results = get_oncoming()
    for result in results:
        print(f"\n=== {result['name']} ===")
        if result['error']:
            print(f"ERROR: {result['error']}")
        else:
            print(f"Found {len(result['entries'])} activities:")
            for activity in result['entries']:
                print(f"- {activity.str_oncoming()}")

    print("end")
