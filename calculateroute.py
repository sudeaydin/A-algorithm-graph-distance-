import pandas as pd
import numpy as np

def calculateroute(listt,file):
    #verinin csv dosyasından okunması
    #dataframe e doğru aktarabilmek için start,to,distance sutünlarını ekledim
    df=pd.read_csv(file)
    startun=df["start"].unique()
    toun=df["to"].unique()
    sehir=[*startun,*toun]
    sehir=list(set(sehir))
    route_list = df.values.tolist()
    adj_list={}
    H={}

    #verileri graph veri yapısına çevirmek için adj list oluşturdum.
    #heuristic fonksiyon için de dictionary veri yapısı kullandım
    #adj list i çift taraflı oluşturdum.
    for i in sehir:
        adj_list[i]=[]
        H[i]=1  #heuristic fonksiyon gerçek sonuçtan daha az  ya da aynı olması gerektiği için 1 olarak yazılır
    for i in route_list:
        adj_list[i[0]].append([i[1],i[2]])
        adj_list[i[1]].append([i[0],i[2]])

    #incelenecek olan node ları belirlemek için open ve close list oluşturulur
    open_lst = []
    open_lst.append(listt[0])
    closed_lst = []

    #şehirler için toplam mesafeyi tutabilmek için dictionary yapısında oluşturulur.başlangıç nodundan itibaren
    dis = {}
    dis[listt[0]] = 0 #başlangıç nodunun uzaklığı 0 olarak belirlenir

    # şehirler için hangi node da olunduğunun bilgisinin tutulması
    adj = {}
    adj[listt[0]] = listt[0] #başlangıç nodunun üst nodu olmadığı için kendisine eşitlenir


    while len(open_lst) > 0:
        n = None
        for i in open_lst: #en düşük f(n) bulunması
            if n == None or dis[i] + H[i] < dis[n] + H[n]:
                n = i;

        if n == None:
            print('Yol geçersiz')
            return None

        if n == listt[1]: #sonuç noduna gelindiğinde
            path = []
            while adj[n] != n:
                path.append(n)
                n = adj[n]
            path.append(listt[0]) #başlangıç nodu eklenir
            path.reverse() #sona ekleme yaptığından ters çevrilir
            delimeter = "-".join(path)
            print(delimeter)
            return path

        for (m, weight) in adj_list[n]:

            if m not in open_lst and m not in closed_lst:
                open_lst.append(m)
                adj[m] = n
                dis[m] = dis[n] + weight #distance ve parent node güncellenir


            else:
                if dis[m] > dis[n] + weight:
                    dis[m] = dis[n] + weight
                    adj[m] = n #distance ve parent node güncellenir

                    if m in closed_lst:
                        closed_lst.remove(m) 
                        open_lst.append(m)

        open_lst.remove(n)
        closed_lst.append(n)
    return None
calculateroute(["Istanbul","Ankara"],"distances.csv")
