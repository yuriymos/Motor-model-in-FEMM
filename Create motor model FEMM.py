# Motor model in FEMM
# Программа обеспечивает создание в FEMM 2D
# простой модели электрической машины
# с постоянным магнитом на роторе
  
import femm
import math

# подключение модуля FEMM 2D в программу Python
femm.openfemm();

# Создание в FEMM 2D задачи анализа магнитной цепи
femm.newdocument(0);

# Define the problem type.  Magnetostatic; Units of mm; Axisymmetric; 
# Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
# the depth dimension, and an angle constraint of 30 degrees
femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, 50, 30);
#####################################################
# параметры электрической машины
# токи в обмотке только в одной катушке по оси абсцисс
p = 2 # число зубцов
outer_stator = 60 # внешний радиус сердечника статора
inner_stator = 50 # внутренний радиус сердечника статора
radius_tooth = 30 # размер от оси вращения до полюсного наконечника статора
toothWidth = 30 # ширина зубца статора
air_gap = 2 # воздушный зазор
bandage = 2 # толщина бандажа ротора
# размер от внутренней окружности спинки статора до полюсного наконечника
inner_tooth = inner_stator - radius_tooth
#####################################################
# угол между срединами зубцов статора
angle = math.pi/p # в радианах
#####################################################
# нарисовать наружнюю окружность сердечника статора
femm.mi_drawarc(outer_stator,0,-outer_stator,0,180,1)
femm.mi_drawarc(-outer_stator,0,outer_stator,0,180,1)
#####################################################
# угол между сторонами каждого зубца
# по внутренней окружности спинки статора
angle_for_tooth = 2*math.asin(toothWidth/2/inner_stator)

# нарисовать дуги внутренней окружности сердечника статора
x_left_0 = math.cos(angle_for_tooth/2)*inner_stator
y_left_0 = math.sin(angle_for_tooth/2)*inner_stator

x_right_0 = math.cos(-angle_for_tooth/2)*inner_stator
y_right_0 = math.sin(-angle_for_tooth/2)*inner_stator

points_for_poles = [0]*2*p

# задаем точки на внутренней окружности спинки статора для зубцов
for i in range (0,2*p):
        x_left = inner_stator*math.cos(math.atan(y_left_0/x_left_0)+i*angle)
        y_left = inner_stator*math.sin(math.atan(y_left_0/x_left_0)+i*angle)
        femm.mi_addnode(x_left,y_left)
        
        x_right = inner_stator*math.cos(math.atan(y_right_0/x_right_0)+i*angle)
        y_right = inner_stator*math.sin(math.atan(y_right_0/x_right_0)+i*angle)       
        points_for_poles[i] = [x_left,y_left,x_right,y_right]
        femm.mi_addnode(x_right,y_right)


# для дуг спинки статора между зубцами
for i in range (0,2*p-1):
        femm.mi_drawarc(points_for_poles[i][0],points_for_poles[i][1],       
                        points_for_poles[i+1][2],points_for_poles[i+1][3],
                        (angle-angle_for_tooth)*180/math.pi,1)
# для последней дуги между зубцами
femm.mi_drawarc(points_for_poles[2*p-1][0],points_for_poles[2*p-1][1],
                points_for_poles[0][2],points_for_poles[0][3],
                (angle-angle_for_tooth)*180/math.pi,1)



# задаем первые точки для полюсного наконечника по оси абсцисс
x_left_end_0 = x_left_0 - inner_tooth
y_left_end_0 = y_left_0

x_right_end_0 = x_right_0 - inner_tooth
y_right_end_0 = y_right_0

points_for_poles_endings = [0]*2*p

# задаем точки для полюсных наконечников
for i in range (0,2*p):
        x_left = math.sqrt(x_left_end_0**2+y_left_end_0**2)*\
                 math.cos(math.atan(y_left_end_0/x_left_end_0)+i*angle)
        y_left = math.sqrt(x_left_end_0**2+y_left_end_0**2)*\
                 math.sin(math.atan(y_left_end_0/x_left_end_0)+i*angle)
        femm.mi_addnode(x_left,y_left)
        
        x_right = math.sqrt(x_left_end_0**2+y_left_end_0**2)*\
        math.cos(math.atan(y_right_end_0/x_right_end_0)+i*angle)
        y_right = math.sqrt(x_left_end_0**2+y_left_end_0**2)*\
        math.sin(math.atan(y_right_end_0/x_right_end_0)+i*angle)
        femm.mi_addnode(x_right,y_right)

        points_for_poles_endings[i] = [x_left,y_left,x_right,y_right]

