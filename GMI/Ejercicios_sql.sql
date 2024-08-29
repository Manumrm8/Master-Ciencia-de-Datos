-- Ejercicio 2--

select nombre, color
from articulos
where color like "_o%";

-- Ejercicio 3--
select * from articulos where peso<100 order by peso asc;

-- Ejercicio 4--
select * from obras where ciudad != "Madrid";

-- Ejercicio 5--
select distinct(a.a), a.nombre
from envios e
join articulos a on a.a=e.a
where e.o=2;

-- Ejercicio 6--
select a.a, a.nombre, s.s, s.nombre, o.o, o.nombre
from envios e
join articulos a on a.a=e.a
join suministradores s on s.s=e.s 
join obras o on o.o=e.o
where e.o=2;

-- Ejercicio 7--
select s.nombre
from envios e
join suministradores s on s.s=e.s
where s.s=3;

-- Ejercicio 8--
select o.nombre, sum(e.cantidad)
from envios e
join obras o on e.o=o.o
group by o.o;

-- Ejercicio 9--
select o.o, o.nombre
from obras o
join envios e on e.o=o.o
group by o.o
having sum(cantidad)>100;


-- Ejercicio 10--
select s.nombre, count(*) n_envios, sum(cantidad), sum(peso/1000)
from envios e
join suministradores s on e.s=s.s
join articulos a on a.a=e.a
group by s.s;

-- Ejercicio 11--
select o, cantidad 
from envios
where cantidad<(select avg(e.cantidad)
from envios e);

-- Ejercicio 12--
select o, cantidad
from envios
where cantidad>=all(select cantidad from envios where o=2);

-- Ejercicio 13--
select s.nombre
from suministradores s
join envios e on e.s=s.s
where e.o not in(select o from obras where nombre="PUERTO") ;

-- Este está mal, el siguiente es el bueno--

select nombre from suministradores where s
not in
(select e.s
from envios e
join obras o on e.o=o.o
where o.nombre="puerto");


-- Ejercicio 14--

select nombre from suministradores s
where "destornillador"=all(
select a.nombre
from envios e
join articulos a on e.a=a.a
join obras o on e.o=o.o
where o.nombre="carretera"and e.s=s.s);

-- Ejer