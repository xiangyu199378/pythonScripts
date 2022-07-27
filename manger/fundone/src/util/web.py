
import  requests

def get_html(code):
    Url = 'http://fund.eastmoney.com/{0}.html'.format(code)
    rsp = requests.get(Url)
    rsp.encoding = "UTF-8" 
    html = rsp.text  
    return html
