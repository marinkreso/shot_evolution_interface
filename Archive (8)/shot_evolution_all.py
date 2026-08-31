from nicegui import ui, run
from report_util_all import main2
from PIL import Image

good_sinner = [
 'AO_2024_F_Sinner_Medvedev',
 'AO_2024_QF_Sinner_Rublev',
 'AO_2024_R16_Sinner_Khachanov',
 'AO_2024_R32_Sinner_Baez',
 'AO_2024_SF_Djokovic_Sinner',
 'Indian_Wells_2024_QF_Lehecka_Sinner',
 'Indian_Wells_2024_R16_Shelton_Sinner',
 'Indian_Wells_2024_R32_Struff_Sinner',
 'Indian_Wells_2024_R64_Kokkinakis_Sinner',
 'Indian_Wells_2024_SF_Sinner_Alcaraz',
 'Miami_2024_R32_Griekspoor_Sinner',
 'Miami_2024_R64_Vavassori_Sinner',
 'Rogers_cup_2021_R32_Duckworth_Sinner',
 'Rogers_cup_2022_2nd_Sinner_Mannarino',
 'Rogers_cup_2022_3rd_Sinner_Carreno-Busta',
 'Rotterdam_2024_F_Sinner_de-Minaur',
 'Rotterdam_2024_QF_Sinner_Raonic',
 'Rotterdam_2024_R16_Sinner_Monfils',
 'Rotterdam_2024_R32_Sinner_van-de-Zandschulp',
 'Rotterdam_2024_SF_Sinner_Griekspoor']
bad_sinner = ['AO_2022_QF_Tsitsipas_Sinner',
    'ATP_cup_2022_RR_Sinner_Purcell',
 'Rome_2021_R64_Humbert_Sinner',
 'Rome_2023_R64_Kokkinakis_Sinner',
 'AO_2022_1st_Sinner_Sousa',
 'Madrid_2022_R64_Paul_Sinner',
 'Indian_Wells_2022_R64_Sinner_Djere',
 'Rome_2023_R16_Cerundolo_Sinner',
 'Rome_2022_QF_Sinner_Tsitsipas',
 'Rome_2022_R32_Fognini_Sinner',
 'Cincinnati_2022_3rd_Auger-Aliassime_Sinner',
 'US_Open_2022_QF_Sinner_Alcaraz',
 'Indian_Wells_2021_R16_Fritz_Sinner',
 'Madrid_2021_R32_Popyrin_Sinner',
 'ATP_cup_2022_RR_Sinner_Rinderknech',
 'AO_2022_4th_Sinner_Minaur',
 'Monte-Carlo_2023_QF_Musetti_Sinner',
 'Dubai_2022_2nd_Murray_Sinner',
 'Indian_Wells_2021_R64_Millman_Sinner',
 'US_Open_2022_1st_Altmaier_Sinner',
 'Rome_2021_R32_Sinner_Nadal',
 'Monte-Carlo_2023_R16_Hurkacz_Sinner',
 'Montpellier_2023_QF_Sonego_Sinner',
 'Miami_2022_R32_Carreno_Busta_Sinner',
 'Indian_Wells_2022_R32_Sinner_Bonzi',
 'Montpellier_2023_F_Cressy_Sinner',
 'Monte_Carlo_2021_R64_Ramos-Vinolas_Sinner',
 'Miami_2021_R64_Sinner_Gaston',
 'Madrid_2022_R16_Auger-Aliassime_Sinner',
 'US_Open_2022_4th_Ivashka_Sinner',
 'Miami_2021_F_Sinner_Hurkacz',
 'AO_2022_3rd_Sinner_Daniel',
 'Cincinnati_2021_R32_Sinner_Isner',
 'Cincinnati_2022_2nd_Kecmanovic_Sinner',
 'Stockholm_2021_2nd_Sinner_Murray',
 'Cincinnati_2021_R64_Sinner_Delbonis',
 'Monte_Carlo_2021_R32_Djokovic_Sinner',
 'Monte-Carlo_2023_R32_Schwartzman_Sinner',
 'Miami_2021_QF_Sinner_Bublik',
 'Rome_2020_R2_SINNER_TSITSIPAS',
 'Miami_2022_R64_Ruusuvuori_Sinner',
 'Miami_2022_QF_Sinner_Cerundolo',
 'Miami_2021_SF_Bautista_Agut_Sinner',
 'Miami_2022_R16_Kyrgios_Sinner',
 'ATP_cup_2022_RR_Sinner_Safiullin',
 'US_Open_2022_2nd_Eubanks_Sinner',
 'Madrid_2021_R64_Pella_Sinner',
 'Monte_Carlo_2022_QF_Sinner_Zverev',
 'Paris_2021_R32_Sinner_Alcaraz',
 'Rome_2022_R16_Krajinovic_Sinner',
 'Madrid_2022_R32_de_Minaur_Sinner',
 'Sofia_2022_SF_Sinner_Rune',
 'Monte_Carlo_2022_R16_Rublev_Sinner',
 'RG_2020_R4_ZVEREV_SINNER',
 'RG_2023_R64_Sinner_Altmaier',
 'Monte-Carlo_2023_2022_SF_Sinner_Rune',
 'Miami_2021_R16_Ruusuvuori_Sinner',
 'Montpellier_2023_SF_Fils_Sinner',
 'Rome_2022_R64_Martinez_Sinner',
 'Monte_Carlo_2022_R32_Ruusuvuori_Sinner',
 'Rome_2023_R32_Shevchenko_Sinner',
 'Cincinnati_2022_1st_Kokkinakis_Sinner',
 'Miami_2021_R32_Sinner_Khachanov',
 'Monte_Carlo_2022_R64_Coric_Sinner',
 'US_Open_2022_3rd_Nakashima_Sinner',
 'AO_2022_2nd_Sinner_Johnson']

