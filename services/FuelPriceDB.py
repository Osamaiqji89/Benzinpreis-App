import sqlite3
import os
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple
from utils.StatusLogger import StatusLogger

class FuelPriceDB:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources/Database/fuel_prices.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def add_to_favorites(self, station_id):
        try:
            self.cursor.execute('INSERT OR REPLACE INTO favorites (station_id) VALUES (?)', (station_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding favorite: {e}")
            return False

    def remove_from_favorites(self, station_id):
        try:
            self.cursor.execute('DELETE FROM favorites WHERE station_id = ?', (station_id,))
            self.cursor.execute('DELETE FROM favorites WHERE station_id = ""')

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error removing favorite: {e}")
            return False

    def is_favorite(self, station_id):
        self.cursor.execute('SELECT station_id FROM favorites WHERE station_id = ?', (station_id,))
        return self.cursor.fetchone() is not None

    def get_favorite_stations(self):
        self.cursor.execute('SELECT station_id FROM favorites')
        return [row[0] for row in self.cursor.fetchall()]

    def get_monthly_averages(self, year: int = None) -> Dict[str, Dict[str, List[Tuple[str, float]]]]:
        """
        Get monthly average prices for all fuel types.
        Args:
            year: Optional year to filter results. If None, returns all years.
        Returns:
            Dictionary with format:
            {
                'diesel': {
                    '2021': [(month_name, price), ...],
                    '2022': [(month_name, price), ...],
                    ...
                },
                'e5': { ... },
                'e10': { ... }
            }
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            year_condition = "AND strftime('%Y', date) = ?" if year else ""
            params = (year,) if year else ()
            
            query = f'''
                WITH monthly_data AS (
                    SELECT 
                        strftime('%Y', date) as year,
                        strftime('%m', date) as month,
                        strftime('%m', date) as month_num,
                        CASE strftime('%m', date)
                            WHEN '01' THEN 'Januar'
                            WHEN '02' THEN 'Februar'
                            WHEN '03' THEN 'März'
                            WHEN '04' THEN 'April'
                            WHEN '05' THEN 'Mai'
                            WHEN '06' THEN 'Juni'
                            WHEN '07' THEN 'Juli'
                            WHEN '08' THEN 'August'
                            WHEN '09' THEN 'September'
                            WHEN '10' THEN 'Oktober'
                            WHEN '11' THEN 'November'
                            WHEN '12' THEN 'Dezember'
                        END as month_name,
                        AVG(diesel) as diesel_avg,
                        AVG(e5) as e5_avg,
                        AVG(e10) as e10_avg,
                        COUNT(*) as days_count
                    FROM daily_prices
                    WHERE 1=1 {year_condition}
                    GROUP BY year, month
                    ORDER BY year, month
                )
                SELECT 
                    year,
                    month_name,
                    month_num,
                    ROUND(diesel_avg, 3) as diesel_price,
                    ROUND(e5_avg, 3) as e5_price,
                    ROUND(e10_avg, 3) as e10_price,
                    days_count
                FROM monthly_data
            '''
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Organize data by fuel type and year
            averages = {
                'diesel': {},
                'e5': {},
                'e10': {}
            }
            
            for row in results:
                year, month_name, month_num, diesel, e5, e10, days = row
                
                # Initialize year dictionaries if they don't exist
                for fuel_type in averages:
                    if year not in averages[fuel_type]:
                        averages[fuel_type][year] = []
                
                # Add monthly averages for each fuel type
                averages['diesel'][year].append((month_name, diesel))
                averages['e5'][year].append((month_name, e5))
                averages['e10'][year].append((month_name, e10))
            
            return averages

    def get_all_prices(self) -> Dict[str, Dict[str, List[float]]]:
        """
        Get monthly average prices in the format expected by the plotting function.
        Returns:
            Dictionary with format:
            {
                'diesel': {
                    '2021': [price1, price2, ..., price12],
                    '2022': [price1, price2, ..., price12],
                    ...
                },
                'e5': { ... },
                'e10': { ... }
            }
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT 
                    strftime('%Y', date) as year,
                    strftime('%m', date) as month,
                    fuel_type,
                    ROUND(AVG(price), 3) as avg_price
                FROM (
                    SELECT date, 'diesel' as fuel_type, diesel as price FROM daily_prices WHERE diesel IS NOT NULL
                    UNION ALL
                    SELECT date, 'e5' as fuel_type, e5 as price FROM daily_prices WHERE e5 IS NOT NULL
                    UNION ALL
                    SELECT date, 'e10' as fuel_type, e10 as price FROM daily_prices WHERE e10 IS NOT NULL
                )
                GROUP BY year, month, fuel_type
                ORDER BY year, month, fuel_type
            '''
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            prices_dict = {'diesel': {}, 'e5': {}, 'e10': {}}
            
            for year, month, fuel_type, avg_price in results:
                if year not in prices_dict[fuel_type]:
                    prices_dict[fuel_type][year] = [0] * 12
                month_idx = int(month) - 1
                prices_dict[fuel_type][year][month_idx] = avg_price
            
            return prices_dict

    def get_daily_prices(self, year: int = None, month: int = None) -> List[Tuple[str, float, float, float]]:
        """
        Get daily prices for all fuel types.
        Args:
            year: Optional year to filter results
            month: Optional month to filter results (1-12)
        Returns:
            List of tuples (date, diesel_price, e5_price, e10_price)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            conditions = []
            params = []
            
            if year:
                conditions.append("strftime('%Y', date) = ?")
                params.append(str(year))
            if month:
                conditions.append("strftime('%m', date) = ?")
                params.append(f"{month:02d}")
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            query = f'''
                SELECT 
                    date,
                    ROUND(diesel, 3) as diesel_price,
                    ROUND(e5, 3) as e5_price,
                    ROUND(e10, 3) as e10_price
                FROM daily_prices
                WHERE {where_clause}
                ORDER BY date
            '''
            
            cursor.execute(query, params)
            return cursor.fetchall()
            
    def load_prices_from_db(self, stations_df=None, fuel_type=None):
        """
        Load price data from the database
        Args:
            stations_df: Optional DataFrame containing station data to filter prices by
        Returns:
            pandas.DataFrame: DataFrame containing price data
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            if stations_df is not None and not stations_df.empty:
                # Get list of station UUIDs
                station_uuids = stations_df['uuid'].unique()
                station_uuids_str = ','.join(f"'{uuid}'" for uuid in station_uuids)
                
                # Query with station filter
                query = f"""
                    SELECT p.id, p.date, p.station_uuid, p.{fuel_type}
                    FROM prices p
                    WHERE p.station_uuid IN ({station_uuids_str})
                """
            else:
                # Query without filter
                query = "SELECT * FROM prices"
            
            prices_df = pd.read_sql_query(query, conn)
            conn.close()
            #print(f"Loaded {len(prices_df)} rows from prices table.")
            StatusLogger.log(f"Loaded {len(prices_df)} rows from prices table.")
            return prices_df
        except Exception as e:
            #print(f"Error loading prices from database: {e}")
            StatusLogger.error(f"Error loading prices from database: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()

    def load_stations_from_db(self, plz_prefix=None):
        """
        Load station data from the database and filter by postal code prefix
        Args:
            db_path: Path to the SQLite database
            plz_prefix: First 3 digits of postal code to filter by (optional)
        Returns:
            pandas.DataFrame: DataFrame containing filtered station data
        """
        try:
            conn = sqlite3.connect(self.db_path)
            query = "SELECT * FROM stations"
            stations_df = pd.read_sql_query(query, conn)
            conn.close()
            #print(f"Loaded {len(stations_df)} rows from stations table.")
            StatusLogger.log(f"Loaded {len(stations_df)} rows from stations table.")
            
            if plz_prefix:
                stations_df['plz_str'] = stations_df['post_code'].astype(str).str.zfill(5)
                stations_df = stations_df[stations_df['plz_str'].str.startswith(str(plz_prefix))]
                #print(f"Rows after filtering by PLZ {plz_prefix}: {len(stations_df)}")
                StatusLogger.log(f"Rows after filtering by PLZ {plz_prefix}: {len(stations_df)}")
            
            return stations_df
        except Exception as e:
            #print(f"Error loading stations from database: {e}")
            StatusLogger.error(f"Error loading stations from database: {e}")
            return pd.DataFrame()