function ret=fivedegreepol(tick,desttime,e0,ef,s0,sf,acc0,accf)

%x = (tick.*10)/(desttime*100);

x = tick;
tf = desttime;

%ret=x.*x.*x.* (100.0/1000.0) + x.*(-150.0/10000) + x.*(60/100000);

a0 = e0;
a1 = s0;
a2 = 1/2 * acc0;
a3 = 1/(2 * tf^3)*(20 * ef - 20 * e0 - (8*sf + 12 * s0)*tf - (3*acc0 - accf)*tf^2);
a4 = 1/(2 * tf^4)*(30 * e0 - 30 * ef + (14*sf + 16*s0)*tf + (3*acc0 - 2*accf)*tf^2);
a5 = 1/(2 * tf^5)*(12 * ef - 12 * e0 - (6 *sf + 6*s0)*tf - (acc0-accf)*tf^2);

ret = a0 + a1 * x + a2 *(x.*x) + a3*((x.*x).*x) + a4*(x.*x.*x.*x) + a5*(x.*x.*x.*x.*x);


end