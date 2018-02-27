import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def get_prop(id):
    url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=cyrjg&code={}'.format(id)
    web = requests.get(url,headers)
    soup = BeautifulSoup(web.content,'lxml')

    proportion_selector = soup.select('body > table > tbody > tr:nth-of-type(1) > td')
    if proportion_selector != []:
        proportion = [i.text for i in proportion_selector]
        return proportion
    else:
        return ['-','-','-','-','-']

def get_info(url):
    web = requests.get(url,headers)
    soup = BeautifulSoup(web.content,'lxml')
    # 有些基金处于封闭期，没有数据收益
    if soup.find(text='近1年：') != None:

        # 获取基金规模
        size_selector = soup.select('div.infoOfFund > table > tr > td:nth-of-type(2)')[0].text
        # 获取基金年化（获取近1年后的那个字符串）
        mmf_annualized = soup.find(text='近1年：').find_next('span').text
        mmf_id = url.split(r'/')[-1].split(r'.')[0]
        mmf_size = size_selector.split('：')[-1].split('元')[0].strip('亿')
        mmf_proportion = get_prop(mmf_id)
        mmf_info = [mmf_id,mmf_size,mmf_annualized] + mmf_proportion
        return mmf_info

