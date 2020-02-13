from datetime import date

from jinja2 import Environment, PackageLoader, select_autoescape

from table_calendar.app import app
from table_calendar.calendar import CustomHTMLCalendar

env = Environment(
    loader=PackageLoader("table_calendar", "templates"),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('index.html')


@app.route('/')
def index_view():
    return template.render(
        table=CustomHTMLCalendar().format_years(
            year=date.today().year,
            years_around=1,
        )
    )
