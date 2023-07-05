def check_ph(ph: float):
    if (ph < 6.5):
        return "Lakukan pengapuran dengan jenis dolomit"

    if (ph > 8.5):
        return "Lakukan pergantian air dan pastikan sumber air tidak basa (mengandung pH tinggi)"

    # pH normal: 6.5 - 8.5
    return None


def check_temp(temp: float):
    if (temp < 25):
        return "Nyalakan heater untuk meningkatkan temperatur air"

    if (temp > 32):
        return "Matikan heater/beri peneduh sementara dan tambah air dengan suhu sejuk"

    # Temperatur normal: 25 - 32 celcius
    return None


def get_recommendation(ph: float = 0, temp: float = 0):
    # TODO: Preprocess outlier data

    ph_recommendation = check_ph(ph)
    temp_recommendation = check_temp(temp)

    recommendation = {
        "ph": None,
        "temp": None
    }

    if (ph_recommendation):
        recommendation["ph"] = ph_recommendation

    if (temp_recommendation):
        recommendation["temp"] = temp_recommendation

    return recommendation
