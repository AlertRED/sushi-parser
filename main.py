import requests
from lxml import html
import re
import pandas as pd
from pandas import ExcelWriter


def scrape_div(div) -> dict:
    items = div.xpath(".//div[@class='item product_data col-xs-1 col-sm-2 col-md-3 col-lg-2']")
    dct = dict()
    for item in items:
        name = item.xpath(".//span[@class='item-name']")[0].xpath(".//a")[0].text
        price = item.xpath(".//span[@class='item-price-value']")[0].text
        weight = item.xpath(".//span[@class='weight']")[0].text
        quantity = item.xpath(".//span[@class='quantity']")[0].text
        desc = item.xpath(".//span[@class='item-cons']")[0].text
        ingredients_count = len(desc.split(','))


        weight = re.sub('\D', '', weight)
        quantity = re.sub('\D', '', quantity)

        dct.setdefault('name', list()).append(name)
        dct.setdefault('price', list()).append(price)
        dct.setdefault('weight', list()).append(weight)
        dct.setdefault('quantity', list()).append(quantity)
        dct.setdefault('desc', list()).append(desc)
        dct.setdefault('ingredients_count', list()).append(ingredients_count)
    return dct


def scrape() -> dict:
    url = 'https://nsk.yapdomik.ru/?noredirect=true'
    text = requests.get(url).text
    tree = html.fromstring(text)

    dct = dict()

    dct['sets'] = scrape_div(tree.xpath("//div[@id='sets']")[0])
    dct['tempura'] = scrape_div(tree.xpath("//div[@id='tempura-rolls']")[0])
    dct['rolls'] = scrape_div(tree.xpath("//div[@id='rolls']")[0])
    dct['grill'] = scrape_div(tree.xpath("//div[@id='grill-rolls']")[0])
    return dct


def dump_csv(dct: dict):
    writer = ExcelWriter('rolls.xlsx')
    for title, items in dct.items():
        df = pd.DataFrame(items, columns=items.keys(), )
        df['formula'] = [f'=B{i}/C{i}' for i in range(2, df.shape[0]+2)]
        df.to_excel(writer, title, index=False, )
    writer.save()


if __name__ == '__main__':
    dct = scrape()
    dump_csv(dct)
