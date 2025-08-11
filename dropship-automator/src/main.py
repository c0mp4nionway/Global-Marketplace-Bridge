import tkinter as tk
from gui.wizard import ConfigurationWizard

def main():
    root = tk.Tk()
    root.title("Dropship Automator")
    root.geometry("800x600")

    # Run the first-run configuration wizard
    wizard = ConfigurationWizard(root)
    wizard.run()

    root.mainloop()

if __name__ == "__main__":
    main()