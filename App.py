from customtkinter import CTk


class App(CTk):
	def __init__(self):
		super(App).__init__(self)


def main():
	app = App()
	app.mainloop()


if __name__ == "__main__":
	main()
