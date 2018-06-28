import android, time

droid = android.Android()
droid.startLocating()
time.sleep(5)
loc = droid.readLocation().result
if loc == {}:
    loc = droid.getLastKnownLocation().result
if loc != {}:
    try:
        n = loc['gps']
    except KeyError:
        n = loc['network']
    la = n['latitude']
    lo = n['longitude']
    address = droid.geocode(la, lo).result
droid.stopLocating()