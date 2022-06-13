from django.db import models
from django.contrib.auth.models import User
from copy import copy
from .constans import BOOST_TYPE_CHOOICES, BOOST_TYPE_VALUES


class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=1)
    level = models.IntegerField(default=0)

    def update_coins(self, coins, commit = True):
        self.coins = coins
        is_levelupdated = self.is_levelup()
        boost_type = 0
        if is_levelupdated:
            self.level += 1
            if self.level % 3 == 0:
                boost_type = 1
        if commit:
            self.save()

        return is_levelupdated, boost_type

    def is_levelup(self):
        return self.coins >= (self.level**2)*100*(self.level+1)

    def calculate_next_level(self):
        return (self.level**2)*100*(self.level+1)

class Boost(models.Model):
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    power = models.IntegerField(default=1)
    type = models.PositiveSmallIntegerField(
    default = 0, choices = BOOST_TYPE_CHOOICES,
    )

    def levelup(self, current_coins):
        if current_coins < self.price:
            return False

        self.core.coins = current_coins - self.price
        self.core.click_power \
            += self.power * BOOST_TYPE_VALUES[self.type]['click_power_scale']
        self.core.auto_click_power \
            += self.power * BOOST_TYPE_VALUES[self.type]['auto_click_power_scale']
        self.core.save()

        old_boost_values = copy(self)
        self.level += 1
        self.power *= 2
        self.price \
            += self.price * BOOST_TYPE_VALUES[self.type]['price_scale']
        self.save()

        return old_boost_values, self