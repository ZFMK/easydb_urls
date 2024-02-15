#!/usr/bin/env python
# -*- coding: utf-8 -*-
class SessionAuthentication ():
	def __init__(self, request):
		self.request = request

	def setSessionToken(self, sessiontoken = None):
		self.request.session['eastoken'] = sessiontoken

	def getSessionToken(self):
		try:
			return self.request.session['eastoken']
		except KeyError:
			self.setSessionToken(None)
			return self.request.session['eastoken']
