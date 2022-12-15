# GPXファイルから緯度経度標高を抽出してXYZファイルに書き出すプログラム
import csv
import gpxpy
from pyproj import Proj

def from_gpx_to_xyz():
    file_name = input("GPXファイルの名称を入力（拡張子除く）：")
    utm_zone = input("UTMゾーンの値を入力（半角数字）：")
    utm_conv = Proj(proj="utm", zone=utm_zone, ellps="GRS80")
    xyz_list = []

    with (open(f"{file_name}.gpx",mode="r") as gpx_file, open(f"{file_name}_from_gpx.xyz",mode="w") as xyz_file):
        gpx = gpxpy.parse(gpx_file)
        for trk in gpx.tracks:
            for seg in trk.segments:
                for pt in seg.points:
                    # 経度は東西方向なのでX方向、緯度は南北方向なのでY方向のデータになる
                    utmx, utmy = utm_conv(pt.longitude, pt.latitude)
                    # 南半球ならオフセットする
                    if pt.latitude < 0:
                        utmy = utmy + 10000000
                    else:
                        pass
                    xyz_list.append([utmx, utmy, pt.elevation])
        # 区切り文字に半角スペースを指定
        writer = csv.writer(xyz_file, delimiter=" ")
        writer.writerows(xyz_list)

if __name__ == "__main__":
    from_gpx_to_xyz()