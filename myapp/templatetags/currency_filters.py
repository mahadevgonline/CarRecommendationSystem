# -*- coding: utf-8 -*-
from django import template

register = template.Library()

# Current USD to INR rate (as of Feb 2026)
USD_TO_INR = 85.0

# Rupee symbol
RUPEE = '\u20b9'


@register.filter(name='inr')
def to_inr(value):
    """
    Converts a USD price to INR and formats with Rupee symbol
    and Indian number formatting (e.g. 1,23,45,678).
    Usage: {{ car.price|inr }}
    """
    try:
        amount = float(value) * USD_TO_INR
        amount_int = int(round(amount))
        formatted = format_indian(amount_int)
        return RUPEE + formatted
    except (TypeError, ValueError):
        return value


def format_indian(n):
    """Formats a number using the Indian numbering system."""
    s = str(n)
    if len(s) <= 3:
        return s
    result = s[-3:]
    s = s[:-3]
    while len(s) > 2:
        result = s[-2:] + ',' + result
        s = s[:-2]
    if s:
        result = s + ',' + result
    return result


@register.filter(name='inr_raw')
def to_inr_raw(value):
    """Returns the raw INR integer (for JS calculations)."""
    try:
        return int(round(float(value) * USD_TO_INR))
    except (TypeError, ValueError):
        return value
