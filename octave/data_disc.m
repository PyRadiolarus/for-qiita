clear all

data = load("data_disc.txt"); #データ読み込み

Y = data(:,1); #年
M = data(:,2); #月
D = data(:,3); #日

temp = data(:,4); #気温
Days = [datenum(Y,M,D)]; #各データの年月日をシリアル日付値に変換してベクトルへ格納
l = length(Days) #ベクトルの長さを変数に代入
tt = []; #空ベクトル定義

#x軸プロット用forループ
for i = 1:l
    sd = Days(i);
    day = sd - 737607; #シリアル日付値で2019年7月1日は737607
    tt(i) = day;
end

#プロット作成
plot(tt, temp)

#凡例作成
h=legend({"Temprature"},"Location","bestoutside") #凡例位置はプロットにかぶらない最適な位置で、グラフの外側を指定
set(h,"FontName","Times New Roman","FontSize",11)
set(gca,"FontName","Times New Roman","FontSize",11)
xlabel("Number of days elapsed since July 1, 2019(days)")
ylabel("Temprature(degree Celsius)")

#プロットをpngファイルに出力
print("Yamagata2019-21_disc","-dpng")