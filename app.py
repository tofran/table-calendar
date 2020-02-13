from flask import Flask
from calendar import HTMLCalendar, month_abbr
from datetime import date

app = Flask(__name__)


class CustomHTMLCalendar(HTMLCalendar):
    def formatweek(self, theweek, themonth, is_first_week):
        parts = ['<tr>']

        if is_first_week:
            parts.append(
                '<td rowspan=6 class="month-name">{}</td>'.format(
                    month_abbr[themonth]
                )
            )

        parts.append(''.join(
            self.formatday(d, wd) for (d, wd) in theweek
        ))

        parts.append('</tr>')

        return ''.join(parts)

    def formatmonth(self, theyear, themonth, withyear=True):
        parts = []
        parts.append(
            '<table border="0" cellpadding="0" cellspacing="0" class="month">'
        )

        month_matrix = self.monthdays2calendar(theyear, themonth)

        for i in range(0, len(month_matrix)):
            parts.append(
                self.formatweek(
                    month_matrix[i],
                    themonth,
                    i == 0,
                )
            )

        parts.append('</table>')
        return ''.join(parts)

    def format_years(self, year, years_around=0):
        return "".join(
            self.formatyear(year, width=1)
            for year in range(
                year - years_around,
                year + years_around + 1,
            )
        )


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Some Calendar</title>
    <style>
        .month-name{{
            transform: rotate(-90deg);
        }}
    </style>
</head>
<body>
    {body}
</body>
</html>
"""


@app.route('/')
def index_view():
    return PAGE_TEMPLATE.format(
        body=CustomHTMLCalendar().format_years(
            date.today().year,
            1,
        )
    )
