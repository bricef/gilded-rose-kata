# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose, update


"""
	- All items have a SellIn value which denotes the number of days we have to sell the item
	- All items have a Quality value which denotes how valuable the item is
	- At the end of each day our system lowers both values for every item

Pretty simple, right? Well this is where it gets interesting:

	- Once the sell by date has passed, Quality degrades twice as fast
	- The Quality of an item is never negative
	- "Aged Brie" actually increases in Quality the older it gets
	- The Quality of an item is never more than 50
	- "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
	- "Backstage passes", like aged brie, increases in Quality as it's SellIn value approaches;
	Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but
	Quality drops to 0 after the concert

We have recently signed a supplier of conjured items. This requires an update to our system:

	- "Conjured" items degrade in Quality twice as fast as normal items
"""


class GildedRoseTest(unittest.TestCase):
	def test_foo(self):
		items = [Item("foo", 0, 0)]
		new_items = update(items)
		self.assertEquals("foo", new_items[0].name)

	def test_degrade_twice_as_fast_after_sellby(self):
		items = [Item("foo", 1, 10)]
		new_items = update(update(items))
		self.assertEquals(new_items[0].quality, 7)

	def test_quality_cannot_go_below_zero(self):
		items = [Item("foo", 0, 0)]
		items = update(items)
		self.assertEquals(items[0].quality, 0)

	def test_aged_brie_gets_better(self):
		items = [Item("Aged Brie", 10, 10)]
		items = update(items)
		self.assertGreater(items[0].quality, 10)

	def test_maximum_quality_for_items_is_50(self):
		items = [Item("Aged Brie", 10, 50)]
		items = update(items)
		self.assertEquals(items[0].quality, 50)

	def test_sulfuras_is_special(self):
		items = [Item("The Sulfuras Gauntlet of awesome!", -1, 80)]
		items = update(items)
		self.assertEquals(items[0].quality, 80)

	def test_backstage_passes_increases_quality(self):
		items = [Item("Backstage passes for MegaMoose", 30, 10)]
		items = update(items)
		self.assertGreater(items[0].quality, 10)

	def test_backstage_passes_increase_by_two_within_ten_days(self):
		items = [Item("Backstage passes for MegaMoose", 9, 10)]
		items = update(items)
		self.assertEquals(items[0].quality, 12)

	def test_backstage_passes_increase_by_three_within_five_days(self):
		items = [Item("Backstage passes for MegaMoose", 4, 10)]
		items = update(items)
		self.assertEquals(items[0].quality, 13)

	def test_backstage_passes_have_no_quality_after_concert(self):
		items = [Item("Backstage passes for MegaMoose", 1, 40)]
		items = update(update(items))
		self.assertEquals(items[0].quality, 0)

	def test_conjured_item_degrades_twice_as_fast_before_date(self):
		items = [Item("Conjured Megalodon", 10, 40)]
		items = update(items)
		self.assertEquals(items[0].quality, 38)

	def test_conjured_item_degrades_twice_as_fast_after_date(self):
		items = [Item("Conjured Megalodon", -1, 40)]
		items = update(items)
		self.assertEquals(items[0].quality, 36)

if __name__ == '__main__':
    unittest.main()
