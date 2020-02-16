from calendar import HTMLCalendar, month_abbr


class CustomHTMLCalendar(HTMLCalendar):
    def __init__(self, *args, show_month_names=True, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_month_names = show_month_names

    def format_week(self, week, month, is_first_week, number_of_weeks):
        """
        Return a complete week as a table row.
        Does not override `formatweek` because it breaks its contract
        """

        parts = ['<tr>']

        if self.show_month_names and is_first_week:
            parts.append(
                '<td rowspan={} class="month-name">{}</td>'.format(
                    number_of_weeks,
                    month_abbr[month]
                )
            )

        parts.append(''.join(
            self.formatday(d, wd) for (d, wd) in week
        ))

        parts.append('</tr>')

        return ''.join(parts)

    def formatmonth(self, theyear, themonth, withyear=True):
        """
            Overrides formatmonth:
                better syntax and calls format_week with its new signature (instead of formatweek)
        """

        parts = []
        parts.append(
            '<table border="0" cellpadding="0" cellspacing="0" class="month">'
        )

        month_matrix = self.monthdays2calendar(theyear, themonth)

        for i in range(0, len(month_matrix)):
            parts.append(
                self.format_week(
                    month_matrix[i],
                    themonth,
                    is_first_week=i == 0,
                    number_of_weeks=len(month_matrix),
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
