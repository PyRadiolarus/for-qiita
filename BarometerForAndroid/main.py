import csv
import datetime
import json
import requests
import subprocess

def get_altitude():
    # 位置情報から標高の取得
    location = subprocess.getoutput("termux-location")
    # デフォルトではGPSから位置情報を取得するが、タイムアウトすると出力が空になってしまう。
    if not location:
        # GPSから取得できなかった場合、ネットワークからの取得を試みる。
        location = subprocess.getoutput("termux-location -p network")
    else:
        pass
    location_dict = json.loads(location)
    altitude = "標高：" + str(round(location_dict["altitude"],2))
    return altitude

def get_pressure():
    # 気圧の取得
    pressure = subprocess.getoutput("termux-sensor -s \"Pressure Sensor\" -n 1")
    pressure_dict = json.loads(pressure)
    pressure_now = "気圧：" + str(round(pressure_dict["ICP10101 Pressure Sensor"]["values"][0],2))
    return pressure_now

def get_time():
    # 現在時刻の取得
    now = datetime.datetime.now()
    # 日本国内での使用を想定
    now_timezone = str(datetime.timezone(datetime.timedelta(hours=9)))
    now = now.strftime("%Y-%m-%d %H:%M ") + "(" + now_timezone + ")"
    return now

def time_diff_trans(diff):
    # 経過時間の差分を算出
    minute, second = divmod(diff, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    return day, hour, minute, second

def push_message(body):
    # プッシュ通知送信
	token = "ここにPushbulletのAPIトークンを入力"
	url = "https://api.pushbullet.com/v2/pushes"
	
	headers = {"content-type": "application/json", "Authorization": 'Bearer '+token}
	data_send = {"type": "note", "title": "現在地の標高・気圧", "body": body}

	message = requests.post(url, headers=headers, data=json.dumps(data_send))

altitude = get_altitude()
pressure = get_pressure()
time = get_time()
trim_time = datetime.datetime.strptime(time[:-12], "%Y-%m-%d %H:%M")

# 前回実行時のデータを取得
with open("diff.csv",mode="r") as old:
    pre_data_lst = [i for i in csv.reader(old)][0]
    pre_att = pre_data_lst[1]
    pre_prs = pre_data_lst[2]
    pre_time = pre_data_lst[0]

pre_time = datetime.datetime.strptime(pre_time, "%Y-%m-%d %H:%M:%S")

# 今回の実行結果をdiff.csvには"上書き"保存
with open("diff.csv", mode="w") as new:
    writer = csv.writer(new)
    new_data_lst = [trim_time,altitude[3:],pressure[3:]]
    writer.writerow(new_data_lst)

# history.csvには"追記"保存
with open("history.csv", mode="a") as out:
    writer = csv.writer(out)
    writer.writerow(new_data_lst)

# 標高の差分算出
att_diff = round(float(altitude[3:]) - float(pre_att),2)

# 差分の正負判定と単位記入、正なら"+"記号追加
if att_diff > 0:
    att_diff = "+" + str(att_diff) + "m"
else:
    att_diff = str(att_diff) + "m"

# 気圧の差分算出
prs_diff = round(float(pressure[3:]) - float(pre_prs),2)

# 差分の正負判定と単位記入、正なら"+"記号追加
if prs_diff > 0:
    prs_diff = "+" + str(prs_diff) + "hPa"
else:
    prs_diff = str(prs_diff) + "hPa"

# 時刻の差分算出
time_diff = trim_time - pre_time
time_diff = time_diff.total_seconds()
# 差分を秒単位に直してから経過日時取得
time_calc = time_diff_trans(time_diff)
time_elap = str(int(time_calc[0]))+ "日，" + str(int(time_calc[1])) + "時間" + str(int(time_calc[2])) + "分"

res = time + "\n" + altitude + "m (" + att_diff + ")\n" + pressure + "hPa (" + prs_diff + ")\n\n前回計測からの経過時間：" + time_elap
push_message(res)