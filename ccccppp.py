import folium
from geocoder import Nominatim

# الحصول على معلومات الموقع الجغرافي
geocoder = Nominatim(user_agent="my_app")
location = geocoder.geocode("رقم الهاتف")

# التحقق من صحة الموقع
if location is None:
    print("لا يمكن العثور على الموقع")
else:
    # استخراج إحداثيات خط الطول والعرض
    latitude = location.latitude
    longitude = location.longitude

# إنشاء خريطة HTML
map = folium.Map(location=[latitude, longitude], zoom_start=10)

# وضع علامة على الموقع على الخريطة
folium.Marker([latitude, longitude], popup="رقم الهاتف").add_to(map)

# عرض الخريطة
map.save("map.html")
