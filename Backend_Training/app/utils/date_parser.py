import datetime


def get_date(input_date):
    if "-" in input_date:
        return datetime.datetime.strptime(input_date, "%Y-%m-%d").date()
    elif "/" in input_date:
        return datetime.datetime.strptime(input_date, "%Y/%m/%d").date()
    else:
        return datetime.datetime.strptime(input_date, "%Y%m%d").date()




