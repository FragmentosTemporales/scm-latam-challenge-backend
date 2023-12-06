import pandas as pd
from flask import jsonify
from math import ceil
from datetime import timedelta
from app.models import Shift, Forecast, Availability, User


class Set_Availability:
    """Retorna horario de trabajo"""
    def __init__(self, user_id):
        self.periodos = 24
        self.user_id = user_id
        self.user = User.find_by_id(self.user_id)
        self.shift = self.set_shift()
        self.forecast_by_day = self.set_forecast()
        self.dates = self.forecast_by_day['date'].dt.date.unique()

        self.k1 = 1
        self.k2 = 2
        self.W_real = self.user.w_real

        self.set_workforce()
        response = self.set_response()
        self.response_json = response.astype(str).to_dict(orient='records')
        self.set_available()

    def set_shift(self):
        """Genera DF de instancia Shift"""
        shifts_objects = Shift.find_all_by_user_id(self.user_id)
        shifts_dict = {
            'start_shift': [shift.start_shift for shift in shifts_objects],
            'end_shift': [shift.end_shift for shift in shifts_objects],
            'name': [shift.name for shift in shifts_objects],
            'shift_type': [shift.shift_type for shift in shifts_objects],
        }
        shifts_to_df = pd.DataFrame(shifts_dict)
        shifts_to_df['start_shift'] = pd.to_datetime(
            shifts_to_df['start_shift'], format='%H:%M')
        shifts_to_df['end_shift'] = pd.to_datetime(
            shifts_to_df['end_shift'], format='%H:%M')

        tiempo = [(timedelta(
            hours=0,
            minutes=15*i * 96/self.periodos)) for i in range(
                int(self.periodos))]

        shifts_to_df['in'] = shifts_to_df['start_shift'].apply(
            lambda x: tiempo.index(timedelta(hours=x.hour, minutes=x.minute)))
        shifts_to_df['out'] = shifts_to_df['end_shift'].apply(
            lambda x: len(tiempo)
            if x.hour == 0 and x.minute == 0
            else tiempo.index(timedelta(hours=x.hour, minutes=x.minute)))
        shifts_to_df['lenght'] = shifts_to_df['out'] - shifts_to_df['in']
        return shifts_to_df

    def set_forecast(self):
        """"Genera DF de instancia Forecast"""
        forecasts_objects = Forecast.find_all_by_user_id(self.user_id)

        forecasts_dict = {
            'date': [forecast.date for forecast in forecasts_objects],
            'demand': [forecast.demand for forecast in forecasts_objects]
        }
        forecast_df = pd.DataFrame(forecasts_dict)
        forecast_df['date'] = forecast_df['date'].astype('datetime64[ns]')
        forecast_df['week'] = forecast_df['date'].dt.isocalendar().week
        forecast_df['day'] = forecast_df['date'].dt.isocalendar().day

        return forecast_df

    def set_workforce(self):
        """Retorna str por consola """
        max_wf_wk = self.forecast_by_day.query('day==7 or day==6')['demand'].max()
        b1 = ceil((self.k2 * max_wf_wk) / (self.k2-self.k1))
        D_week = 0

        for w in self.forecast_by_day['week'].unique():
            d = self.forecast_by_day[self.forecast_by_day['week']==w]['demand'].to_list()
            D = 0
            for i in d:
                D += i
            if D > D_week:
                D_week = D

        b2 = ceil(D/5)
        b3 = self.forecast_by_day['demand'].max()
        W = max(b1,b2,b3)

        print(f"Minimum workforce: {W}")

        if self.W_real > W:
            print("Workforce is enough, surplus: ", self.W_real-W)
            free_wf_wk = ceil(self.W_real*self.k1/self.k2)
        else:
            print("Workforce is not enough, deficit: ", W-self.W_real)
            free_wf_wk = ceil(self.W_real*self.k1/self.k2)

        print(f"Workforce free by Weekend: {free_wf_wk}")

    def set_response(self):
        """Generamos DF"""
        max_demanda_per_weekend = {w:self.forecast_by_day[self.forecast_by_day['week']==w].query('day==7 or day==6')['demand'].max() for w in self.forecast_by_day['week'].unique()}
        self.forecast_by_day['surplus'] = self.forecast_by_day.apply(lambda row: self.W_real - row['demand'] if row['day'] not in [6, 7] else self.W_real - max_demanda_per_weekend[row['week']], axis=1)

        max_dda_wk = self.forecast_by_day[(self.forecast_by_day['day']==7) | (self.forecast_by_day['day']==6)]['demand'].max()

        # Caso 1:2
        collab_list = [i for i in range(self.W_real)]
        collab_list_wknd = [collab_list[:int(len(collab_list)/2)], collab_list[int(len(collab_list)/2):]]
        collab_list_wknd = collab_list_wknd*2

        free_wknd_collab = {}
        for w, cs in zip(max_demanda_per_weekend, collab_list_wknd):
            free_wknd_collab[w] = cs

        def two_highest_keyvalue(dicc):
            dicc_copy = dict(dicc)
            key1 = max(dicc_copy, key=dicc_copy.get)
            del dicc_copy[key1]
            key2 = max(dicc_copy, key=dicc_copy.get)
            return [key1, key2]
        
        data = []
        for c in collab_list:
            for fecha in self.dates:
                data.append([c, fecha])

        df_availability = pd.DataFrame(data, columns=['collaborator', 'date'])
        df_availability['availability'] = 1
        df_availability['date'] = df_availability['date'].astype('datetime64[ns]')
        df_availability['week'] = df_availability['date'].dt.isocalendar().week
        df_availability['day'] = df_availability['date'].dt.isocalendar().day

        for w in free_wknd_collab: # Dar domingo libres
            for c in free_wknd_collab[w]:
                filtro = (df_availability["collaborator"] == c) & (df_availability["day"] == 7) & (df_availability["week"] == w)
                df_availability.loc[filtro, "availability"] = 0

        day_off_by_week = {}

        for wk in  free_wknd_collab: # Pares días libres
            surplus_week = self.forecast_by_day[(self.forecast_by_day['week']==wk) & (self.forecast_by_day['day']!=7)][['day','surplus']].set_index('day').to_dict()['surplus']
            day_off_pairs = []
            for j in range(len(collab_list) - len(free_wknd_collab[wk])):
                keys = two_highest_keyvalue(surplus_week)
                surplus_week[keys[0]] -= 1
                surplus_week[keys[1]] -= 1
                day_off_pairs.append(keys)

            day_off_by_week[wk] = day_off_pairs

        for wk in day_off_by_week:  # Dar libres entre semana
            j = 0
            for c in collab_list:
                if df_availability[
                    (df_availability['collaborator'] == c) & (df_availability['week'] == wk)]['availability'].sum() == 7:
                    days_off = day_off_by_week[wk][j]

                    if days_off[0] <= max_dda_wk and days_off[1] <= max_dda_wk:
                        filter1 = (df_availability['collaborator'] == c) & (df_availability['week'] == wk) & (
                                df_availability['day'] == days_off[0])
                        filter2 = (df_availability['collaborator'] == c) & (df_availability['week'] == wk) & (
                                df_availability['day'] == days_off[1])
                        df_availability.loc[filter1, "availability"] = 0
                        df_availability.loc[filter2, "availability"] = 0
                        j += 1

        return df_availability

    def set_available(self):
        for record in self.response_json:
            availability_instance = Availability(
                collaborator=record['collaborator'],
                date=record['date'],
                is_available=int(record['availability']),
                week=int(record['week']),
                day=int(record['day']),
                user_id=int(self.user_id)
            )
            availability_instance.save_to_db()
            print("Guardado correctamente: ", record)
