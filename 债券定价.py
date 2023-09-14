class Coupon():
    def __init__(self, year, m, couponrate, i, P=1000):
        self.year = year
        self.m = m
        self.couponrate = couponrate
        self.i = i
        self.P = P
        self.T = self.year * self.m
        self.dis_rate = self.i / self.m
        self.interest = self.P * self.couponrate / self.m

    def get_pv(self):
        s = 0
        for t in range(1, int(self.T+1)):
            a = self.interest/(1+self.dis_rate)**t
            s += a
        dis_price = self.P/(1+self.dis_rate)**(self.T)
        self.PV = s + dis_price
        return self.PV

    def get_D(self):
        s = 0
        for t in range(1, int(self.T+1)):
            a = t*self.interest/(1+self.dis_rate)**t
            s += a
        final_ct = self.T*self.P/(1+self.dis_rate)**self.T
        s += final_ct
        self.D = s/self.get_pv()/self.m
        return self.D

    def get_Dm(self):
        return self.get_D()/(1+self.dis_rate)

    def get_convex(self):
        s = 0
        for t in range(1, int(self.T+1)):
            a = t*(t+1)*self.interest/(1+self.dis_rate)**t
            s += a
        final_ct = self.T*(self.T+1)*self.P/(1+self.dis_rate)**self.T
        s += final_ct
        self.convex = s/self.get_pv()/(1+self.dis_rate)**2/self.m**2
        return self.convex


    def get_fv(self):
        s = 0
        for t in range(int(self.T)):
            a = self.interest*(1+self.dis_rate)**t
            s += a
        self.FV = s
        return self.FV

A = Coupon(5.5, 2, 0.125, 0.125)
B = Coupon(15, 2, 0.125, 0.125)
C = Coupon(8, 2, 0.10125, 0.125)


D = Coupon(2.5, 2, 0.10125, 0.125)
E = Coupon(5.5, 2, 0.10125, 0.125)
F = Coupon(5.5, 2, 0.125, 0.125)

# from sympy import symbols
# import sympy
#
#
# x,t= symbols('x t')
# A,B,C= symbols('A B C', function=True)
# f = symbols('f', function=True)
# f = 62.5/(1+x/2)**t
# A = sympy.summation(f, (t, 1, 11))+1000/(1+x/2)**11
# B = x+x**2
# sympy.plot(B)