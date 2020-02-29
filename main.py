
from load_data import DataLoader
from analytics import Analytics
if __name__ == '__main__':
    data = DataLoader()
    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw)