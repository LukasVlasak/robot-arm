# Design Ideas and Things to Investigate

This document contains ideas, questions and possible design improvements that is being investigated during the development of the robot.


## Idea: Aluminium link instead of PLA

### Question
Would an aluminium link provide better stiffness and lower deflection than a PLA link without significantly increasing the weight?

### Why investigate it?
We can make the PLA link much thicker than the aluminium one without incresing the weight

### Result
Not tested yet.


# Co delat

## 1. Tvar linku
Jakmile budem premyslet o tvaru linku, tak vzit v potaz i to jak se to bude tisknout - neco se tiskne hur, a ma to vetsi riziko na to, ze se to rozjebe - hlavne pri previsech. 

### 1.1 jak moc budem potrebovat material kolem osy y
Kdyz otocime s ramenem a pak to rychle zastavi, tak se to bude mrcasit nebo ne? -> kolik materialu proste budem potrebovat v tech linkach

### 1.2 Delka tech ramen?
Bude mozny vytisknout to nejdelsi rameno na tiskarne v labu? Protoze to chce vytisknout v co nejmensich kusech - nejdelsi je 0.3m
Prozkoumat vice delku tech ramen - je to dostacujici, neni ten kinmatickej model nejakej jebnutej? protoze se tam neohyba ten posledni link
#### 1.2.1 Offsety
Proc offsety? - aby jsi byl robota schopny prevest pri transportu
Vykrati se ty offsety? Kdyz je udelam zrcadlove

### 1.3 Celkovej tvar toho linku
Jakej je nejlepsi tvar na ohybani, jak to bude s hmostnosti, proc tohle a ne tamto, na jakejch dalsich faktorech zalezi?

## 2. Hlinik vs Plast

## 3. Tvar jointy
Jak to bude vypadat, jak moc to musi betjt tlusty aby se to nerozbilo - jaka cca bude vaha? jakej celkovej bude tvar toho a proc?

## 4. Ozubeny kolecka
Zjistit jstli to ma smysl
Prevadet moment ozubenyma koleckama a snizit tak vahu - motory vazej hodne
Kolik vahy usetris?
Nosnost? - jestli by to vydrzelo





## Sila kterou musi vynalozit motor pro otoceni s ramenem s ramenem
### Je lepsi dat vetsi motor primo do zakladny aby s robotem otacel do stran nebo o jedno vis aby otacel nahoru a dolu?

- Torque moment required => T = r * sin(omega) * F
                        => T = r * sin(omega) * m*g (omega = 90 stupnu -> gravitacni sila pusobi kolmo)
                        => T = r * 1 * m*g
                        => T = r * m * g (r - x-ova vzdalenost teziste, m => teziste)


#### zjistuji m - 3 motory + 3 linky + end effector
- jeden motor ma 83g - https://robotis.us/products/dynamixel-xm430-w350-t?srsltid=AU7gw4WdXu83MEWZ_S2w-UYNEthsW0pRe4yIigRo7nuGApWx5hD06XKj&dxl1=XM430-W350-T&dxl2=XM430-W210-R
- 
- link => cca ramena dlouhe 0.3, 0.28, 0.16 -> vaha jednoho cca, pocitam PALG
- kolik cca muze vazit jeden link na robota vytisknuty s PALG, kdyz bude mit 0.3 potom 0.28 a 0.16m dlouhe a tvar kruhovej a 35mm vnejsi a 25mm vnitrni
- podle chata -> 432g dohromady
-
- end efectorr => 30g + jointy cca 20g na kazdy - joint u endeeffectoru, takze treba 45g => 75g

pocitam pres zjednodusene teziste tzn. rCOM = x1*m1+x2*m2... /M

vyvorim skript, abych si kdyztak hodnoty mohl menit - pocitam s tim ze linky maji teziste uprosted, jointy budou dlouhe cca 5cm a maji teziste tky uprostred a motory jsou dlouhe cca 5cm a maji teziste taky ve prostred - coz by melo vzdy cca sedet

#### Vysledky
Torque needed: 4.1079375Nm

Stall torque mensiho motor: 4.1Nm

Stall torque vetsiho motor: 7.3Nm

### Samotne otoceni
- stejne assumptions jako predtim
- zalezi na moment of inertia (moment setrvacnosti), ktery pocita jak je hmota rozlozena vzhledem k ose otaceni
- potom spocitam Torque, ktery je potreba pro urcite zrcyhleni
- vytvorit testovaci skript