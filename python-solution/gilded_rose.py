# -*- coding: utf-8 -*-
import re 
import pprint


class CouldNotHandleItemError(RuntimeError):
    pass

def update(items):

    def past_sell_by(item):
        return item.sell_in < 0

    def update_default(item):
        if past_sell_by(item):
            item.quality -= 2
        else:
            item.quality -= 1
        return item

    def update_aged_brie(item):
        item.quality += 1
        return item

    def update_backstage(item):
        item.quality += 1
        if item.sell_in <= 10:
            item.quality += 1
        if item.sell_in <= 5:
            item.quality += 1
        if item.sell_in < 0:
            item.quality = 0
        return item

    def update_sellby_date(item):
        item.sell_in -= 1
        return item

    def enforce_quality_constraints(item):
        if item.quality < 0:
            item.quality = 0
        if item.quality > 50:
            item.quality = 50
        return item

    dispatch = [
        # No specifications on what happens to a Conjured backstage pass, or a conjured aged brie. 
        (".*Sulfuras.*", []),
        (".*[Cc]onjured.*", [update_sellby_date, update_default, update_default, enforce_quality_constraints]),
        (".*[Bb]ackstage [Pp]asses.*", [update_sellby_date, update_backstage, enforce_quality_constraints]),
        (".*[aA]ged [Bb]rie.*", [update_sellby_date, update_aged_brie, enforce_quality_constraints]),
        (".*", [update_sellby_date, update_default, enforce_quality_constraints])
    ]

    def update_item(item):
        for rx, updatefns in dispatch:
            if re.match(rx, item.name):
                for fn in updatefns:
                    item = fn(item)
                return item
        raise CouldNotHandleItemError()

    return [update_item(item) for item in items]

    
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
