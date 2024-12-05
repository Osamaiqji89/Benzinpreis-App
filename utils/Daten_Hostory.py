import zipfile
import pandas as pd
import matplotlib.pyplot as plt

# Funktion zum Laden der Preisdaten aus der ZIP-Datei
def load_prices_from_zip(zip_path):
    # Öffnen des ZIP-Archivs
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Alle Dateien im Archiv auflisten
        files = zip_ref.namelist()
        print(files)

        # Erstellen einer leeren Liste, um die DataFrames zu speichern
        price_df_list = []

        # Durch jede Datei im Archiv iterieren
        for file in files:
            with zip_ref.open(file) as f:
                price_df_list.append(pd.read_csv(f))

        # Alle DataFrames in der Liste zu einem DataFrame zusammenfügen
        prices_df = pd.concat(price_df_list, ignore_index=True)

    return prices_df

# Funktion zur Berechnung der wöchentlichen Durchschnittspreise
def calculate_weekly_avg(prices_df, selected_fuel_type):
    # Sicherstellen, dass das Datum im richtigen Format vorliegt
    prices_df['date'] = pd.to_datetime(prices_df['date'])

    # Setzen des Datums als Index
    prices_df.set_index('date', inplace=True)

    # Berechnung des Durchschnittspreises pro Woche
    weekly_avg_prices = prices_df.resample('W')[selected_fuel_type].mean()

    return weekly_avg_prices

# Funktion zur Darstellung der Preistrends
def plot_price_trend(prices_df, selected_fuel_type):
    # Berechnung des wöchentlichen Durchschnittspreises
    weekly_avg_prices = calculate_weekly_avg(prices_df, selected_fuel_type)

    # Einfache Darstellung der Preistrends im Zeitverlauf (Woche)
    plt.figure(figsize=(10, 6))
    plt.plot(weekly_avg_prices.index, weekly_avg_prices.values, label=f'{selected_fuel_type} Preis', color='blue')
    plt.xlabel('Woche')
    plt.ylabel(f'{selected_fuel_type} Preis in EUR')
    plt.title(f'{selected_fuel_type} Preis im Zeitverlauf (wöchentliche Durchschnittswerte)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

# Funktion zur Auswahl der Spritsorte
def get_fuel_type():
    # Nutzer nach der Spritsorte fragen
    print("Bitte wählen Sie die Spritsorte:")
    print("1: Diesel")
    print("2: E5")
    print("3: E10")
    choice = input("Geben Sie 1, 2 oder 3 ein: ")

    # Rückgabe der gewählten Spritsorte
    if choice == '1':
        return 'diesel'
    elif choice == '2':
        return 'e5'
    elif choice == '3':
        return 'e10'
    else:
        # Standardmäßig Diesel auswählen, wenn die Eingabe ungültig ist
        print("Ungültige Eingabe. Standardmäßig wird Diesel ausgewählt.")
        return 'diesel'

# Hauptfunktion
def main():
    zip_path = '11.zip'

    # Wählen Sie die Spritsorte aus
    selected_fuel_type = get_fuel_type()

    # Lade Preisdaten
    prices_df = load_prices_from_zip(zip_path)

    # Zeige die ersten paar Zeilen der Daten zur Kontrolle
    print(prices_df.head())

    # Zeige die Preisveränderungen für den ausgewählten Kraftstoff an
    plot_price_trend(prices_df, selected_fuel_type)

main()
