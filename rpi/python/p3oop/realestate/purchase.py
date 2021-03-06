class Purchase:
	def __init__(self, price='', taxes='', **kwargs):
		super().__init__(**kwargs)
		self.price = price
		self.taxes = taxes
		
	def display(self):
		super().display()
		print("PURCHASE DETAILS")
		print("selling price: {}".format(self.price))
		print("estimated taxes: {}".format(self.taxes))
		print()
		
	def prompt_init():
		return dict(
			price=input("What is the selling price? "),
			taxes=input("What are the estimated taxes? "))
	prompt_init = staticmethod(prompt_init)
	
