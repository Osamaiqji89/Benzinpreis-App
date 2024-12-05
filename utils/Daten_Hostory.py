import zipfile
import pandas as pd
import matplotlib.pyplot as plt

# Funktion zum Laden der Preisdaten aus der ZIP-Datei
def load_prices_from_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        files = zip_ref.namelist()
        print("Gefundene Dateien im Archiv:", files)

        price_df_list = []
        for file in files:
            with zip_ref.open(file) as f:
                price_df_list.append(pd.read_csv(f))
        prices_df = pd.concat(price_df_list, ignore_index=True)

    return prices_df

# Funktion zum Laden der Tankstellen-Daten und Filtern nach PLZ
def load_stations_from_zip(zip_path, plz_prefix):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        files = zip_ref.namelist()
        print("Gefundene Dateien im Stations-Archiv:", files)

        station_df_list = []
        for file in files:
            with zip_ref.open(file) as f:
                station_df_list.append(pd.read_csv(f))
        stations_df = pd.concat(station_df_list, ignore_index=True)

    stations_df = stations_df.drop_duplicates(subset=['uuid'])

    if plz_prefix:
        stations_df['short_plz'] = stations_df['post_code'].astype(str).str[:3]
        filtered_stations = stations_df[stations_df['short_plz'] == plz_prefix]
        return filtered_stations
    return stations_df

# Funktion zur Berechnung der wöchentlichen Durchschnittspreise
def calculate_weekly_avg(prices_df, selected_fuel_type):
    prices_df['date'] = pd.to_datetime(prices_df['date'])
    prices_df.set_index('date', inplace=True)
    weekly_avg_prices = prices_df.resample('W')[selected_fuel_type].mean()
    return weekly_avg_prices

# Funktion zur Darstellung der Preistrends
def plot_price_trend(prices_df, selected_fuel_type, plz_prefix):
    weekly_avg_prices = calculate_weekly_avg(prices_df, selected_fuel_type)
    
    plt.figure(figsize=(10, 6))
    plt.plot(weekly_avg_prices.index, weekly_avg_prices.values, label=f'{selected_fuel_type} Preis', color='blue')
    plt.xlabel('Woche')
    plt.ylabel(f'{selected_fuel_type} Preis in EUR')
    plt.title(f'{selected_fuel_type} Preis im Zeitverlauf (PLZ: {plz_prefix}*)' if plz_prefix else f'{selected_fuel_type} Preis im Zeitverlauf')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

# Funktion zur Auswahl der Spritsorte
def get_fuel_type():
    print("Bitte wählen Sie die Spritsorte:")
    print("1: Diesel")
    print("2: E5")
    print("3: E10")
    choice = input("Geben Sie 1, 2 oder 3 ein: ")

    if choice == '1':
        return 'diesel'
    elif choice == '2':
        return 'e5'
    elif choice == '3':
        return 'e10'
    else:
        print("Ungültige Eingabe. Standardmäßig wird Diesel ausgewählt.")
        return 'diesel'

# Hauptfunktion
def main():
    prices_zip_path = '11.zip'
    stations_zip_path = '11_stations.zip'

    selected_fuel_type = get_fuel_type()

    # Benutzer nach der PLZ fragen (optional)
    plz = input("Geben Sie eine PLZ ein (oder drücken Sie Enter für alle Daten): ")
    plz_prefix = plz[:3] if plz else None

    prices_df = load_prices_from_zip(prices_zip_path)

    # Wenn eine PLZ angegeben wurde, die relevanten Stationen finden
    if plz_prefix:
        stations_df = load_stations_from_zip(stations_zip_path, plz_prefix)
        valid_station_uuids = stations_df['uuid'].unique()
        prices_df = prices_df[prices_df['station_uuid'].isin(valid_station_uuids)]

    if prices_df.empty:
        print("Keine Daten gefunden für die gewählte PLZ oder Kraftstoffart.")
        return

    print(prices_df.head())

    plot_price_trend(prices_df, selected_fuel_type, plz_prefix)

if __name__ == "__main__":
    main()
