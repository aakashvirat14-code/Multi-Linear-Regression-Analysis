#import library
import pandas as pd
import numpy as np

#load dataset
data = pd.read_csv("C:\imagecon\Dataset\multiple_linear_regression_unclean_500_rows.csv")
print(data)
#data inspection
data.head()
data.tail()
data.shape
data.describe()
data.info()

#data cleaning
#checking null values 
data.isnull().sum()
#fill missing values
data["Area_sqft"] = data["Area_sqft"].fillna(data["Area_sqft"].mean())
data["Bedrooms"] = data["Bedrooms"].fillna(data["Bedrooms"].median())
data["Bathrooms"] = data["Bathrooms"].fillna(data["Bathrooms"].median())
data["Parking"] = data["Parking"].fillna(data["Parking"].median())
data["Location"] = data["Location"].fillna(data["Location"].mode()[0])
data["Price"] = data["Price"].fillna(data["Price"].mean())

#drop age
data.drop("Age", axis=1, inplace=True)

#encode location
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data["Location"] = le.fit_transform(data["Location"])

#split x and y
x = data.iloc[:,[0,1,2,4]].values
y = data.iloc[:, -1].values

#train test split
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(
    x,y,test_size=0.30,random_state=0
)

#model
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train,y_train)

#prediction
y_pred = regressor.predict(x_test)
print(y_pred)

#scores
print("Train Score:", regressor.score(x_train,y_train))
print("Test Score:", regressor.score(x_test,y_test))

# HOUSE PRICE PREDICTOR GUI

import tkinter as tk
from tkinter import messagebox

def predict_house_price():
    try:
        area = float(area_entry.get())
        bedroom = int(bedroom_entry.get())
        bathroom = int(bathroom_entry.get())

        location = location_var.get()

        if location == "Urban":
            location = 2
        elif location == "Suburban":
            location = 1
        else:
            location = 0

        new_data = [[area, bedroom, bathroom, location]]

        prediction = regressor.predict(new_data)

        result_label.config(
            text=f"Predicted House Price\n₹ {prediction[0]:,.0f}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("House Price Prediction")
root.geometry("700x550")
root.configure(bg="lightblue")

title = tk.Label(
    root,
    text="🏠 HOUSE PRICE PREDICTION SYSTEM",
    font=("Arial",20,"bold"),
    bg="lightblue",
    fg="darkblue"
)
title.pack(pady=20)

# Area
tk.Label(root,text="Area Sqft",
         font=("Arial",12,"bold"),
         bg="lightblue").pack()

area_entry = tk.Entry(root,font=("Arial",12),width=25)
area_entry.pack(pady=5)

# Bedroom
tk.Label(root,text="Bedrooms",
         font=("Arial",12,"bold"),
         bg="lightblue").pack()

bedroom_entry = tk.Entry(root,font=("Arial",12),width=25)
bedroom_entry.pack(pady=5)

# Bathroom
tk.Label(root,text="Bathrooms",
         font=("Arial",12,"bold"),
         bg="lightblue").pack()

bathroom_entry = tk.Entry(root,font=("Arial",12),width=25)
bathroom_entry.pack(pady=5)

# Location
tk.Label(root,text="Location",
         font=("Arial",12,"bold"),
         bg="lightblue").pack()

location_var = tk.StringVar()
location_var.set("Urban")

location_menu = tk.OptionMenu(
    root,
    location_var,
    "Urban",
    "Suburban",
    "Rural"
)
location_menu.pack(pady=5)

# Predict Button
predict_btn = tk.Button(
    root,
    text="Predict House Price",
    font=("Arial",14,"bold"),
    bg="green",
    fg="white",
    command=predict_house_price
)
predict_btn.pack(pady=20)

# Result Label
result_label = tk.Label(
    root,
    text="Enter House Details",
    font=("Arial",18,"bold"),
    bg="lightblue",
    fg="red"
)
result_label.pack(pady=20)

root.mainloop()

