#----------------------------------------------------------------------------------------------------------------------#
#  MBRadio
#
#  iTunes XML DB Implementation
#----------------------------------------------------------------------------------------------------------------------#

import MusicLibrary
import xml.parsers.expat

class iTunesLibrary(MusicLibrary.MusicLibrary):
		
	def load(self, path):
		
		print "   Parsing iTunes XML..."
		p = xml.parsers.expat.ParserCreate()
		p.StartElementHandler = self.start_element
		p.EndElementHandler = self.end_element
		p.CharacterDataHandler = self.char_data
		p.ParseFile(file(path))
		print "   Loaded " + str(self.trackCount) + " tracks!"
		
		print self.tracks
		
	# Private variables
	
	inDict = 0
	inKey = 0
	inTracks = 0
	inTrack = 0
	inData = 0
	currentKey = ""
	skipRest = 0
	trackID = ''
	trackTitle = ''
	trackArtist = ''
	trackAlbum = ''
	trackGenre = ''
	trackDuration = ''
					
	# Private methods:
	
	def start_element(self, name, attrs):
		if self.skipRest:
			return
			
		if name == u'key':
			self.inKey = 1
		elif name == u'dict':
			self.inDict = 1
		elif name == u'string' or name == u'integer':
			self.inData = 1

	def end_element(self, name):
		if self.skipRest:
			return
			
		if name == u'key':
			self.inKey = 0
		elif name == u'dict':
			self.inDict = 0

			if self.inTracks and self.inTrack:
				self.addTrack(self.trackID, self.trackTitle, self.trackArtist, self.trackAlbum, self.trackGenre, self.trackDuration)
				self.inTrack = 0
				
		self.inData = 0
		
	def char_data(self, data):
		if self.skipRest:
			return
			
		if self.inKey:
			if data == u'Playlists':
				self.skipRest = 1
				return
			
			if self.inTracks:
				self.currentKey = data
				
				if data == u'Track ID':
					self.inTrack = 1
					self.trackID = ''
					self.trackTitle = ''
					self.trackArtist = ''
					self.trackAlbum = ''
					self.trackGenre = ''
					self.trackDuration = ''
					
			else:
				if data == u'Tracks':
					self.inTracks = 1
		
		elif self.inData and self.inTracks and self.inTrack:
				if self.currentKey == u'Track ID':
					self.trackID = int(data)
				elif self.currentKey == u'Name':
					self.trackTitle = data
				elif self.currentKey == u'Artist':
					self.trackArtist = data
				elif self.currentKey == u'Album':
					self.trackAlbum = data
				elif self.currentKey == u'Genre':
					self.trackGenre = data
				elif self.currentKey == u'Total Time':
					self.trackDuration = int(data)
					