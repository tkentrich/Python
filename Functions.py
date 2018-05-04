#!/usr/bin/env python
# -*- coding: utf-8 -*-
def dms(lat, long):
	if lat < 0:
		ns = 'S'
		lat = -lat
	else:
	    	ns = 'N'
	if long < 0:
		ew = 'W'
		long = -long
	else:
		ew = 'E'
	latdeg = int(lat)
	latmin = int(lat % 1 * 60)
	latsec = int(lat * 60 % 1 * 60)
	longdeg = int(long)
	longmin = int(long % 1 * 60)
	longsec = int(long * 60 % 1 * 60)
	return u"%02d°%02d'%02d\"%s %02d°%02d'%02d\"%s" % (latdeg, latmin, latsec, ns, longdeg, longmin, longsec, ew,)

