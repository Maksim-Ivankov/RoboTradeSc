

from datetime import datetime



class Print_graph:
    def __init__(self,master,settings):
        self.settings_window55()
        self.master = master
        self.settings = settings

        self.df = self.settings['df']
        self.VOLUME = self.settings['VOLUME']
        self.step_input = self.settings['step_input']
        self.trend = self.settings['trend']
        self.TP = self.settings['TP']
        self.SL = self.settings['SL']
        

        self.height_canvas = 500
        self.width_canvas = 600
        self.width_telo = 3 # Ширина тела свечи
        self.width_spile = 1 # Ширина хвоста, шпиля
        self.flag_pricel = 0 # флаг для логики прицела
        self.bg="#161A1E"
        self.width=self.width_canvas
        self.height=self.height_canvas

        
        

        # Это то, что позволяет использовать мышь
        self.canvas.bind("<ButtonPress-1>", lambda event: self.move_start(event))
        self.canvas.bind("<B1-Motion>", lambda event:self.move_move(event))
        self.canvas.bind("<MouseWheel>",lambda event:self.zoomer(event))
        self.canvas.bind('<Motion>', lambda event:self.mmove(event,self.height_canvas))

        self.paint_bar(self.canvas,self.df,self.df,self.VOLUME,self.height_canvas,self.width_canvas)
        self.print_setka_from_graph(self.height_canvas)
        # printn_tools(cavas_tools)

        self.print_tp_sl(self.canvas,self.TP,self.SL,self.height)
        self.print_place_input(self.step_input,self.df,self.canvas,self.height)

        self.win55.mainloop()
        



    # перемещение канваса мышкой старт
    def move_start(self,event):
        self.canvas.scan_mark(event.x, event.y)
        self.canvas_price.scan_mark(0, event.y)
        self.canvas_date.scan_mark(event.x, 0)
        self.canvas_volume.scan_mark(event.x, 60)

    # перемещение канваса мышкой отпускание 
    def move_move(self,event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.canvas_price.scan_dragto(0, event.y, gain=1)
        self.canvas_date.scan_dragto(event.x, 0, gain=1)
        self.canvas_volume.scan_dragto(event.x, 60, gain=1)

    # зум колесиком мыши
    def zoomer(self,event):
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)  
        if (event.delta > 0):
            self.canvas.scale("all", true_x, true_y, 1.1, 1.1)
            self.canvas_price.scale("all", 20, true_y, 1.1, 1.1)
            self.canvas_date.scale("all", true_x, 14, 1.1, 1.1)
            self.canvas_volume.scale("all", true_x, 80, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", true_x, true_y, 0.9, 0.9)
            self.canvas_price.scale("all", 20, true_y, 0.9, 0.9)
            self.canvas_date.scale("all", true_x, 14, 0.9, 0.9)
            self.canvas_volume.scale("all", true_x, 80, 0.9, 0.9)
        #canvas_date.configure(scrollregion = canvas_date.bbox("all"))

    # отображает перекрестье на графике, изменяет цену и время
    def mmove(self,event,height_canvas):
        x0 = self.canvas.canvasx(0)
        y0 = self.canvas.canvasy(0)
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)  
        if self.flag_pricel!=0:
            # прицел
            self.canvas.coords(self.canvas_id,x, -1000, x, 10000)
            self.canvas_volume.coords(self.canvas_id3,x, -1000, x, 10000)
            self.canvas.coords(self.canvas_id2,0, y, 10000, y)
            # цена
            self.canvas_price.coords(self.price_rectangle,0, y-7,46, y+7)
            self.canvas_price.coords(self.price_rectangle_text,22, y)
            text_price = round(float((((height_canvas-y)*self.OldRange)/self.NewRange)+self.price_min),1)
            self.canvas_price.itemconfigure(self.price_rectangle_text, text=text_price)
            # дата
            self.canvas_date.coords(self.date_rectangle_text,x, 14)
            self.canvas_date.itemconfigure(self.date_rectangle_text, text=self.get_all_values(x))
            # canvas.coords(price_rectangle_polosa,x0+width_canvas-46, y0, x0+width_canvas, y0+height_canvas)

            return
        self.canvas_id = self.canvas.create_line(x, 0, x, 10000, width=1, fill='#424747')
        self.canvas_id3 = self.canvas_volume.create_line(x, 0, x, 10000, width=1, fill='#424747')
        self.canvas_id2 = self.canvas.create_line(0, y, 10000, y, width=1, fill='#424747')

        self.print_real_price_x(x,y)
        self.flag_pricel = 1


    # находим дату по интервалу
    def get_all_values(self,age):
       for key, value in self.mass_date_interval_graph.items():
          if (age >= key[0] and age <= key[1]):
            return value


    # рисует прямоугольник с ценой справа графика и временем внизу
    def print_real_price_x(self,x,y):
        self.price_rectangle = self.canvas_price.create_rectangle(x+0, y+0, x+60, y+30, fill="#363A45",outline='#363A45')
        self.price_rectangle_text = self.canvas_price.create_text(100,10,fill="#DADBDD",font=('Purisa',8),text='124112')
        self.date_rectangle_text = self.canvas_date.create_text(100,10,fill="#DADBDD",font=('Purisa',8),text='124112')
        pass


    # рисуем все свечи по историческим
    def paint_bar(self,canv,prices,prices_old,VOLUME,height_canvas,width_canvas):
        # определяем границы для масштабирования графика цены
        self.price_max = (prices_old.loc[prices_old['close'] == prices_old['close'].max()].iloc[0]['close'])
        self.price_min = (prices_old.loc[prices_old['close'] == prices_old['close'].min()].iloc[0]['close'])
        self.OldRange = (self.price_max - self.price_min) 
        self.NewRange = height_canvas 
        self.OldRange1 = (VOLUME)  
        self.NewRange1 = (width_canvas/(144/VOLUME))  
        # определяем границы для масштабирования графика объёмов
        price_max_volume = (prices_old.loc[prices_old['VOLUME'] == prices_old['VOLUME'].max()].iloc[0]['VOLUME'])
        price_min_volume = (prices_old.loc[prices_old['VOLUME'] == prices_old['VOLUME'].min()].iloc[0]['VOLUME'])
        OldRange_volume = (price_max_volume - price_min_volume) 
        NewRange_volume = 110     

        self.mass_date_interval_graph = {}
        self.mass_date_line = []
        for i in range(0,3000,20):
            self.mass_date_line.append(((i * self.NewRange1) / self.OldRange1))
        for index, row in prices.iterrows():
            x0 = ((index * self.NewRange1) / self.OldRange1)
            self.mass_date_interval_graph[(x0-2,x0+2)] = datetime.fromtimestamp(int(row['open_time']/1000)).strftime('%d.%m.%Y %H:%M')
            y0 = (((row['open'] - self.price_min) * self.NewRange) / self.OldRange)
            y1 = (((row['close'] - self.price_min) * self.NewRange) / self.OldRange)
            high = (((row['high'] - self.price_min) * self.NewRange) / self.OldRange)
            low = (((row['low'] - self.price_min) * self.NewRange) / self.OldRange)
            self.paint_candle(canv,x0,y0,y1,high,low,height_canvas)

            VOLUME_y = (((row['VOLUME'] - price_min_volume) * NewRange_volume) / OldRange_volume)
            self.paint_one_volume(self.canvas_volume,x0,y0,y1,VOLUME_y)

    # рисуем одну свечу    
    def paint_candle(self,canv,x0,y0,y1,high,low,height_canvas):
        height = height_canvas
        if y0>=y1:
            canv.tag_lower(canv.create_line(x0+2,height-high,x0+2,height-y0,width=1,fill="#F6465D"))
            canv.tag_lower(canv.create_rectangle(x0, height-y0, x0+self.width_telo, height-y1,outline="#F6465D", fill="#F6465D"))
            canv.tag_lower(canv.create_line(x0+2,height-low,x0+2,height-y1,width=1,fill="#F6465D"))
        if y0<y1:
            canv.tag_lower(canv.create_line(x0+2,height-high,x0+2,height-y0,width=1,fill="#0ECB81"))
            canv.tag_lower(canv.create_rectangle(x0, height-y0, x0+self.width_telo, height-y1,outline="#0ECB81", fill="#0ECB81"))
            canv.tag_lower(canv.create_line(x0+2,height-low,x0+2,height-y1,width=1,fill="#0ECB81"))

        # рисуем один объём
    def paint_one_volume(self,canv,x0,y0,y1,VOLUME_y):
        if y0>=y1: # красный
            canv.tag_lower(canv.create_rectangle(x0, 80-VOLUME_y, x0+self.width_telo, 80,outline="#F6465D", fill="#F6465D"))
        if y0<y1: # зеленый
            canv.tag_lower(canv.create_rectangle(x0, 80-VOLUME_y, x0+self.width_telo, 80,outline="#0ECB81", fill="#0ECB81"))

    # рисуем сетку
    def print_setka_from_graph(self,height_canvas):
        mass_setka_price = []
        digit = 1000
        prise_mas_min = self.price_round(self.price_min,digit)
        prise_mas_max = self.price_round(self.price_max,digit)
        for i in range(prise_mas_min,prise_mas_min-30*digit,-1000):
            mass_setka_price.append(i)
        for i in range(prise_mas_max,prise_mas_max+30*digit,1000):
            mass_setka_price.append(i)
        for i in range(prise_mas_min,prise_mas_max,1000):
            mass_setka_price.append(i)
        for i in mass_setka_price:
            y = (((i - self.price_min) * self.NewRange) / self.OldRange)   
            self.canvas.tag_lower(self.canvas.create_line(-1000,height_canvas- y, 5000, height_canvas-y, width=1, fill='#1B1F24'))
            self.canvas_price.create_text(20,height_canvas-y,fill="#707985",font=('Purisa',8),text=i)
        for i in self.mass_date_line:
            self.canvas.tag_lower(self.canvas.create_line(i,-1000, i, 5000, width=1, fill='#1B1F24'))
            self.canvas_volume.tag_lower(self.canvas_volume.create_line(i,-1000, i, 5000, width=1, fill='#1B1F24'))


    # фугкция округления - принимает цену, которую хоим округлить и разряд
    def price_round(self,price,digit):
        x = price
        n = digit
        return n * round(x/n)

    # рисуем тейк и стоп
    def print_tp_sl(self,canv,tp,sl,height):
        y_tp = (((float(tp) - self.price_min) * self.NewRange) / self.OldRange)
        y_sl = (((float(sl) - self.price_min) * self.NewRange) / self.OldRange)
        canv.create_line(-5000,height-y_tp,5000,height-y_tp,width=1,fill="#5DEB2E")
        canv.create_line(-5000,height-y_sl,5000,height-y_sl,width=1,fill="#EB2020")

    def print_place_input(self,step_input,df,canv,height):
        y_price_trade = df['close'][int(step_input)]
        y_trade = (((float(y_price_trade) - self.price_min) * self.NewRange) / self.OldRange)
        x_trade = ((float(step_input) * self.NewRange1) / self.OldRange1)+1.5
        canv.create_line(x_trade-6,height-y_trade,x_trade+6,height-y_trade,width=3,fill="#EBEB58")
        canv.create_line(x_trade,height-y_trade-6,x_trade,height-y_trade+6,width=3,fill="#EBEB58")

        self.canvas.xview_moveto(str((abs(-5000)+x_trade-300)/(abs(-5000)+5000)))
        self.canvas_volume.xview_moveto(str((abs(-5000)+x_trade-300)/(abs(-5000)+5000)))
        self.canvas_date.xview_moveto(str((abs(-5000)+x_trade-300)/(abs(-5000)+5000)))











