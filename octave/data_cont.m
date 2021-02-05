clear all

data = load("data_cont.txt"); #データ読み込み

temp = data(:,4); #気温
days = size(temp)
tt = [1:(days)];


#プロット作成
plot(tt, temp)

#凡例作成
h=legend({"Temprature"},"Location","bestoutside") #凡例位置はプロットにかぶらない最適な位置で、グラフの外側を指定
set(h,"FontName","Times New Roman","FontSize",11)
set(gca,"FontName","Times New Roman","FontSize",11)
xlabel("Number of days elapsed since July 1, 2019(days)")
ylabel("Temprature(degree Celsius)")

#プロットをpngファイルに出力
print("Yamagata2019-21_cont","-dpng")
