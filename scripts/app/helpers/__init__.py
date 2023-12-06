import json
from app.models import Shift, Forecast, Availability


class Installer():
    """Helper to install default info"""
    def __init__(self):
        self.shift_data = self.load_data('app/data/shifts.json')
        self.forecast_data = self.load_data('app/data/forecast.json')
        self.save_shifts()
        self.save_forecasts()

    def load_data(self, url):
        with open(url, 'r') as f:
            data = json.load(f)
        return data

    def save_shifts(self):
        print("INICIAMOS CARGA DE HORARIOS...")
        count = 0
        for shift in self.shift_data:
            shift_instance = Shift(
                name=shift['name'],
                start_shift=shift['start_shift'],
                end_shift=shift['end_shift'],
                shift_type=shift['shift_type'],
                user_id=shift['user_id']
            )
            shift_instance.save_to_db()
            count += 1
        print(f"Proceso terminado, {count} objetos procesados.")

    def save_forecasts(self):
        print("INICIAMOS CARGA DE DEMANDAS...")
        count = 0
        for forecast in self.forecast_data:
            forecast_instance = Forecast(
                date=forecast['date'],
                demand=forecast['demand'],
                user_id=forecast['user_id']
            )
            forecast_instance.save_to_db()
            count += 1
        print(f"Proceso terminado, {count} objetos procesados.")


class Deleter():
    """Helper to uninstall data info"""
    def __init__(self):
        self.shift_data = Shift.find_all_by_user_id(1)
        self.forecast_data = Forecast.find_all_by_user_id(1)
        self.availability_data = Availability.find_all_by_user_id(1)
        print("ELIMINANDO HORARIOS...")
        self.delete_shifts()
        print("ELIMINANDO DEMANDAS...")
        self.delete_forecasts()
        print("ELIMINANDO TURNOS...")
        self.delete_availability()

    def delete_shifts(self):
        count = 0
        for shift in self.shift_data:
            shift.delete_from_db()
            count += 1
        print(f"{count} registros eliminados.")

    def delete_forecasts(self):
        count = 0
        for forecast in self.forecast_data:
            forecast.delete_from_db()
            count += 1
        print(f"{count} registros eliminados.")

    def delete_availability(self):
        count = 0
        for availability in self.availability_data:
            availability.delete_from_db()
            count += 1
        print(f"{count} registros eliminados.")
