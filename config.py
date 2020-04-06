JH_CONFIRMED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
JH_RECOVERED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
JH_DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

JH_US_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
JH_US_DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

#API_CONFIRMED_CASES = "https://coviddata.github.io/covid-api/v1/regions/cases.csv"
#API_RECOVERED_CASES = "https://coviddata.github.io/covid-api/v1/regions/recoveries.csv"
#API_DEATHS = "https://coviddata.github.io/covid-api/v1/regions/deaths.csv"

#JH_CONFIRMED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
#JH_RECOVERED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
#JH_DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

# JH_CONFIRMED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
# JH_RECOVERED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
# JH_DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

# CONFIRMED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
# RECOVERED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
# DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

CONFIRMED_CASES = "https://covidbio-covid-data.s3.us-east-2.amazonaws.com/confirmed.csv"
RECOVERED_CASES = "https://covidbio-covid-data.s3.us-east-2.amazonaws.com/recovered.csv"
DEATHS = "https://covidbio-covid-data.s3.us-east-2.amazonaws.com/deaths.csv"

UPDATE_STRING = 'https://covidbio-covid-data.s3.us-east-2.amazonaws.com/updated_string.txt'
UPDATE_DATE_STAMP = 'https://covidbio-covid-data.s3.us-east-2.amazonaws.com/date_stamp.txt'

WORLDWIDE_REGIONS = {
    'Africa': ['Algeria', 'Egypt', 'Morocco', 'Senegal'],
    'Asia': ['South Korea', 'Iran', 'Japan', 'Singapore', 'Hong Kong', 'Kuwait', 'Bahrain', 'Thailand', 'Taiwan',
             'Malaysia', 'Iraq', 'United Arab Emirates', 'Vietnam', 'Lebanon', 'Macau', 'Israel', 'Oman', 'India',
             'Pakistan', 'Philippines', 'Qatar', 'Indonesia', 'Nepal', 'Cambodia', 'Sri Lanka', 'Afghanistan', 'Armenia',
             'Saudi Arabia', 'Mainland China', 'Russia', 'Georgia', 'Azerbaijan'],
    'Europe': ['Switzerland', 'UK', 'Norway', 'Austria', 'Netherlands', 'Sweden', 'Belgium', 'San Marino', 'Croatia',
               'Greece', 'Finland', 'Iceland', 'Denmark', 'Romania', 'Czech Republic', 'Portugal', 'North Macedonia',
               'Estonia', 'Belarus', 'Lithuania', 'Ireland', 'Luxembourg', 'Monaco', 'Andorra', 'Latvia', 'Italy',
               'France', 'Germany', 'Spain'],
    'North America': ['Canada', 'Mexico', 'Dominican Republic', 'US'],
    'Oceania': ['Australia', 'New Zealand'],
    'South America': ['Ecuador', 'Brazil']
}

COUNTRIES_MENU = ["US", "Iran", "Italy", "Germany", "France", "Spain", "Switzerland", "UK"]

STATE_MAP = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "D.C.": "District Of Columbia",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    'U.S.': "United States"
}

MANUAL_DAY_COUNTS = {
    'US': 119,
    'France': 140,
    'Germany': 131,
    'Spain': 83,
    'Iran': 94,
    'Switzerland': 115
}