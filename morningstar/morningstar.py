from requests import PreparedRequest
import requests
import sys


MORNING_STAR_FINANCE = 'http://financials.morningstar.com'
REPORT_PROCESS = '/ajax/ReportProcess4CSV.html'
KEY_RATIO_REPORT = '/finan/ajax/exportKR2CSV.html'
PERCENTAGE = 'percentage'
RAW = 'raw'


def __get_data(url, params=None, headers=None):
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != requests.codes.ok:
        print('status code: ' + str(response.status_code))
        return None

    return response.text


def key_ratio(symbol):
    url = MORNING_STAR_FINANCE + KEY_RATIO_REPORT
    params = {
        'callback': '?',
        't': symbol,
        'region': 'usa',
        'culture': 'en-US',
        'order': 'asc'
    }

    req = PreparedRequest()
    req.prepare_url(MORNING_STAR_FINANCE + '/ratios/r.html', params={
        't': params['t']
    })

    headers = {
        'Referer': req.url
    }

    return __get_data(url, params, headers)


def financial_sheet(metadata):
    """
    metadata {
        symbol: ticket,
        view: data type,
        finance: income-statement, cash-flow, balance-sheet
        reportType: is, cf, bs
    }
    """
    url = MORNING_STAR_FINANCE + REPORT_PROCESS
    params = {
        't': metadata['symbol'],
        'region': 'usa',
        'culture': 'en-US',
        'cur': '',
        'reportType': metadata['reportType'],
        'period': 12,
        'dataType': 'A',
        'order': 'asc',
        'columnYear': 5,
        'curYearPart': '1st5year',
        'rounding': 3,
        'view': metadata['view'],
        'denominatorView': metadata['view'],
        'number': 3
    }

    req = PreparedRequest()
    req.prepare_url(MORNING_STAR_FINANCE + '/' + metadata['finance'] + '/' + params['reportType'] + '.html',
                    params={
                        't': params['t'],
                        'region': params['region'],
                        'culture': params['culture']
                    })
    headers = {
        'Referer': req.url
    }

    return __get_data(url, params, headers)


def income_statement(symbol, show=PERCENTAGE):
    metadata = {
        'symbol': symbol,
        'view': show,
        'finance': 'income-statement',
        'reportType': 'is'
    }

    return financial_sheet(metadata)


def cash_flow(symbol, show=PERCENTAGE):
    metadata = {
        'symbol': symbol,
        'view': show,
        'finance': 'cash-flow',
        'reportType': 'cf'
    }

    return financial_sheet(metadata)


def balance_sheet(symbol, show=PERCENTAGE):
    metadata = {
        'symbol': symbol,
        'view': show,
        'finance': 'balance-sheet',
        'reportType': 'bs'
    }

    return financial_sheet(metadata)


def main():
    income = income_statement('DIS')
    if income:
        print(income)
    else:
        print('income statement is unsuccessful')

    bs = balance_sheet('SBUX')
    if bs:
        print(bs)
    else:
        print('balance sheet is unsuccessful')

    cf = cash_flow('AAPL')
    if cf:
        print(cf)
    else:
        print('cash flow is unsuccessful')


if __name__ == '__main__':
    main()
