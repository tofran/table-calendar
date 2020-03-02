from datetime import MAXYEAR, MINYEAR, date

from flask import abort, request
from jinja2 import Environment, PackageLoader, select_autoescape

from table_calendar.app import app
from table_calendar.custom_calendar import CustomHTMLCalendar

MAX_YEARS_AROUND = 4

env = Environment(
    loader=PackageLoader('table_calendar', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('index.html.j2')


@app.route('/')
def index_view():
    try:
        year = int(request.args.get('year', date.today().year))
        years_around = int(request.args.get('years_around', 0))
        show_month_names = not request.args.get('hide_month_names', 'false') == 'true'

    except ValueError:
        abort(404)

    year = min(
        max(year, MINYEAR+years_around),
        MAXYEAR-years_around,
    )

    years_around = min(years_around, MAX_YEARS_AROUND)

    return template.render(
        year=year,
        years_around=years_around,
        max_years_around=MAX_YEARS_AROUND,
        show_month_names=show_month_names,

        table=(
            CustomHTMLCalendar(
                show_month_names=show_month_names,
            ).format_years(
                year=year,
                years_around=years_around,
            )
        )
    )
