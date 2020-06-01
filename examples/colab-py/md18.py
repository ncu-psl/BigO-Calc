def module18():
    import urllib.request
    x = urllib.request.urlopen('https://kai.one/colab_quiz_18.txt') #把-----替換成正確的網址
    print(x.read().decode('utf-8'))