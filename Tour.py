"""
    상품 정보를 담는 클레스
"""
class TourInfo:
    # 맴버변수
    title =''
    price =''
    area = ''
    link =''
    img =''
    # 생성자
    def __init__(self, title, price, area, link, img):
        self.title = title
        self.price = price
        self.area = area
        self.link = link
        self.img = img
