#!/usr/bin/env python
#coding: utf8

from sgs.cards.wholecard import WholeCard

WHOLE_CARD=WholeCard()

def getHeadCard(cnt): return WHOLE_CARD.getHead(cnt)
def getTailCard(cnt): return WHOLE_CARD.getTail(cnt)
def putHeadCard(cardlist): WHOLE_CARD.putHead(cardlist)
def putTailCard(cardlist): WHOLE_CARD.putTail(cardlist)