# радиус окружности через наконечники зубцов статора        
pole_endings_radius = math.sqrt(x_left_end_0**2+y_left_end_0**2)

# окружность, проходящая через наконечники зубцов статора
femm.mi_drawarc(pole_endings_radius,0,-pole_endings_radius,0,180,1)
femm.mi_drawarc(-pole_endings_radius,0,pole_endings_radius,0,180,1)

# боковые линии зубцов статора
for i in range (0,2*p):
        # слева
        femm.mi_drawline(points_for_poles[i][0],points_for_poles[i][1],
                         points_for_poles_endings[i][0],points_for_poles_endings[i][1])
        # справа
        femm.mi_drawline(points_for_poles[i][2],points_for_poles[i][3],
                         points_for_poles_endings[i][2],points_for_poles_endings[i][3])

# линии для разделения катушек обмотки
for i in range (0,2*p):
        # точки на внутренней окружности спинки статора
        x_up = math.cos(i*angle+angle/2)*inner_stator
        y_up = math.sin(i*angle+angle/2)*inner_stator
        #femm.mi_addnode(x,y)
        # точки на окружности спинки статора
        x_down = math.cos(i*angle+angle/2)*pole_endings_radius
        y_down = math.sin(i*angle+angle/2)*pole_endings_radius
        #femm.mi_addnode(x,y)
        femm.mi_drawline(x_up,y_up,x_down,y_down)

# нарисовать наружнюю окружность ротора,
# которая меньше окружности полюсных наконечников
# на величину воздушного зазора
rotor_radius = pole_endings_radius-air_gap
femm.mi_drawarc(rotor_radius,0,-rotor_radius,0,180,1)
femm.mi_drawarc(-rotor_radius,0,rotor_radius,0,180,1)
# нарисовать окружность для магнита на роторе,
# которая меньше окружности ротора на величину бандажа
magnet_radius = rotor_radius - bandage
femm.mi_drawarc(magnet_radius,0,-magnet_radius,0,180,1)
femm.mi_drawarc(-magnet_radius,0,magnet_radius,0,180,1)

#####################################################
# необходимо добавить необходимые материалы и среды в проект
# добавить воздушную среду вокруг рассматриваемой ЭМ
femm.mi_addmaterial('Air', 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0);
femm.mi_addblocklabel(0,1.25*outer_stator)
femm.mi_selectlabel(0,1.25*outer_stator)
femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()

# Добавим ферромагнитный материал сердечника
# с заданной кривой намагничивания (зависимость B от H)
# Сначала, создаем материал с линейной зависимостью B от H 
# значения, используемые для определения магнитной проницаемости,
# являются всего лишь заполнителями.
femm.mi_addmaterial('Iron', 2100, 2100, 0, 0, 0, 0, 0, 1, 0, 0, 0);

# Затем задается набор точек, определяющих кривую B от H
bdata = [ 0.0,0.3,0.8,1.12,1.32,1.46,1.54,1.62,1.74,1.87,1.99,2.046,2.08]; 
hdata = [ 0,40,80,160,318,796,1590,3380,7960,15900,31800,55100,79600];
for n in range(0,len(bdata)):
	femm.mi_addbhpoint('Iron', bdata[n],hdata[n]);

