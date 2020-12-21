from django.db import models
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Create your models here.
class Cuaca(models.Model):
    title = models.CharField(max_length=200)
    sweat = models.FloatField(default=0)
    cape =  models.FloatField(default=0)
    rh700 = models.FloatField(default=0)

    @property
    def total(self):
        return fuzzy(self)
    
def fuzzy(data):
    # New Antecedent/Consequent objects hold universe variables and membership
    sweat = ctrl.Antecedent(np.arange(0, 266, 1), 'sweat')
    cape = ctrl.Antecedent(np.arange(0, 3251, 1), 'cape')
    rh700 = ctrl.Antecedent(np.arange(0, 76, 1), 'rh700')
    prakiraan = ctrl.Consequent(np.arange(0, 101, 1), 'prakiraan')

    # SWEAT membership
    sweat['lemah'] = fuzz.trapmf(sweat.universe,[0,0,85,145])
    sweat['kuat'] = fuzz.trimf(sweat.universe, [85, 145, 205])
    sweat['sangat kuat'] = fuzz.trapmf(sweat.universe,[145,205,265,265])
    # CAPE membership
    cape['kecil'] = fuzz.trapmf(cape.universe,[0,0,1000,1750])
    cape['besar'] = fuzz.trimf(cape.universe, [1000, 1750, 2500])
    cape['sangat besar'] = fuzz.trapmf(cape.universe,[1750,2500,3250,3250])
    # RH 700 membership
    rh700['sedikit'] = fuzz.trapmf(rh700.universe,[0,0,10,35])
    rh700['sedang'] = fuzz.trimf(rh700.universe, [10, 35, 60])
    rh700['banyak'] = fuzz.trapmf(rh700.universe,[35,60,75,75])
    # Prakiraan membership
    prakiraan['cerah'] = fuzz.trapmf(prakiraan.universe,[0,0,11,44])
    prakiraan['berawan'] = fuzz.trimf(prakiraan.universe, [11, 44, 77])
    prakiraan['hujan'] = fuzz.trapmf(prakiraan.universe,[44,77,100,100])

    # Create Rule
    rule1 = ctrl.Rule(sweat['lemah'] & cape['kecil'] &
                    rh700['sedikit'], prakiraan['cerah'])
    rule2 = ctrl.Rule(sweat['lemah'] & cape['kecil']
                    & rh700['sedang'], prakiraan['cerah'])
    rule3 = ctrl.Rule(sweat['lemah'] & cape['kecil']
                    & rh700['banyak'], prakiraan['berawan'])
    rule4 = ctrl.Rule(sweat['kuat'] & cape['kecil']
                    & rh700['sedikit'], prakiraan['berawan'])
    rule5 = ctrl.Rule(sweat['kuat'] & cape['kecil']
                    & rh700['sedang'], prakiraan['berawan'])
    rule6 = ctrl.Rule(sweat['kuat'] & cape['kecil']
                    & rh700['banyak'], prakiraan['berawan'])
    rule7 = ctrl.Rule(sweat['sangat kuat'] & cape['kecil']
                    & rh700['sedikit'], prakiraan['berawan'])
    rule8 = ctrl.Rule(sweat['sangat kuat'] & cape['kecil']
                    & rh700['sedang'], prakiraan['berawan'])
    rule9 = ctrl.Rule(sweat['sangat kuat'] & cape['kecil']
                    & rh700['banyak'], prakiraan['hujan'])
    rule10 = ctrl.Rule(sweat['lemah'] & cape['besar']
                    & rh700['sedikit'], prakiraan['cerah'])
    rule11 = ctrl.Rule(sweat['lemah'] & cape['besar']
                    & rh700['sedang'], prakiraan['berawan'])
    rule12 = ctrl.Rule(sweat['lemah'] & cape['besar']
                    & rh700['banyak'], prakiraan['berawan'])
    rule13 = ctrl.Rule(sweat['kuat'] & cape['besar']
                    & rh700['sedikit'], prakiraan['berawan'])
    rule14 = ctrl.Rule(sweat['kuat'] & cape['besar']
                    & rh700['sedang'], prakiraan['berawan'])
    rule15 = ctrl.Rule(sweat['kuat'] & cape['besar']
                    & rh700['banyak'], prakiraan['berawan'])
    rule16 = ctrl.Rule(sweat['sangat kuat'] & cape['besar']
                    & rh700['sedikit'], prakiraan['berawan'])
    rule17 = ctrl.Rule(sweat['sangat kuat'] & cape['besar']
                    & rh700['sedang'], prakiraan['berawan'])
    rule18 = ctrl.Rule(sweat['sangat kuat'] & cape['besar']
                    & rh700['banyak'], prakiraan['hujan'])
    rule19 = ctrl.Rule(sweat['lemah'] & cape['sangat besar']
                    & rh700['sedikit'], prakiraan['berawan'])
    rule20 = ctrl.Rule(sweat['lemah'] & cape['sangat besar']
                    & rh700['sedang'], prakiraan['berawan'])
    rule21 = ctrl.Rule(sweat['lemah'] & cape['sangat besar']
                    & rh700['banyak'], prakiraan['hujan'])
    rule22 = ctrl.Rule(sweat['kuat'] & cape['sangat besar']
                    & rh700['sedikit'], prakiraan['berawan'])
    rule23 = ctrl.Rule(sweat['kuat'] & cape['sangat besar']
                    & rh700['sedang'], prakiraan['berawan'])
    rule24 = ctrl.Rule(sweat['kuat'] & cape['sangat besar']
                    & rh700['banyak'], prakiraan['hujan'])
    rule25 = ctrl.Rule(sweat['sangat kuat'] & cape['sangat besar']
                    & rh700['sedikit'], prakiraan['hujan'])
    rule26 = ctrl.Rule(sweat['sangat kuat'] & cape['sangat besar']
                    & rh700['sedang'], prakiraan['hujan'])
    rule27 = ctrl.Rule(sweat['sangat kuat'] & cape['sangat besar']
                    & rh700['banyak'], prakiraan['hujan'])


    prakiraan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12,
                                        rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27])
    prakiraan_cuaca = ctrl.ControlSystemSimulation(prakiraan_ctrl)

    prakiraan_cuaca.input['sweat'] = data.sweat
    prakiraan_cuaca.input['cape'] = data.cape
    prakiraan_cuaca.input['rh700'] = data.rh700
    prakiraan_cuaca.compute()

    hasil = prakiraan_cuaca.output['prakiraan']
    output =""
    if(hasil<44):
        output="Cerah"
    elif (hasil<77):
        output="Berawan"
    else:
        output="Hujan"

    return output

