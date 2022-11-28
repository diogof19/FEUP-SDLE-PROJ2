import ntplib
import os

offset = 0

def sync_time() -> None:
    global offset
    ntpclient = ntplib.NTPClient()
    for attempt in range(3):
        try:
            response = ntpclient.request('pool.ntp.org')
            offset = response.offset
            if os.getenv('DEBUG'):
                debug_ntp(response)
            return 
        except ntplib.NTPException:
            #print(f'NTP request failed, attempt number {attempt + 1}')
            pass

def debug_ntp(response : ntplib.NTPStats) -> None:
    print("NTP offset: ", response.offset)
    print("NTP delay: ", response.delay)
    print("NTP precision: ", response.precision)
    print("NTP stratum: ", response.stratum)
    print("NTP ref_id: ", response.ref_id)
    print("NTP ref_time: ", response.ref_time)
    print("NTP root_delay: ", response.root_delay)
    print("NTP root_dispersion: ", response.root_dispersion)
    print("NTP tx_time: ", response.tx_time)
    print("NTP dest_time: ", response.dest_time)
    print("NTP leap: ", response.leap)
    print("NTP version: ", response.version)
    print("NTP mode: ", response.mode)
    print("NTP poll: ", response.poll)
    print("NTP ref_time: ", response.ref_time)
    print("NTP ref_time: ", response.ref_time)
    print("NTP ref_time: ", response.ref_time)