# Журнал работы над проектом

## IP-camera
Разобраться с IP-камерами, приобрести походящую, разобраться с ней.

Выбран VSTARCAM (https://www.vstarcam.com/1056.html) самая дешевая HD  
c поддержкой onvif-протокола, чтобы общаться с ней из любого софта.
![c43](C43Sy_17.jpg)

Потрачено много времени на подключение.

**Ccылки**   
Программа для работы и настройки   
https://sourceforge.net/projects/onvifdm/
Список адресов (у разных камер разный адрес!)
http://www.ispyconnect.com/cameras 


## Распознавание доски, крестиков и ноликов  
Попробуем так, возможно для игры хватит:
_Доска_ в аппроксимации - 20-угольник, внутри которого четырехугольник
```python   
def detect_board(contours, hierarchy):
    for i, c in enumerate(contours):
        if cv2.arcLength(c, True) < 50:
            continue
        epsilon = 0.02 * cv2.arcLength(c, True)
        poly = cv2.approxPolyDP(c, epsilon, True)
        if len(poly) == 20:
            if hierarchy[0][i][2] != -1:
                inside = contours[hierarchy[0][i][2]]
                epsilon = 0.02 * cv2.arcLength(inside, True)
                poly = cv2.approxPolyDP(inside, epsilon, True)
                if len(poly) == 4:
                    return i
    return None
```
_Крестик_ - отношение расстояния ближней от центра контура точки и ближней - мало  
_Нолик_ - в ином случае 
```python
def detect_sign(contour):
    '''NOUGHT or CROSS'''
    center, r = cv2.minEnclosingCircle(contour)
    mind = r * r
    for p in contour:
        d = dist2(p[0], center)
        if d < mind:
            mind = d
    # print(mind / (r * r))
    if mind / (r * r) < 0.1:
        return X
    else:
        return O
```
![](Image%20725.png)

![](Image%20726.png)

![](Image%20727.png)

Да... Посторонние предметы (можно отсечь выделением области игры), 
но, главное, четырехугольник внутри распознается как нолик...

Начало положено!
