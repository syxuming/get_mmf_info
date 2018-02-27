from get_mmf_url import mmf_url_list
from get_fund_info import get_info
import csv
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=250)
    with open('data.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['id','size','annualized','prop_dt','prop_large','prop_retail','prop_insider','share'])
        for num,url in enumerate(mmf_url_list[2800:]):
            print(num, url)
            row = executor.submit(get_info,url)
            if row.result() != None:
                writer.writerow(row.result())
        executor.shutdown()