data = {
  
  'SEYBOTH_WILD_evolution': [
            {'player': 'SEYBOTH WILD', 'year': '2024', 'tournaments': ['MADRID', 'ROME'], 'name': 'CLAY 2024'},  

        {'player': 'SEYBOTH WILD', 'year': '2024', 'tournaments': ['MIAMI', 'INDIAN'], 'name': 'MIAMI + INDIAN WELLS 2024'},  
                                {'player': 'SEYBOTH WILD', 'year': '2024', 'tournaments': ['Adelaide'], 'name': 'ADELAIDE 2024'}, 

                {'player': 'SEYBOTH WILD', 'year': '2023', 'tournaments': ['Stockholm', 'Basel', 'Paris'], 'name': 'POST US-OPEN 2023'}, 


    ],
    
'GAUFF_post_miami_won_vs_lost': [
    {'player': 'GAUFF', 'matches': ['Madrid_2024_R16_Gauff_Keys', 'Berlin_2024_SF_Gauff_Pegula', 'Rome_2024_SF_Swiatek_Gauff', 'RG_2024_SF_Swiatek_Gauff'], 'name': 'LOST MATCHES'},
    {'player': 'GAUFF', 'matches': ['Madrid_2024_R32_Gauff_Yastremska',
 'Madrid_2024_R64_Gauff_Rus',
 'RG_2024_1st_Gauff_Avdeeva',
 'RG_2024_QF_Gauff_Jabeur',
 'RG_2024_R16_Gauff_Cocciaretto',
 'RG_2024_R32_Gauff_Yastremska',
 'RG_2024_R64_Gauff_Zidansek',
 'Rome_2024_QF_Gauff_Zheng',
 'Rome_2024_R16_Gauff_Badosa',
 'Rome_2024_R32_Gauff_Cristian',
 'Rome_2024_R64_Gauff_Frech'], 'name': 'WON MATCHES'}],
    
'TSITSIPAS_grass_comparison': [
    {'player': 'TSITSIPAS', 'matches': ['Wimbledon_2024_R64_Ruusuvuori_Tsitsipas'], 'name': 'WIMBLEDON 2024 R2'},
    {'player': 'TSITSIPAS', 'matches': ['Wimbledon_2024_1st_Daniel_Tsitsipas'], 'name': 'WIMBLEDON 2024 R1'},
    {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['Stuttgart', 'Halle', 'Wimbledon'], 'name': 'WIMBLEDON 2024 ALL'},  
    {'player': 'TSITSIPAS', 'year': '2023', 'tournaments': ['Stuttgart', 'Halle', 'Wimbledon'], 'name': 'GRASS 2023'},
    {'player': 'TSITSIPAS', 'year': '2022', 'tournaments': ['Stuttgart', 'Halle', 'Wimbledon'], 'name': 'GRASS 2022'},
     {'player': 'TSITSIPAS', 'matches': ['United_Cup_2024_R32_Tsitsipas_Zverev',
 'United_Cup_2024_R64_Tsitsipas_Diez',
 'AO_2024_1st_Bergs_Tsitsipas',
 'AO_2024_R16_Fritz_Tsitsipas',
 'AO_2024_R64_Thompson_Tsitsipas',
 'Acapulco_2024_QF_de-Minaur_Tsitsipas',
 'Acapulco_2024_R16_Cobolli_Tsitsipas',
 'Acapulco_2024_R32_Safiullin_Tsitsipas',
 'Los_Cabos_2024_QF_Kovacevic_Tsitsipas',
 'Los_Cabos_2024_R16_Vukic_Tsitsipas',
 'Los_Cabos_2024_SF_Ruud_Tsitsipas',
 'Indian_Wells_2024_R16_Lehecka_Tsitsipas',
 'Indian_Wells_2024_R32_Tiafoe_Tsitsipas',
 'Indian_Wells_2024_R64_Pouille_Tsitsipas'], 'name': 'HARD 2024'}
 
 ],

    'ALTMAIER_comparison': [
      {'player': 'ALTMAIER', 'matches': ['Brisbane_2024_1st_Tu_Altmaier',
 'AO_2024_1st_Altmaier_Khachanov',
 'Brisbane_2024_R64_Altmaier_Dimitrov',
 'Acapulco_2024_R16_Altmaier_Kecmanovic',
 'Acapulco_2024_R32_Zverev_Altmaier',
 'Indian_Wells_2024_1st_Pouille_Altmaier',
 ], 'name': 'HARD 2024'},  
 {'player': 'ALTMAIER', 'name': 'HARD 2023', 'matches': ['Acapulco_2023_R32_Altmaier_Nakashima',
 'Beijing_2023_Q_Harris_Altmaier',
 'Cincinnati_2023_Q_Altmaier_Moutet',
 "Cincinnati_2023_Q_Altmaier_O'Connell",
 'Cincinnati_2023_R64_Popyrin_Altmaier',
 'Dallas_2023_R16_Isner_Altmaier',
 'Dallas_2023_R32_Svajda_Altmaier',
 'Delray-Beach_2023_R32_Altmaier_Mannarino',
 'Miami_2023_1st_Ivashka_Altmaier',
 'Miami_2023_Q_Altmaier_Blancaneaux',
 'Miami_2023_Q_Altmaier_Damm',
 'Paris_2023_R64_Altmaier_Fils',
 'Paris_2023_RR_Altmaier_Rune',
 'Shanghai_2023_1st_Altmaier_Nishioka',
 'Vienna_2023_R32_Monfils_Altmaier']},
            {'player': 'ALTMAIER', 'year': '2024', 'tournaments': ['MADRID', 'ROME', 'MONTE', 'RG_'], 'name': 'CLAY 2024'},  
            {'player': 'ALTMAIER', 'year': '2023', 'tournaments': ['MADRID', 'ROME', 'MONTE', 'RG_'], 'name': 'CLAY 2023'}, 
            {'player': 'SINNER', 'year': '2023', 'tournaments': ['MADRID', 'ROME', 'MONTE', 'RG_'], 'name': 'CLAY 2023'}, 
             {'player': 'DIMITROV', 'name': 'HARD 2023-2024', 'matches': ['Beijing_2023_QF_Dimitrov_Sinner',
 'Indian-Wells_2023_R64_Kubler_Dimitrov',
 'Miami_2023_R32_Sinner_Dimitrov',
 'Miami_2023_R64_Struff_Dimitrov',
 'Paris_2023_SF_Dimitrov_Tsitsipas',
 'United_Cup_2023_RR_Tsitsipas_Dimitrov',
 'AO_2024_R32_Dimitrov_Borges',
 'Brisbane_2024_QF_Rune_Dimitrov',
 'Brisbane_2024_R16_Thompson_Dimitrov',
 'Brisbane_2024_R32_Hijikata_Dimitrov',
 'Brisbane_2024_R64_Altmaier_Dimitrov']}, 
 {'player': 'TSITSIPAS', 'matches': ['AO_2023_1st_Tsitsipas_Halys',
 'AO_2023_4th_Sinner_Tsitsipas',
 'AO_2023_F_Tsitsipas_Djokovic',
 'AO_2023_QF_Tsitsipas_Lehecka',
 'AO_2023_SF_Tsitsipas_Khachanov',
 'Antwerp_2023_QF_Tsitsipas_Hanfmann',
 'Antwerp_2023_R16_Tsitsipas_van-de-Zandschulp',
 'Antwerp_2023_SF_Tsitsipas_Fils',
 'Beijing_2023_R32_Jarry_Tsitsipas',
 'Cincinnati_2023_R16_Tsitsipas_Hurkacz',
 'Cincinnati_2023_R32_Tsitsipas_Shelton',
 'Indian-Wells_2023_R64_Thompson_Tsitsipas',
 'Los_Cabos_2023_F_Tsitsipas_de-Minaur',
 'Los_Cabos_2023_QF_Tsitsipas_Jarry',
 'Los_Cabos_2023_R16_Tsitsipas_Isner',
 'Los_Cabos_2023_SF_Tsitsipas_Coric',
 'Miami_2023_R16_Khachanov_Tsitsipas',
 'Miami_2023_R32_Garin_Tsitsipas',
 'Monte-Carlo_2023_QF_Fritz_Tsitsipas',
 'Monte-Carlo_2023_R16_Jarry_Tsitsipas',
 'Monte-Carlo_2023_R32_Bonzi_Tsitsipas',
 'Paris_2023_QF_Tsitsipas_Khachanov',
 'Paris_2023_R16_Tsitsipas_Zverev',
 'Paris_2023_R32_Tsitsipas_Auger-Aliassime',
 'Paris_2023_SF_Dimitrov_Tsitsipas',
 'Rogers-cup_2023_R32_Tsitsipas_Monfils',
 'Rotterdam_2023_1st_Tsitsipas_Ruusuvuori',
 'Rotterdam_2023_2nd_Tsitsipas_Sinner',
 'Shanghai_2023_R32_Tsitsipas_Humbert',
 'Shanghai_2023_R64_Tsitsipas_Hijikata',
 'Turin_2023_RR_Sinner_Tsitsipas',
 'US_Open_2023_1st_Tsitsipas_Raonic',
 'US_Open_2023_R64_Tsitsipas_Stricker',
 'United_Cup_2023_RR_Tsitsipas_Dimitrov',
 'United_Cup_2023_RR_Tsitsipas_Goffin',
 'United_Cup_2023_SF_Tsitsipas_Berrettini',
 'Vienna_2023_QF_Tsitsipas_Gojo',
 'Vienna_2023_R16_Tsitsipas_Machac',
 'Vienna_2023_R32_Tsitsipas_Thiem',
 'Vienna_2023_SF_Medvedev_Tsitsipas'], 'name': 'HARD 2024'},  
            

            



    ],
'PAUL_HARD_AND_ALCARAZ': [
    {'player': 'PAUL', 'matches': ['Acapulco_2024_R32_Draper_Paul',
'Adelaide_2024_R64_Paul_Bolt',
'Dallas_2024_F_Giron_Paul',
'Dallas_2024_QF_Koepfer_Paul',
'Dallas_2024_R16_Daniel_Paul',
'Dallas_2024_SF_Shelton_Paul',
'Delray_Beach_2024_F_Fritz_Paul',
'Delray_Beach_2024_QF_Thompson_Paul',
'Delray_Beach_2024_R16_Michelsen_Paul',
'Delray_Beach_2024_SF_Paul_Tiafoe',
'Indian_Wells_2024_QF_Paul_Ruud',
'Indian_Wells_2024_R16_Nardi_Paul',
'Indian_Wells_2024_R32_Paul_Humbert',
'Indian_Wells_2024_R64_Paul_Michelsen',
'Indian_Wells_2024_SF_Paul_Medvedev',
'Madrid_2024_R32_Paul_Cerundolo',
'Madrid_2024_R64_Paul_Klein',
'Miami_2024_R64_Paul_Damm'
], 'name': 'HARD 2024'},
    {'player': 'PAUL', 'matches': ['Acapulco_2023_F_Paul_De-Minaur', 'Acapulco_2023_QF_Mcdonald_Paul',
       'Acapulco_2023_R32_Gomez_Paul', 'Acapulco_2023_SF_Paul_Fritz',
       "Adelaide2_2023_R32_Paul_O'Connell", 'Adelaide_2024_R64_Paul_Bolt',
       'Beijing_2023_R32_Paul_Medvedev',
       'Cincinnati_2023_R32_Humbert_Paul',
       'Cincinnati_2023_R64_Kecmanovic_Paul',
       'Delray-Beach_2023_QF_Albot_Paul',
       'Delray-Beach_2023_R16_Kudla_Paul',
       'Eastbourne_2023_F_Cerundolo_Paul', 'Eastbourne_2023_QF_Wolf_Paul',
       'Eastbourne_2023_R16_Baez_Paul', 'Eastbourne_2023_SF_Barrere_Paul',
       'Indian-Wells_2023_R16_Paul_Auger-Aliassime',
       'Indian-Wells_2023_R32_Hurkacz_Paul',
       'Indian-Wells_2023_R64_Struff_Paul',
       'Los-Cabos_2023_QF_De-Minaur_Paul',
       'Los-Cabos_2023_R16_Meligeni-Alves_Paul',
       'Miami_2023_R32_Davidovich-Fokina_Paul',
       'Miami_2023_R64_Huesler_Paul',
       'Paris_2023_R32_Paul_van-de-Zandschulp',
       'Paris_2023_R64_Paul_Gasquet', 'Rogers-cup_2023_QF_Alcaraz_Paul',
       'Rogers-cup_2023_R16_Paul_Giron',
       'Rogers-cup_2023_R32_Paul_Cerundolo',
       'Rogers-cup_2023_R64_Paul_Schwartzman',
       'Rogers-cup_2023_SF_Paul_Sinner', 'Shanghai_2023_R16_Paul_Rublev',
       'Shanghai_2023_R32_Paul_Fils', 'Shanghai_2023_R64_Paul_Ofner',
       'US_Open_2023_1st_Paul_Travaglia', 'US_Open_2023_R16_Paul_Shelton',
       'US_Open_2023_R32_Paul_Davidovich-Fokina',
       'US_Open_2023_R64_Paul_Safiullin'], 'name': 'HARD 2023'},
    {'player': 'PAUL', 'matches': ['Rogers-cup_2023_QF_Alcaraz_Paul', 'Miami_2023_R16_Alcaraz_Paul', 'Cincinnati_2023_R16_Alcaraz_Paul'], 'name': 'VS ALCARAZ HARD 2023'},
],

    'PAVLYUCHENKOVA_evolution': [
            {'player': 'PAVLYUCHENKOVA', 'year': '2023', 'tournaments': ['MADRID', 'ROME'], 'name': 'CLAY 2023'},  
            {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['MADRID', 'ROME'], 'name': 'CLAY 2024'},  
                        {'player': 'PAVLYUCHENKOVA', 'year': '2023', 'tournaments': ['CINCI'], 'name': 'HARD 2023'},  

            {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['MIAMI', 'INDIAN'], 'name': 'MIAMI + INDIAN WELLS 2024'},  
    ],

    'DRAPER_234': [  
                      {'player': 'DRAPER', 'year': '2024', 'tournaments': ['Stuttgart', 'Queens'], 'name': 'GRASS 2024'}, 
                    {'player': 'DRAPER', 'year': '2023', 'tournaments': ['INDIAN', 'ADELAIDE'], 'name': 'HARD 2023'},
                    {'player': 'DRAPER', 'year': '2022', 'tournaments': ['Wimbledon'], 'name': 'GRASS 2022'},  
                      ],
 'BADOSA_234clay': [  
                      {'player': 'BADOSA', 'year': '2024', 'tournaments': ['ROME'], 'name': 'ROME 2024'}, 
                    {'player': 'BADOSA', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'},
                    {'player': 'BADOSA', 'year': '2023', 'tournaments': ['ROME'], 'name': 'ROME 2023'},  
                    {'player': 'BADOSA', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                      ],

    'TSITSIPAS_234clay': [  
                    {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'TSITSIPAS', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'TSITSIPAS', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
'PAUL_234clay': [  
                    {'player': 'PAUL', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'PAUL', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'PAUL', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'PAUL', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
'SINNER_234clay': [  
                    {'player': 'SINNER', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'SINNER', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'SINNER', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
'SINNER_2345clay': [  
                    {'player': 'SINNER', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                     {'player': 'SINNER', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'SINNER', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'SINNER', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
'KECMANOVIC_234clay': [  
                    {'player': 'KECMANOVIC', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'KECMANOVIC', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'KECMANOVIC', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'KECMANOVIC', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
'ALTMAIER_234clay': [  
                    {'player': 'ALTMAIER', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'ALTMAIER', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'ALTMAIER', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'ALTMAIER', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
'KORDA_234clay': [  
                    {'player': 'KORDA', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'KORDA', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'KORDA', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'KORDA', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
'ALTMAIER_234clay': [  
                    {'player': 'ALTMAIER', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'ALTMAIER', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'ALTMAIER', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'ALTMAIER', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
                      'SWIATEK_234clay': [  
                    {'player': 'SWIATEK', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'SWIATEK', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'ROME 2023'}, 
                      ],
                      'GAUFF_234clay': [  
                    {'player': 'GAUFF', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'GAUFF', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'GAUFF', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'ROME 2023'}, 
                      ],

                      'HADDAD_234clay': [
                                            {'player': 'HADDAD MAIA', 'year': '2024', 'tournaments': ['ROME'], 'name': 'ROME 2024'}, 
  
                    {'player': 'HADDAD MAIA', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'HADDAD MAIA', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'CLAY 2023'}, 
                      ],

'RYBAKINA_234clay': [  
                    {'player': 'RYBAKINA', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'RYBAKINA', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'ROME 2023'}, 
                      ],
                      'SHANG_2023_2024_56htr': [  
                    {'player': 'SHANG', 'year': '2024',  'name': '2024'}, 
                    {'player': 'SHANG', 'year': '2023', 'name': '2023'}, 
                    {'player': 'SHANG', 'year': '2022', 'name': '2022'}

                      ],
'SINNER_2023_2024_56ht': [  
                    {'player': 'SINNER', 'year': '2024',  'name': '2024'}, 
                    {'player': 'SINNER', 'year': '2023', 'name': '2023'}, 
                      ],
                      'NAVARRO_2023_2024_56ht': [  
                         {'player': 'NAVARRO', 'year': '2024', 'tournaments': ['ROME'], 'name': 'ROME 2024'}, 

 {'player': 'NAVARRO', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
  {'player': 'NAVARRO', 'year': '2024', 'tournaments': ['MIAMI'], 'name': 'MIAMI 2024'}, 
   {'player': 'NAVARRO', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'INDIAN WELLS 2024'}, 

                    {'player': 'NAVARRO', 'year': '2024',  'name': '2024'}, 
                    {'player': 'NAVARRO', 'year': '2023', 'name': '2023'}
                      ],

'ANDREEVA_234clay': [  
                      {'player': 'ANDREEVA', 'year': '2024', 'tournaments': ['ROME'], 'name': 'ROME 2024'}, 

                    {'player': 'ANDREEVA', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'ANDREEVA', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                      ],

'PAVLYU_234clay': [  
                      {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['ROME'], 'name': 'ROME 2024'}, 

                    {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'PAVLYUCHENKOVA', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'PAVLYUCHENKOVA', 'year': '2023', 'tournaments': ['ROME'], 'name': 'ROME 2023'}, 
                      ],
                      'PAVLYUCHENKOVA_234clay': [  
                      {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['ROME'], 'name': 'ROME 2024'}, 

                    {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'PAVLYUCHENKOVA', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'PAVLYUCHENKOVA', 'year': '2023', 'tournaments': ['ROME'], 'name': 'ROME 2023'}, 
                      ],

      


    
    'DAVIDOVICH_234clay': [  
                    {'player': 'DAVIDOVICH FOKINA', 'year': '2024', 'tournaments': ['MADRID'], 'name': 'MADRID 2024'}, 
                    {'player': 'DAVIDOVICH FOKINA', 'year': '2023', 'tournaments': ['MADRID'], 'name': 'MADRID 2023'}, 
                    {'player': 'DAVIDOVICH FOKINA', 'year': '2024', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2024'}, 
                    {'player': 'DAVIDOVICH FOKINA', 'year': '2023', 'tournaments': ['ROME', 'MONTE', 'RG_'], 'name': 'OTHER CLAY 2023'}, 
                      ],
                      
    'ANDREEVA_clay8g65': [{'player': 'ANDREEVA', 'year': '2024', 'tournaments': ['Madrid'], 'name': 'MADRID 2024'},
                            {'player': 'ANDREEVA', 'year': '2023', 'tournaments': ['Madrid'], 'name': 'MADRID 2023'}],
    'OSAKA_clay8g65': [{'player': 'OSAKA', 'year': '2024', 'tournaments': ['Madrid'], 'name': 'Madrid 2024'},
                            {'player': 'OSAKA', 'year': '2022', 'tournaments': ['Madrid'], 'name': 'Madrid 2022'},
                            {'player': 'OSAKA', 'year': '2021', 'tournaments': ['Madrid'], 'name': 'Madrid 2021'},
                            {'player': 'OSAKA', 'year': '2024', 'tournaments': ['AO', 'Brisbane', 'Diego', 'Doha', 'Indian', 'Miami'], 'name': 'hard 2024'},
                             {'player': 'OSAKA', 'name': 'HARD 2020-2021', 'matches': ['AO_2020_R1_Osaka_Bouzkova', 'AO_2020_R2_Osaka_Zheng',
       'AO_2020_R3_Osaka_Gauff', 'AO_2021_1st_Pavlyuchenkova_Osaka',
       'AO_2021_2nd_Garcia_Osaka', 'AO_2021_3rd_Jabeur_Osaka',
       'AO_2021_4th_Muguruza_Osaka', 'AO_2021_F_Brady_Osaka',
       'AO_2021_QF_Hsieh_Osaka', 'AO_2021_SF_Osaka_S.Williams',
       'Brisbane_2020_QF_Bertens_Osaka', 'Brisbane_2020_R1_Sakkari_Osaka',
       'Brisbane_2020_R2_Kenin_Osaka',
       'Brisbane_2020_SF_Osaka_K.Pliskova',
       'Cincinnati_2020_QF_Osaka_Kontaveit',
       'Cincinnati_2020_R2_OSAKA_MUCHOVA',
       'Cincinnati_2020_R3_OSAKA_YASTREMSKA',
       'Cincinnati_2020_SF_Osaka_Mertens',
       'Cincinnati_2021_2nd_Gauff_Osaka',
       'Cincinnati_2021_3rd_Teichmann_Osaka',
       'Melbourne_2021_R2_CORNET_OSAKA',
       'Melbourne_2021_R3_BOULTER_OSAKA', 'US_Open_2020_F_OSAKA_AZARENKA',
       'US_Open_2020_QF_OSAKA_ROGERS', 'US_Open_2020_R1_OSAKA_DOI',
       'US_Open_2020_R2_OSAKA_GIORGI', 'US_Open_2020_R3_OSAKA_KOSTYUK',
       'US_Open_2020_R4_OSAKA_KONTAVEIT', 'US_Open_2020_SF_BRADY_OSAKA']}],
    'TSITSIPAS_clay8g65': [{'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['Madrid'], 'name': 'Madrid 2024'},
                            {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['Monte'], 'name': 'MC 2024'}, 
                            {'player': 'TSITSIPAS', 'year': '2023', 'tournaments': ['Monte'], 'name': 'MC 2023'}, 
                             {'player': 'TSITSIPAS', 'name': 'CLAY 2022-2023', 'matches': ['Monte-Carlo_2023_R32_Bonzi_Tsitsipas',
 'Rome_2022_SF_Tsitsipas_Zverev',
 'RG_2023_R16_Ofner_Tsitsipas',
 'Monte_Carlo_2022_QF_Schwartzman_Tsitsipas',
 'Madrid_2023_R16_Zapata-Miralles_Tsitsipas',
 'RG_2022_3rd_Ymer_Tsitsipas',
 'Rome_2023_R64_Tsitsipas_Borges',
 'Monte-Carlo_2023_QF_Fritz_Tsitsipas',
 'RG_2023_QF_Alcaraz_Tsitsipas',
 'Madrid_2022_2nd_Pouille_Tsitsipas',
 'Rome_2023_R16_Tsitsipas_Musetti',
 'Madrid_2023_2nd_Thiem_Tsitsipas',
 'RG_2023_Q_Vesely_Tsitsipas',
 'Madrid_2022_SF_Tsitsipas_Zverev',
 'Monte-Carlo_2023_R16_Jarry_Tsitsipas',
 'Rome_2022_2nd_Dimitrov_Tsitsipas',
 'Madrid_2023_R32_Baez_Tsitsipas',
 'RG_2022_2nd_Kolar_Tsitsipas',
 'Rome_2023_R32_Tsitsipas_Sonego',
 'RG_2023_R32_Schwartzman_Tsitsipas',
 'Madrid_2023_QF_Struff_Tsitsipas',
 'RG_2022_1st_Musetti_Tsitsipas',
 'Rome_2022_F_Djokovic_Tsitsipas',
 'Monte_Carlo_2022_2nd_Fognini_Tsitsipas',
 'Rome_2023_SF_Medvedev_Tsitsipas',
 'Monte_Carlo_2022_SF_Tsitsipas_Zverev',
 'Madrid_2022_3rd_Dimitrov_Tsitsipas',
 'Rome_2022_3rd_Khachanov_Tsitsipas',
 'Madrid_2022_QF_Rublev_Tsitsipas',
 'RG_2022_4th_Rune_Tsitsipas',
 'Rome_2023_QF_Tsitsipas_Coric',
 'Monte_Carlo_2022_3rd_Djere_Tsitsipas',
 'Rome_2022_QF_Sinner_Tsitsipas',
 'Monte_Carlo_2022_F_Davidovich-Fokina_Tsitsipas',
 'RG_2023_R64_Carballes-Baena_Tsitsipas']}],
    'DAVIDOVICH_clay8g65': [{'player': 'DAVIDOVICH FOKINA', 'year': '2024', 'tournaments': ['Madrid', 'Monte', 'Rome'], 'name': 'MC 2024'}, {'player': 'DAVIDOVICH FOKINA', 'year': '2023', 'tournaments': ['Madrid', 'Monte', 'Rome'], 'name': 'CLAY 2023'}, {'player': 'RUUD', 'name': 'CLAY 2022-2023', 'matches': ['Rome_2023_R64_Ruud_Rinderknech',
 'Monte-Carlo_2023_R16_Struff_Ruud',
 'Rome_2023_SF_Rune_Ruud',
 'Monte-Carlo_2023_R32_van-de-Zandschulp_Ruud',
 'Rome_2022_SF_Djokovic_Ruud',
 'Rome_2022_R32_van_de_Zandschulp_Ruud',
 'Rome_2023_R16_Ruud_Djere',
 'Rome_2023_QF_Ruud_Cerundolo',
 'Monte_Carlo_2022_R16_Ruud_Dimitrov',
 'Monte_Carlo_2024_F_Ruud_Tsitsipas',
 'Madrid_2022_R32_Lajovic_Ruud',
 'Monte_Carlo_2022_R32_Ruud_Rune',
 'Rome_2022_QF_Shapovalov_Ruud',
 'Rome_2022_R16_Brooksby_Ruud',
 'Rome_2023_R32_Ruud_Bublik',
 'Madrid_2023_R64_Ruud_Arnaldi']}],
    'SINNER_comparison': [
    {'player': 'SINNER', 'name': 'BEFORE RG 2023', 'matches': bad_sinner},
    {'player': 'SINNER', 'name': 'AFTER RG 2023', 'matches': good_sinner}
    ],
    'TSITSIPAS_grass': [
        {'player': 'TSITSIPAS', 'name': 'GRASS 2023', 'matches': ['Wimbledon_2023_R64_Murray_Tsitsipas',
 'Wimbledon_2023_1st_Thiem_Tsitsipas',
 'Halle_2023_R16_Jarry_Tsitsipas',
 'Halle_2023_R32_Barrere_Tsitsipas',
 'Wimbledon_2023_R16_Eubanks_Tsitsipas',
 'Wimbledon_2023_R32_Djere_Tsitsipas',
 'Stuttgart_2023_R16_Tsitsipas_Gasquet']},
    {'player': 'TSITSIPAS', 'name': 'GRASS 2022', 'matches': ['Stuttgart_2022_2nd_Tsitsipas_Stricker',
 'Malorca_2022_SF_Bonzi_Tsitsipas',
 'Malorca_2022_QF_Giron_Tsitsipas',
 'Halle_2022_2nd_Kyrgios_Tsitsipas',
 'Wimbledon_2022_3rd_Kyrgios_Tsitsipas',
 'Wimbledon_2022_1st_Ritschard_Tsitsipas',
 'Wimbledon_2022_2nd_Thompson_Tsitsipas',
 'Malorca_2022_2nd_Ivashka_Tsitsipas',
 'Stuttgart_2022_QF_Tsitsipas_Murray']}
    
    ],

    'SAKKARI_8g65': [
        {'player': 'SAKKARI', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'IW 2024'},
                {'player': 'SWIATEK', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'IW 2024'}
                            
    ],
    'ALTMAIER_8g6543': [
        {'player': 'ALTMAIER', 'year': '2024'},
        {'player': 'ALTMAIER', 'year': '2023'},
        {'player': 'ALTMAIER', 'year': '2022'}],
  
    'PUTINTSEVA_8g64': [  
                    {'player': 'PUTINTSEVA', 'year': '2024', 'tournaments': ['MIAMI'], 'name': 'MIAMI 2024'}, 
                    {'player': 'PUTINTSEVA', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'IW 2024'}, 
                      {'player': 'PUTINTSEVA', 'year': '2024', 'tournaments': ['HOBART', 'AO_'], 'name': 'AUSTRALIA 2024'}     
                      ],
    'GAUFF_8g64': [  
                    {'player': 'GAUFF', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'IW 2024'}, 
                    {'player': 'GAUFF', 'year': '2024', 'tournaments': ['AO_'], 'name': 'AO 2024'}, 
                      {'player': 'GAUFF', 'year': '2023', 'tournaments': ['Cincinnati', 'US_', 'Washington'], 'name': 'SUMMER 2023'},
                      {'player': 'GAUFF', 'year': '2023', 'tournaments': ['AO_', 'Auckland', 'Indian'], 'name': 'REST OF 2023'},
                      {'player': 'GAUFF', 'year': '2022'},
                      ],
   
    'SWIATEK_8g65': [
                            {'player': 'SWIATEK', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'IW 2024'},
                            {'player': 'SWIATEK', 'year': '2024', 'tournaments': ['DOHA'], 'name': 'DOHA 2024'},
                            {'player': 'SWIATEK', 'year': '2024', 'tournaments': ['DUBAI'], 'name': 'DUBAI 2024'},
                            {'player': 'SWIATEK', 'year': '2024', 'tournaments': ['AO'], 'name': 'AO 2024'},
                            {'player': 'SWIATEK', 'year': '2023', 'tournaments': ['INDIAN'], 'name': 'IW 2023'},
                            {'player': 'SWIATEK', 'year': '2023', 'name': 'ALL 2023'}
    ],
    'TSITSIPAS_8g654': [
        {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['INDIAN_'], 'name': 'VS LEHECKA IW 2024', 'matches': ['Indian_Wells_2024_R16_Lehecka_Tsitsipas']}, 
        {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['INDIAN_'], 'name': 'IW 2024'}, 
        {'player': 'TSITSIPAS', 'year': 'ALL 2024'}, 
        {'player': 'TSITSIPAS', 'year': 'ALL 2023'}],
         'TSITSIPAS_8g6543': [
        {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['INDIAN_'], 'name': 'VS LEHECKA IW 2024', 'matches': ['Indian_Wells_2024_R16_Lehecka_Tsitsipas']}, 
        {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['INDIAN_'], 'name': 'IW 2024 OTHER MATCHES', 'matches': ['Indian_Wells_2024_R32_Tiafoe_Tsitsipas', 'Indian_Wells_2024_R64_Pouille_Tsitsipas']}, 
        {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['AO_', 'UNITED', 'CABOS', 'ACAPULCO'], 'name': '2024 BEFORE IW'}, 
        {'player': 'TSITSIPAS', 'year': '2023'}, 
        {'player': 'TSITSIPAS', 'year': '2022'},
        {'player': 'TSITSIPAS', 'year': '2021'}, 
        {'player': 'TSITSIPAS', 'year': '2020'}
        ]    
    ,
    'DAVIDOVICH_8g65': [{'player': 'DAVIDOVICH FOKINA', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'IW 2024'}, {'player': 'DAVIDOVICH FOKINA', 'year': '2024', 'tournaments': ['DOHA'], 'name': 'DOHA 2024'}, {'player': 'DAVIDOVICH FOKINA', 'year': '2024', 'tournaments': ['DUBAI'], 'name': 'DUBAI 2024'}, {'player': 'DAVIDOVICH FOKINA', 'year': '2024', 'tournaments': ['ROTTERDAM'], 'name': 'ROTTERDAM 2024'}, {'player': 'DAVIDOVICH FOKINA', 'year': '2024', 'name': '2024 ALL'}, {'player': 'DAVIDOVICH FOKINA', 'year': '2023'}],
    'PAVLYUCHENKOVA_8g65': [
                            {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'VS KOSTYUK IW 2024', 'matches': ['Indian_Wells_2024_R16_Pavlyuchenkova_Kostyuk']},
                            {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['DIEGO'], 'name': 'VS KOSTYUK SAN DIEGO 2024', 'matches': ['San_Diego_2024_QF_Pavlyuchenkova_Kostyuk']},
                            
                            {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'IW 2024'}, 
                            {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['DIEGO'], 'name': 'SAN DIEGO 2024'}, 
                            {'player': 'PAVLYUCHENKOVA', 'year': '2024', 'tournaments': ['ADELAIDE'], 'name': 'ADELAIDE 2024'}],
        'GAUFF_8g65r65': [{'player': 'GAUFF', 'year': '2024', 'tournaments': ['AO_'], 'name': 'VS SABALENKA AO 2024', 'matches': ['AO_2024_SF_Gauff_Sabalenka']}, 
                    {'player': 'GAUFF', 'year': '2023', 'tournaments': ['US'], 'name': 'VS SABALENKA US 2023', 'matches': ['US_Open_2023_F_Gauff_Sabalenka']}, 
                      {'player': 'GAUFF', 'year': '2023', 'tournaments': ['Cincinnati', 'US_', 'Washington'], 'name': 'SUMMER 2023'},
                      {'player': 'SWIATEK', 'year': '2024'},
                      {'player': 'GAUFF', 'year': '2024', 'multi': ['SABALENKA', 'RYBAKINA']}
                      ],
                      'GAUFF_8g654': [
  {'player': 'GAUFF', 'year': '2024', 'tournaments': ['INDIAN'], 'name': 'IW 2024'}, 
  {'player': 'GAUFF', 'year': '2024', 'tournaments': ['AO_'], 'name': 'AO 2024'}, 
  {'player': 'GAUFF', 'year': '2023'} 
                      ],
    'SWIATEK_Dubai': [{'player': 'SWIATEK', 'year': '2024', 'tournaments': ['Dubai'], 'name': 'VS Kalinskaya', 'matches': ['Dubai_2024_SF_Swiatek_Kalinskaya']}, 
                    {'player': 'SWIATEK', 'year': '2024', 'tournaments': ['Dubai'], 'name': 'DUBAI WON MATCHES', 'matches': ['Dubai_2024_QF_Swiatek_Zheng', 'Dubai_2024_R16_Swiatek_Svitolina', 'Dubai_2024_R32_Swiatek_Stephens']}, 
                    {'player': 'SWIATEK', 'year': '2024', 'tournaments': ['Doha'], 'name': 'DOHAv WON MATCHES', 'matches': ['Doha_2024_F_Swiatek_Rybakina', 'Doha_2024_R32_Swiatek_Cirstea', 'Doha_2024_QF_Swiatek_Azarenka', 'Doha_2024_R16_Swiatek_Alexandrova']}
                      ],
     'OPPONENTS_Dubai': [{'player': 'KALINSKAYA', 'year': '2024', 'tournaments': ['Dubai'], 'name': ' VS SWIATEK DUBAI', 'matches': ['Dubai_2024_SF_Swiatek_Kalinskaya']}, 
                         {'player': 'SVITOLINA', 'year': '2024', 'tournaments': ['Dubai'], 'name': ' VS SWIATEK DUBAI', 'matches': ['Dubai_2024_R16_Swiatek_Svitolina']}, 
                         {'player': 'STEPHENS', 'year': '2024', 'tournaments': ['Dubai'], 'name': ' VS SWIATEK DUBAI', 'matches': ['Dubai_2024_R32_Swiatek_Stephens']}, 
                         {'player': 'ZHENG', 'year': '2024', 'tournaments': ['Dubai'], 'name': ' VS SWIATEK DUBAI', 'matches': ['Dubai_2024_QF_Swiatek_Zheng']}, 
                      ],
                      'TSITSIPAS_clay_comparison': [
    {'player': 'TSITSIPAS', 'matches': ['RG_2024_QF_Tsitsipas_Alcaraz', 'RG_2023_QF_Alcaraz_Tsitsipas'], 'name': 'V ALCARAZ RG 2023-2024'},
    {'player': 'TSITSIPAS', 'matches': ['RG_2024_QF_Tsitsipas_Alcaraz'], 'name': 'V ALCARAZ RG 2024'},
    {'player': 'TSITSIPAS', 'matches': ['RG_2022_4th_Rune_Tsitsipas'], 'name': 'V RUNE RG 2022'},
    {'player': 'TSITSIPAS', 'matches': ['Madrid_2022_3rd_Dimitrov_Tsitsipas', 'Rome_2022_2nd_Dimitrov_Tsitsipas'], 'name': 'V DIMITROV CLAY'},
    {'player': 'TSITSIPAS', 'matches': ['Madrid_2021_3rd_Ruud_Tsitsipas', 'Monte_Carlo_2024_F_Ruud_Tsitsipas'], 'name': 'V RUUD CLAY'},
],
    'NAKASHIMA_8g65rnew': [
        {'player': 'NAKASHIMA', 'year': '2024',  
        'tournaments': ['MIAMI'], 'name': 'MIAMI 2024'}, 
        {'player': 'NAKASHIMA', 'year': '2024',  
        'tournaments': ['INDIAN'], 'name': 'IW 2024'}, 
        {'player': 'NAKASHIMA', 'year': '2024',  'tournaments': ['AO_'], 'name': 'AO 2024'},
        {'player': 'NAKASHIMA', 'year': '2023'},
        {'player': 'NAKASHIMA', 'year': '2022'},
        {'player': 'NAKASHIMA', 'year': '2021'},
        {'player': 'NAKASHIMA', 'year': '2020'},
        ],
    'TSITSIPAS_8g65': [{'player': 'TSITSIPAS', 'year': '2024'}, {'player': 'TSITSIPAS', 'year': '2023'}],
    'ZHENG_8g65r': [{'player': 'ZHENG', 'year': '2024', 'tournaments': ['AO_'], 'name': 'AO 2024'}, {'player': 'ZHENG', 'year': '2024', 'tournaments': ['United'], 'name': 'UC 2024'}, {'player': 'ZHENG', 'year': '2023'}, {'player': 'SABALENKA', 'year': '2024'}, {'player': 'RYBAKINA', 'year': '2024'}],
    'PRIZMIC_8g65r': [{'player': 'PRIZMIC', 'year': '2024'}, {'player': 'DJOKOVIC', 'year': '2023', 'name': ''}, {'player': 'SINNER', 'year': '2023', 'tournaments': ['Vienna', 'Paris', 'Shanghai', 'Turin'], 'name': 'LATE 2023'}, {'player': 'RUNE', 'year': '2023', 'name': ''}],
    'NAKASHIMA_8g65r': [{'player': 'NAKASHIMA', 'year': '2024'}, {'player': 'NAKASHIMA', 'year': '2023'}],
        'DIMITROV_8g65r': [{'player': 'DIMITROV', 'year': '2024'}, {'player': 'DIMITROV', 'year': '2023'}],
        'DIMITROV_8g65r2': [{'player': 'DIMITROV', 'opponent': 'BORGES',  'year': '2024', 'tournaments': ['AO_'], 'name': 'AO 2024 BORGES'}, {'player': 'DIMITROV', 'year': '2024', 'tournaments': ['Brisbane'], 'name': 'Brisbane 2024'}, {'player': 'DIMITROV', 'year': '2023', 'tournaments': ['Beijing', 'United', 'Paris', 'Indian', 'Miami'], 'name': 'hard 2023'}],
        'TIAFOE_8g65r': [{'player': 'TIAFOE', 'year': '2024'}, {'player': 'TIAFOE', 'year': '2023'}],
        'MULLER_8g65r': [{'player': 'MULLER', 'year': '2024'}, {'player': 'MULLER', 'year': '2023'}],
        'GRENIER_8g65r': [{'player': 'GRENIER', 'year': '2024'}, {'player': 'GRENIER', 'year': '2023'}],
        'HADDAD_8g65r': [{'player': 'HADDAD MAIA', 'year': '2024'}, {'player': 'HADDAD MAIA', 'year': '2023'}],
        'NAKASHIMA_8g65r': [{'player': 'NAKASHIMA', 'year': '2024'}, {'player': 'NAKASHIMA', 'year': '2023'}],
        'BLOCKX_cfd24': [{'player': 'BLOCKX', 'year': '2024'}, {'player': 'BLOCKX', 'year': '2023'}],
        'FOKINA_cfd245': [{'player': 'DAVIDOVICH FOKINA', 'year': '2023'}, {'player': 'DAVIDOVICH FOKINA', 'year': '2022'}],
        'PAUL_cfd245': [{'player': 'PAUL', 'year': '2024'}, {'player': 'PAUL', 'year': '2023'}],
        'KECMANOVIC_cfd245': [{'player': 'KECMANOVIC', 'year': '2024'}, {'player': 'KECMANOVIC', 'year': '2023'}],
        'RYBAKINA_cfd245': [{'player': 'RYBAKINA', 'year': '2024'}, {'player': 'RYBAKINA', 'year': '2023'}],
        'SWIATEK_cfd245': [{'player': 'SWIATEK', 'year': '2024'}, {'player': 'SWIATEK', 'year': '2023'}, {'player': 'SWIATEK', 'year': '2022'},
        {'player': 'SWIATEK', 'year': '2022', 'multi': ['SABALENKA', 'GAUFF', 'RYBAKINA']}],
        'TSITSIPAS_8g65r': [{'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['AO_'], 'name': 'AO 2024'}, {'player': 'TSITSIPAS', 'year': '2023', 'tournaments': ['AO_'], 'name': 'AO 2023'} , {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['United_Cup']}, {'player': 'TSITSIPAS', 'year': '2023', 'tournaments': ['Vienna', 'Turin', 'Paris', 'Shanghai'], 'name': '2023 late'}],
        'TSITSIPAS_clay_gstaad': [
    {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['GSTAAD'], 'name': 'GSTAAD 2024'},  
    {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['RG_'], 'name': 'RG 2024'},  
    {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['Rome'], 'name': 'ROME 2024'},  
    {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['Madrid'], 'name': 'MADRID 2024'},  
    {'player': 'TSITSIPAS', 'year': '2024', 'tournaments': ['Monte-', 'Monte_'], 'name': 'MONTE CARLO 2024'},  
    {'player': 'TSITSIPAS', 'year': '2023', 'tournaments': ['RG_', 'Madrid', 'Rome', 'Monte'], 'name': 'CLAY 2023 ALL'},  
    {'player': 'TSITSIPAS', 'year': '2022', 'tournaments': ['RG_', 'Madrid', 'Rome', 'Monte'], 'name': 'CLAY 2022 ALL'},  
]
        }
#pretty_dict, data1, data2, data3, data_order = main2()

dark = ui.dark_mode()
dark.enable()

@ui.page('/report/{report}', dark=True, response_timeout=15)
async def main_page(report: str):
    #data
    ui.markdown(f'# GSA Shot Quality Evolution Report - {report.split("_")[0]}').classes('mx-auto')
    pretty_dict, data_list, data_order = await run.cpu_bound(main2, data[report])
    #with ui.row():
    #    ui.label('sCSS').style('color: #888; font-weight: bold')
    #    ui.label('Tailwind').classes('font-serif')
    #    ui.label('Quasar').classes('q-ml-xl')
    #ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')
    #img = Image.opens('blockx.jpeg')
    #img = img.resize((10,20), Image.LANCZOS)
    #ui.image(img).classes('w-64')

    with ui.tabs().classes('w-full') as tabs:
        ui.tab('serve', label='Serve')
        ui.tab('return', label='Return')
        ui.tab('return_speed', label='Return Speed')
        ui.tab('consistency', label='Consistency')
        ui.tab('initiative', label='Initiative')
        ui.tab('pressure', label='pressure')
        ui.tab('groundstroke_table', label='Rally FH/BH')
        ui.tab('winners_table', label='WINNERS')
        #ui.tab('groundstroke_table', label='Groundstroke Table')
        ui.tab('approach_stats', label='Approach Stats')
        ui.tab('rally_play_type', label='Rally play type')
    #with ui.tabs() as tabs2:
        ui.tab('offensive', label='Offensive')
        ui.tab('defensive', label='Defensive')
        ui.tab('dropshots', label='Drop shots')
        
    #ui.add_head_html('<style>.my-table tbody td { font-size: 1.25em }</style>')
    #ui.add_head_html('<style>.my-table-header thead th { font-size: 1.25em }</style>')

    with ui.tab_panels(tabs, value='serve').classes('mx-auto'):
        for key in data_order:
            with ui.tab_panel(key).classes('w-full'):
                
                for table in data_order[key]:
                  rows = []
                  for k in table['columns']:
                  #for k in data_order[key]:
                      row_dict = {
                      'filter': pretty_dict.get(k, k.replace("_", " ")).upper().replace('FIRST', '1ST').replace('SECOND', '2ND')#.replace('RETURN FH SPEED', 'FH SPEED').replace('RETURN BH SPEED', 'FH SPEED').replace('DEUCE FH', 'FH DEUCE').replace('DEUCE BH', 'BH DEUCE').replace('AD FH', 'FH AD').replace('AD BH', 'BH AD')
                      
                      }
                      for i, d in enumerate(data_list):
                          row_dict['report' + str(i)] = d[0][k]
                      rows.append(row_dict)
                  columns=[{'name': 'filter', 'label': '', 'field': 'filter', 'align': 'center'}]
                  for i, d in enumerate(data_list):
                      columns.append({'name': 'report1', 'label': f'{d[1]} {d[2]}', 'field': 'report' + str(i), 'align': 'center'})
                  #with ui.row().style('font-size: 5.25em;'):
                  if table.get('title'):
                      ui.markdown(f'## {table.get("title")}').classes('mx-auto')
                  ui.table(columns=columns, rows=rows, row_key='name').classes('w-full').classes('my-table').classes('my-table-header')#.add_slot('header', '<th style="font-size: 1.25em">{{ props.row.name }}</th>')#.style('overflow-x: visible')
            
        
    

ui.run(host='0.0.0.0', port=8509)