femm.mi_addblocklabel(0,(outer_stator+inner_stator)/2)
femm.mi_selectlabel(0,(outer_stator+inner_stator)/2)
femm.mi_setblockprop('Iron', 0, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()

# добавить воздушную среду в зазор между статором и ротором
femm.mi_addblocklabel(0,rotor_radius+air_gap/2)
femm.mi_selectlabel(0,rotor_radius+air_gap/2)
femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()

# добавить материал бандажа ротора из титана
femm.mi_addmaterial('Titanium', 1, 1, 0, 0, 1.798, 0, 0, 1, 0, 0, 0);
femm.mi_addblocklabel(0,(rotor_radius+magnet_radius)/2)
femm.mi_selectlabel(0,(rotor_radius+magnet_radius)/2)
femm.mi_setblockprop('Titanium', 0, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()

# добавить постоянный магнит на ротор
magnet_angle = 40
femm.mi_getmaterial('NdFeB 37 MGOe');
femm.mi_addblocklabel(0,0)
femm.mi_selectlabel(0,0)
femm.mi_setblockprop('NdFeB 37 MGOe', 1, 0, '<None>', magnet_angle, '<None>', '<None>')
femm.mi_clearselected()

# Обмотки изготовлены из медного провода
femm.mi_addmaterial('Coil', 1, 1, 0, 0, 58, 0, 0, 1, 0, 0, 0);
# задать ток 'i1' 20 ампер
# c последовательным соединением проводников
femm.mi_addcircprop('i1', 20, 1);
# задать ток 'i2' 0 ампер
# c последовательным соединением проводников
femm.mi_addcircprop('i2', 0, 1);

# установить токи и число витков катушек
current = [0]*2*p
current[0] = 'i1'
current[p] = 'i1'
windings = [0]*2*p
windings[0] = 40
windings[p] = -40

k = 0; # для перебора индексив массива

for i in range (0,2*p):
        x_left = math.cos(i*angle+angle/3)*(inner_stator-inner_tooth/2)
        y_left = math.sin(i*angle+angle/3)*(inner_stator-inner_tooth/2)
        femm.mi_addblocklabel(x_left,y_left)
        femm.mi_selectlabel(x_left,y_left)
        # катушка с числом витков 40 и током 'i1'
        femm.mi_setblockprop('Coil', 0, 1, current[k], 0, 0, windings[k]);
        femm.mi_clearselected()
        x_right = math.cos(-i*angle-angle/3)*(inner_stator-inner_tooth/2)
        y_right = math.sin(-i*angle-angle/3)*(inner_stator-inner_tooth/2)
        femm.mi_addblocklabel(x_right,y_right)
        femm.mi_selectlabel(x_right,y_right)
        # катушка с числом витков 40 и током 'i2'
        femm.mi_setblockprop('Coil', 0, 1, current[k], 0, 0, -windings[k]);
        femm.mi_clearselected()
        k+=1

# для автоматического построения границ с граничными условиями
femm.mi_makeABC(7,2*outer_stator,0,0,0)

# точки контура для определения индукции в спинке статора
x_Bc_1 = math.cos(math.pi*135/180)*inner_stator
y_Bc_1 = math.sin(math.pi*135/180)*inner_stator
femm.mi_addnode(x_Bc_1,y_Bc_1)
x_Bc_2 = math.cos(math.pi*135/180)*outer_stator
y_Bc_2 = math.sin(math.pi*135/180)*outer_stator
femm.mi_addnode(x_Bc_2,y_Bc_2)

# точка для определения плотности тока J в катушке обмотки
x_J = math.cos(angle/3)*(inner_stator-inner_tooth/2)
y_J = math.sin(angle/3)*(inner_stator-inner_tooth/2)

# Изменение масштаба
femm.mi_zoomnatural()

# Сохранение файла программы FEMM
femm.mi_saveas('motor_model_FEMM.fem');

# анализ проблемы и загрузка решения после завершения анализа
femm.mi_analyze()
femm.mi_loadsolution()

# выбрать контур для определения магнитной индукции в спинке
femm.mo_selectpoint(x_Bc_1,y_Bc_1);
femm.mo_selectpoint(x_Bc_2,y_Bc_2);

# сохранить данные в файл
femm.mo_makeplot(1,500,'motor_model_FEMM.txt',1);

# загрузить данные из файла
file = open('motor_model_FEMM.txt', 'r')
lines=file.readlines()
array=[]
for x in lines:
    array.append(float(x.split('\t')[1]))
file.close()

# определяем среднее значение индукции в спинке
Bc_mean = sum(array)/len(array)

# определяем плотность тока в катушке
Rez_J = femm.mo_getpointvalues(x_J,y_J)
J = Rez_J[8]

print("Bc_mean =", Bc_mean, "J =", J)

# закрыть приложение FEMM
#femm.closefemm()
