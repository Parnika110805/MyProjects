import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib
from tkinter import Tk, Frame, Button, Label
from PIL import Image, ImageTk
import webbrowser
import matplotlib.pyplot as plt
import seaborn as sns
import time
import numpy as np


# Load and preprocess data
def load_and_preprocess_data(csv_file):
    try:
        df = pd.read_csv(csv_file)

        df['Job Title'] = df['Job Title'].astype(str)
        df['Job Location'] = df['Job Location'].astype(str)

        le_job_title = LabelEncoder()
        le_job_location = LabelEncoder()
        df['Job Title Encoded'] = le_job_title.fit_transform(df['Job Title'])
        df['Job Location Encoded'] = le_job_location.fit_transform(df['Job Location'])

        df.fillna({'Salary': df['Salary'].median()}, inplace=True)

        X = df[['Job Title Encoded', 'Job Location Encoded', 'Experience']]
        y = df['Salary']

        return X, y, le_job_title, le_job_location
    except Exception as e:
        print(f"Error loading or preprocessing data: {e}")
        return None, None, None, None


# Train the model
def train_model(X, y):
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if len(X_test) < 2:
            print("Not enough samples for meaningful evaluation. Add more data or adjust split ratio.")
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            print("Model Evaluation:")
            print(f"MAE: {mae}")
            print(f"R2 Score: {r2}")

            joblib.dump(model, 'salary_predictor.pkl')
            print("Model saved successfully!")

            plot_model_performance(y_test, y_pred)

    except Exception as e:
        print(f"Error training model: {e}")


# Predict salary
def predict_salary(job_title, job_location, experience, job_title_le, job_location_le):
    try:
        model = joblib.load('salary_predictor.pkl')

        job_title_encoded = job_title_le.transform([job_title])[0]
        job_location_encoded = job_location_le.transform([job_location])[0]

        features = pd.DataFrame([[job_title_encoded, job_location_encoded, experience]],columns=['Job Title Encoded', 'Job Location Encoded', 'Experience'])

        predicted_salary = model.predict(features)[0]
        return predicted_salary
    except Exception as e:
        print(f"Error predicting salary: {e}")
        return None


#Popup notification
def show_popup(job_row, background_path, job_title_le, job_location_le):
    try:
        job_title = job_row['Job Title']
        job_location = job_row['Job Location']
        experience = job_row['Experience']
        link = job_row['Link']

        predicted_salary = predict_salary(job_title, job_location, experience, job_title_le, job_location_le)
        salary_text = f"{predicted_salary:.2f} LPA" if predicted_salary else "Unavailable"

        window = Tk()
        window.title("Job Notification")
        window.geometry("800x800")

        background = Image.open(background_path)
        background = background.resize((800, 800), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(background)

        bg_label = Label(window, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title_frame = Frame(window, bg="white")
        title_frame.place(relx=0.5, y=70, anchor="center")
        Label(title_frame, text=job_title, font=("Arial", 24), bg="white").pack()

        location_frame = Frame(window, bg="white")
        location_frame.place(relx=0.5, y=150, anchor="center")
        Label(location_frame, text=job_location, font=("Arial", 24), bg="white").pack()

        salary_frame = Frame(window, bg="white")
        salary_frame.place(relx=0.5, y=230, anchor="center")
        Label(salary_frame, text=salary_text, font=("Arial", 24), fg="green", bg="white").pack()

        button_frame = Frame(window, bg="white")
        button_frame.place(relx=0.5, y=310, anchor="center")
        Button(button_frame, text="Click Here", command=lambda: webbrowser.open(link),font=("Arial", 18), bg="green", fg="white").pack()

        time.sleep(5)
        window.mainloop()

    except Exception as e:
        print(f"Error displaying popup: {e}")


#Plotting graphs
def plot_model_performance(y_test, y_pred):
    try:
        if len(y_test) == 0 or len(y_pred) == 0:
            print("Error: The data is empty. Cannot plot performance.")
            return

        # Plot Actual vs Predicted Salaries (Bar plot)
        pd.DataFrame({'Actual Salary': y_test, 'Predicted Salary': y_pred}).head(10).plot(kind='bar', figsize=(10, 6), width=0.8)
        plt.title("Actual vs Predicted Salaries")
        plt.ylabel("Salary (in LPA)")
        plt.xlabel("Row Number")
        plt.xticks(ticks=range(10), labels=[f"Row {i+1}" for i in range(10)], rotation=45)
        plt.tight_layout()
        plt.show()

        # Plot Actual vs Predicted Salaries (Scatter plot)
        plt.figure(figsize=(12, 8))
        colors = plt.cm.viridis(np.linspace(0, 1, len(y_pred)))
        scatter = plt.scatter(x=y_test, y=y_pred, c=y_pred, cmap='viridis', s=120, edgecolor='black', alpha=0.8)
        plt.title("Actual vs Predicted Salaries (Scatter Plot)", fontsize=18, fontweight='bold', color='darkblue')
        plt.xlabel("Actual Salary (in LPA)", fontsize=15, fontweight='bold')
        plt.ylabel("Predicted Salary (in LPA)", fontsize=15, fontweight='bold')
        plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', linewidth=3, label='Perfect Prediction')
        plt.xticks(fontsize=12, fontweight='bold')
        plt.yticks(fontsize=12, fontweight='bold')
        plt.grid(True, linestyle='-', color='gray', linewidth=0.7, alpha=0.3)
        cbar = plt.colorbar(scatter)
        cbar.set_label('Predicted Salary (in LPA)', fontsize=14)
        plt.legend(fontsize=14, loc='upper left')
        plt.tight_layout()
        plt.show()

        # Plot distribution of Predicted Salaries
        sns.set(style="whitegrid")
        plt.figure(figsize=(8, 5))
        sns.histplot(y_pred, kde=True, color='blue', bins=20, edgecolor='black')
        plt.title("Distribution of Predicted Salaries", fontsize=16, fontweight='bold')
        plt.xlabel("Predicted Salary (in LPA)", fontsize=14)
        plt.ylabel("Frequency", fontsize=14)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error plotting graphs: {e}")


# Main execution
if __name__ == "__main__":
    try:
        csv_file = "JobOp.csv"
        background_path = "PopUpBG1.png"

        X, y, job_title_le, job_location_le = load_and_preprocess_data(csv_file)

        if X is not None and y is not None:
            train_model(X, y)

            job_data = pd.read_csv(csv_file)
            for _, job_row in job_data.iterrows():
                show_popup(job_row, background_path, job_title_le, job_location_le)
    except Exception as e:
        print(f"An error occurred: {e}")
