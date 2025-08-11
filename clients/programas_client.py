from bs4 import BeautifulSoup, Tag
import requests
from typing import List, Dict, Optional, Any
import traceback
from datetime import datetime, date
import re

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

        # Handle format like "Del 1 al 25 de Septiembre" or "Del 1 de Agosto al 02 de Septiembre"
        elif inscription_date_str:
            # Pattern for "Del 1 al 25 de Septiembre"
            pattern1 = r"Del\s+(\d+)\s+al\s+\d+\s+de\s+(\w+)"
            # Pattern for "Del 1 de Agosto al 02 de Septiembre"
            pattern2 = r"Del\s+(\d+)\s+de\s+(\w+)\s+al"
            # Pattern for simple date like "26 de Junio"
            pattern3 = r"(\d+)\s+de\s+(\w+)"

            match = re.search(pattern1, inscription_date_str)
            if not match:
                match = re.search(pattern2, inscription_date_str)
            if not match:
                match = re.search(pattern3, inscription_date_str)

            if match:
                day = int(match.group(1))
                month_name = match.group(2)
                month = get_month_number(month_name)

                # Use current year for comparison
                start_date = date(current_date.year, month, day)

                # If the resulting date is more than 6 months in the past,
                # it's likely for next year
                if (current_date - start_date).days > 180:
                    start_date = date(current_date.year + 1, month, day)

                return start_date >= current_date

        return True  # If we can't parse the date, include the activity
    except Exception as e:
        # If there's any error parsing the date, include the activity
        print(f"Error parsing date '{inscription_date_str}': {str(e)}")
        return True


def get_month_number(month_name: str) -> int:
    """
    Convert Spanish month name to its number (1-12)

    Args:
        month_name: Spanish month name

    Returns:
        Month number (1-12)
    """
    month_name = month_name.lower().strip()
    months = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }
    return months.get(month_name, 1)  # Default to January if not found


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
