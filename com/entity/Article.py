# encoding=utf-8


class Article:

    def __init__(self, sid, article_id, name, url, read_count, discuss_count, spread_count):
        self.sid = sid
        self.article_id = article_id
        self.name = str(name).replace('\\', '')
        self.url = url
        self.read_count = read_count
        self.discuss_count = discuss_count
        self.spread_count = spread_count

    def to_string(self):
        return 'sid:{}, article_id:{}, name:{}, url:{}, read_count:{}, discuss_count:{}, spread_count:{}'.format(
            self.sid, self.article_id, self.name, self.url, self.read_count, self.discuss_count, self.spread_count)
