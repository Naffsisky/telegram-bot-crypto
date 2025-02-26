import os
import requests

CMC_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
CMC_BASE_URL = "https://pro-api.coinmarketcap.com/v1"

def get_crypto_price(symbol: str):
    """Mengambil harga crypto dalam USD dan IDR dengan dua request."""
    try:
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY, "Accept": "application/json"}

        # Request harga dalam USD
        url_usd = f"{CMC_BASE_URL}/cryptocurrency/quotes/latest"
        params_usd = {"symbol": symbol, "convert": "USD"}
        response_usd = requests.get(url_usd, headers=headers, params=params_usd, timeout=10)
        data_usd = response_usd.json()

        # Request harga dalam IDR
        url_idr = f"{CMC_BASE_URL}/cryptocurrency/quotes/latest"
        params_idr = {"symbol": symbol, "convert": "IDR"}
        response_idr = requests.get(url_idr, headers=headers, params=params_idr, timeout=10)
        data_idr = response_idr.json()

        # Debug response dari API
        # print(f"🔍 DEBUG USD: {data_usd}")
        # print(f"🔍 DEBUG IDR: {data_idr}")

        # Cek apakah request berhasil
        if (response_usd.status_code == 200 and data_usd["status"]["error_code"] == 0) and \
           (response_idr.status_code == 200 and data_idr["status"]["error_code"] == 0):
            
            usd_price = data_usd["data"][symbol]["quote"]["USD"]["price"]
            idr_price = data_idr["data"][symbol]["quote"]["IDR"]["price"]
            return usd_price, idr_price
        else:
            return None, None
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None, None
