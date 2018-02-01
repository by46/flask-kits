# -:- coding:utf8 -:-
from flask_kits.exceptions import InvalidFormatError


class Pagination(object):
    """
    Example
    >>> from flask_kits.restful import entity.Pagination
    >>> class ItemsPagination(Pagination):
    >>>     limit = 20
    >>>     ORDERS = ('ID', 'NAME')
    >>> class ItemEntity(EntityBase):
    >>>     Range = Field("Range", type=ItemsPagination, location=LOC_HEADERS, default=DirectoryPagination.default)
    """
    DIRECTIONS = ('ASC', 'DESC')
    ORDERS = ('ID',)
    start = 0
    limit = 100
    order_by = 'ID'
    order = 'ASC'

    def __init__(self, line=None):
        self._parse(line)

    def _parse(self, line):
        line = line or ''
        segments = [x.strip() for x in line.split(';', 1) if x.strip()]
        if not segments:
            return

        try:
            segment, segments = segments[0], segments[1:]
            order_by, start_and_end = segment.split(' ', 1)
            if order_by not in self.ORDERS:
                raise InvalidFormatError()
            self.order_by = order_by

            start, end = start_and_end.split('..')
            start = int(start or str(self.start))
            self.start = max(start, 0)
            # end = int(end or str(self.start + self.limit))
            # if not (0 < start < end):
            #     raise InvalidFormatError()
            # self.start = start
            # self.limit = end - start

            if segments:
                segment, = segments
                options = dict([x.split('=') for x in segment.split(',') if x.strip()])
                if 'order' in options:
                    order = options.get('order', self.order).upper()
                    if order not in self.DIRECTIONS:
                        order = Pagination.order
                    self.order = order

                if 'max' in options:
                    size = int(options.get('max'))
                    self.limit = min(max(size, 0), 1000)

        except InvalidFormatError as e:
            raise e
        except Exception:
            raise InvalidFormatError()

    def status_and_headers(self, rowcount):
        code = 206 if rowcount == self.limit else 200
        h = {'Accept-Range': ','.join(self.ORDERS)}
        if code == 206:
            content_range = '{order_by} {start}..{end}'.format(
                order_by=self.order_by,
                start=self.start,
                end=self.start + rowcount)

            start = self.start + self.limit
            end = start + self.limit
            next_range = '{order_by} {start}..{end};order={order},max={limit}'.format(
                order=self.order,
                start=start,
                end=end,
                order_by=self.order_by,
                limit=self.limit
            )
            h['Next-Range'] = next_range
            h['Content-Range'] = content_range

        return code, h

    @classmethod
    def default(cls):
        return cls()
