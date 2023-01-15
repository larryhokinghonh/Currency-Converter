import requests, math, emoji, apiKey, datetime
import tkinter as tk
import matplotlib.pyplot as plot
from tkinter import Frame, messagebox


class currConverterGUI:
    def __init__(self):
        # Set up the interface
        self.root = tk.Tk()

        rootWidth = 1080
        rootHeight = 720
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        xCoord = (screenWidth/2) - (rootWidth/2)
        yCoord = (screenHeight/2) - (rootHeight/2)

        self.root.geometry("{}x{}+{}+{}".format(rootWidth, rootHeight, int(xCoord), int(yCoord))) # Interface will appear in the middle of the user screen
        self.root.resizable(False, False)
        self.root.iconbitmap("images/favicon.ico")
        self.root.title("Currency Converter")

        #  Set up the frame for title, set up the title and subtitle for the program
        self.titleFrame = Frame(self.root)
        self.titleFrame.pack()

        self.title = tk.Label(self.titleFrame, text="Currency Converter", font=("Tahoma", 36))
        self.title.pack(padx=10, pady=40)

        self.subtitle = tk.Label(self.root, text="How much do you want to convert?", font=("Tahoma", 24))
        self.subtitle.pack(pady=25)

        # Set up the frame for labels
        self.label = Frame(self.root)
        self.label.pack()

        self.fromLabel = tk.Label(self.label, text="From: ", font=("Tahoma",18))
        self.fromLabel.pack(side=tk.LEFT, padx=140)

        self.toLabel = tk.Label(self.label, text="To: ", font=("Tahoma", 18))
        self.toLabel.pack(padx=140)

        # Set up the frame for user inputs
        self.currInput = Frame(self.root)
        self.currInput.pack()

        self.currAmtBefore = tk.Entry(self.currInput, width=15, font=("Tahoma", 18))
        self.currAmtBefore.pack(side=tk.LEFT, padx=10)

        self.currCodeBefore = tk.Entry(self.currInput, width=5, font=("Tahoma", 18))
        self.currCodeBefore.pack(side=tk.LEFT, padx=10)

        self.arrowBtn = tk.Button(self.currInput, text="⇆", width=2, command=self.swapCurrency, font=("Tahoma", 12))
        self.arrowBtn.pack(side=tk.LEFT, padx=5)

        self.displayAmt = tk.IntVar(self.root, 0) # Set one of the inputs to zero

        self.currAmtAfter = tk.Entry(self.currInput, width=15, textvariable=self.displayAmt, state="readonly", font=("Tahoma", 18))
        self.currAmtAfter.pack(side=tk.LEFT, padx=10)

        self.currCodeAfter = tk.Entry(self.currInput, width=5, font=("Arial", 18))
        self.currCodeAfter.pack(side=tk.LEFT, padx=10)

        # Set up the frame for "Convert" button
        self.btn = Frame(self.root)
        self.btn.pack()
        
        self.convertBtn = tk.Button(self.btn, text="Convert", command=self.convertCurrency, font=("Tahoma", 20))
        self.convertBtn.pack(pady=25)

        # Set up the frame for "days" input and "View Previous Conversion Rates" button
        self.displayPrevRate = Frame(self.root)
        self.displayPrevRate.pack()

        self.daysInput = tk.Entry(self.displayPrevRate, width=5, font=("Tahoma", 18))
        self.daysInput.pack(side=tk.LEFT, padx=10)

        self.text = tk.Label(self.displayPrevRate, text="Days", font=("Tahoma", 18))
        self.text.pack(side=tk.LEFT)

        self.viewPrevRateBtn = tk.Button(self.displayPrevRate, text="View Previous Conversion Rate", command=self.viewPreviousRate, font=("Tahoma", 16))
        self.viewPrevRateBtn.pack(padx=25, pady=20)

        # Set up the footer of the interface
        self.footerFrame = Frame(self.root)
        self.footerFrame.pack(side=tk.BOTTOM)

        self.clearAllBtn = tk.Button(self.footerFrame, text="Clear All", command=self.clearAll, font=("Tahoma", 18))
        self.clearAllBtn.pack()

        self.footerContent = tk.Message(self.footerFrame, text=emoji.emojize("Made With ❤ by Larry"), width=300, foreground="red", font=("Tahoma", 18))
        self.footerContent.pack(pady=50)

        # Prompts the user to confirm whether to close the program
        self.root.protocol("WM_DELETE_WINDOW", self.closeProgram)

        self.root.mainloop()

    def closeProgram(self):
        if messagebox.askyesno(title="Quit Program", message="Do you want to quit?"):
            self.root.destroy()

    def clearAll(self):
        self.currCodeBefore.delete(0, len(self.currCodeBefore.get()))
        self.currCodeAfter.delete(0, len(self.currCodeAfter.get()))
        self.currAmtBefore.delete(0, len(self.currAmtBefore.get()))
        self.daysInput.delete(0, len(self.daysInput.get()))

    def swapCurrency(self):
        temp = self.currCodeBefore.get()
        self.currCodeBefore.delete(0, len(self.currCodeBefore.get()))
        self.currCodeBefore.insert(0, self.currCodeAfter.get()) 
        self.currCodeAfter.delete(0, len(self.currCodeAfter.get()))
        self.currCodeAfter.insert(0, temp)

    def convertCurrency(self):
        self.currAmtAfter.config(state="normal")
        amtBefore = self.currAmtBefore.get()
        codeBefore = self.currCodeBefore.get().upper()
        codeAfter = self.currCodeAfter.get().upper()
        if not amtBefore or not codeBefore or not codeAfter:
            messagebox.showwarning(title="Error!", message="Please fill up the necessary fields")
            return

        response1 = requests.get(f"https://v6.exchangerate-api.com/v6/{apiKey.apiKey}/latest/{codeBefore.strip()}")
        try:
            jsonData1 = response1.json()
        except:
            messagebox.showwarning(title="Error!", message="Either one of the currency codes entered is invalid.")
            self.currAmtAfter.config(state="readonly")
            return

        if jsonData1["result"] == "error" or response1.status_code == "404":
            messagebox.showwarning(title="Error!", message="Either one of the currency codes entered is invalid.")
            self.currAmtAfter.config(state="readonly")
            return

        conversionRate = jsonData1["conversion_rates"][f"{codeAfter.strip()}"]
        try:
            total = int(amtBefore) * conversionRate
        except:
            messagebox.showwarning(title="Error!", message="Please enter a valid number.")
            self.currAmtAfter.config(state="readonly")
            return
        
        self.currAmtAfter.delete(0, len(str(total)))
        self.currAmtAfter.insert(0, "{:.2f}".format(total))
        self.currAmtAfter.config(state="readonly")

    def viewPreviousRate(self):
        amtOfDays = self.daysInput.get()
        codeBefore = self.currCodeBefore.get().upper()
        codeAfter = self.currCodeAfter.get().upper()

        if not amtOfDays or not codeBefore or not codeAfter:
            messagebox.showwarning(title="Error!", message="Please fill up the necessary fields.")
            return

        try:
            if int(amtOfDays) >= 365:
                messagebox.showwarning(title="Error!", message="Please refrain from requesting too much data.")
                return
        except:
            messagebox.showwarning(title="Error!", message="Please enter a valid number.")
            return

        # Structure user input before sending request to API
        prevDates = []
        for i in range(1, int(amtOfDays)+1):
            timestamp = str(datetime.datetime.today() - datetime.timedelta(days = i))
            date = timestamp[0:10]
            prevDates.append(date)

        # Retrieve and store converstion rate data according to each data from API
        prevConversionRates = []
        for dates in prevDates[::-1]:
            response2 = requests.get(f"https://theforexapi.com/api/{dates}/?base={codeBefore}&symbols={codeAfter}")
            if response2.status_code == "400":
                messagebox.showwarning(title="Error!", message="Invalid input(s).")
            jsonData2 = response2.json()
            try:
                conversionRate = jsonData2["rates"][f"{codeAfter}"]
            except:
                messagebox.showwarning(title="Error!", message="Either one of the currency codes entered is invalid.")
                return
            prevConversionRates.append(float(f"{conversionRate:.6f}"))

        monthDay = []
        for dates in prevDates[::-1]:
            monthDay.append(dates[5:10])
        
        # Set up algorithm to improve graph visualization by showing each rates after i days
        splitMonthDay = []
        splitConversionRates = []
        num = 1
        for i in range(2, 14):
            qiotient = int(amtOfDays) / i
            if qiotient > 15 and qiotient < 25:
                num = math.ceil(i)
                break

        if int(amtOfDays) >= 20:
            splitMonthDay = monthDay[::num]
            x = splitMonthDay
            splitConversionRates = prevConversionRates[::num]
            y = splitConversionRates
        else:
            x = monthDay
            y = prevConversionRates

        # Plot graph
        plot.plot(x, y)

        plot.xlabel("Date")
        plot.ylabel(f"{codeBefore} to {codeAfter}")

        plot.title(f"Graph of {codeBefore} to {codeAfter}")

        plot.show()

if __name__ == "__main__":
    currConverterGUI()