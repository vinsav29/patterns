
class Display:
	def __init__(self):
		self.x_size = 122
		self.y_size = 32
		self.Screen = bytearray(self.x_size * self.y_size // 8)

	def Pixel(self, X, Y, Color):
		line = Y >> 3;
		bit = Y & 7
		if Color > 0:
			self.Screen[line * self.x_size + X] |= (1 << bit)
		else:
			self.Screen[line * self.x_size + X] &= ~(1 << bit)
			
	def SetPixel(self, X, Y):
		line = Y >> 3;
		bit = Y & 7
		self.Screen[line * self.x_size + X] |= (1 << bit)
		
	def ResetPixel(self, X, Y):
		line = Y >> 3;
		bit = Y & 7
		self.Screen[line * self.x_size + X] &= ~(1 << bit)
		
	def GetPixel(self, X, Y):
		line = Y >> 3;
		bit = Y & 7
		
		pix = 0 if self.Screen[line * self.x_size + X] & (1 << bit) else 1
		return pix
		
	def InvertPixel(self, X, Y):
		line = Y >> 3;
		bit = Y & 7
		
		pix = 0 if self.Screen[line * self.x_size + X] & (1 << bit) else 1
		
		if pix > 0:
			self.Screen[line * self.x_size + X] |= (1 << bit)
		else:
			self.Screen[line * self.x_size + X] &= ~(1 << bit)
	
	def Clear(self):
		for i in range(len(self.Screen)):
			self.Screen[i] = 0
			
	def DrawLine(self, X1, Y1, X2, Y2, Color):
		deltaX = abs(X2 - X1)
		deltaY = abs(Y2 - Y1)
		
		signX = 1 if X1 <= X2 else -1  
		signY = 1 if Y1 <= Y2 else -1  
		
		error = deltaX - deltaY

		while ((X1 != X2) | (Y1 != Y2)):
			self.Pixel(X1, Y1, Color)
			error2 = error * 2

			if error2 > -deltaY:
				error -= deltaY
				X1 += signX

			if error2 < deltaX:
				error += deltaX
				Y1 += signY
				
		self.Pixel(X2, Y2, Color)
		
	def DrawRectangle(self, X1, Y1, X2, Y2, Color):
		signX = 1 if X1 <= X2 else -1  
		signY = 1 if Y1 <= Y2 else -1 
		
		for x in range(X1, X2 + 1, signX):
			self.Pixel(x, Y1, Color)
			self.Pixel(x, Y2, Color)
			
		for y in range(Y1, Y2 + 1, signY):
			self.Pixel(X1, y, Color)
			self.Pixel(X2, y, Color)

	def DrawFill(self, X1, Y1, X2, Y2, Color):
		signX = 1 if X1 <= X2 else -1  
		signY = 1 if Y1 <= Y2 else -1
		
		for y in range(Y1, Y2 + 1, signY):
			for x in range(X1, X2 + 1, signX):
				self.Pixel(x, y, Color)
				
	def DrawInvertFill(self, X1, Y1, X2, Y2):
		signX = 1 if X1 <= X2 else -1  
		signY = 1 if Y1 <= Y2 else -1
		
		for y in range(Y1, Y2 + 1, signY):
			for x in range(X1, X2 + 1, signX):
				self.InvertPixel(x, y)

	def DrawImage(self, X1, Y1, Image, Color):
		width, height, bitmap = Image
		
		for y in range(height):
			for x in range(width):
				byte = (x + width * y) >> 3
				bit = (x + width * y) & 0x07
				data = bitmap[byte] if Color > 0 else ~bitmap[byte]
				pix = data & (0x80 >> bit)
				self.Pixel(X1 + x, Y1 + y, pix)

	def DrawChar(self, X1, Y1, Char):
		code = ord(Char)
		Image = self.Font[code]
		self.DrawImage(X1, Y1, Image, 1)
		return X1 + Image[0]
		
	def DrawInvertChar(self, X1, Y1, Char):
		code = ord(Char)
		Image = self.Font[code]
		self.DrawImage(X1, Y1, Image, 0)

		for y in range(0, Image[1]):
			self.Pixel(X1 - 1, Y1 + y, 1)
		
		return X1 + Image[0]
		
	def DrawString(self, X1, Y1, Str):
		x = X1
		for char in Str:
			x = self.DrawChar(x, Y1, char)
		return x

	def DrawStringSelect(self, X1, Y1, Str, From, To):
		x = X1
		idx = 0
		for char in Str:
			if (idx >= From) & (idx <= To):
				x = self.DrawInvertChar(x, Y1, char)
			else:
				x = self.DrawChar(x, Y1, char)
			idx += 1
		return x
	
	def SetFont(self, Font):
		self.Font = Font
