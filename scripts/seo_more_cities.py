# -*- coding: utf-8 -*-
"""Ciudades adicionales de México para las páginas servicio × ciudad (cobertura nacional, 11 nov 2026).

Mismas reglas que seo_data.py: hechos públicos y generales por ciudad (industrias, parques, zonas),
sin cifras inventadas, sin clientes. Cada ciudad lleva los 3 servicios núcleo: vigilancia (monitoreo),
auditoría y respuesta a incidentes.
"""

CORE = ["monitoreo", "auditoria", "incidentes"]

LOCAL_REMOTO = ("Atendemos {ciudad} de forma remota: la vigilancia corre igual sin importar dónde esté tu oficina, "
                "la llamada mensual es por videollamada y, para el Arranque o un incidente, podemos viajar. "
                "Operamos desde Torreón, Coahuila, para todo México, con el mismo precio en todo el país.")

def c(key, name, region, code, lat, lon, ind, context, slug=None, place=None):
    return dict(key=key, slug=slug or key, name=name, region=region,
                geo=(code, place or f"{name}, {region}, México", f"{lat}, {lon}"),
                existing=None, ind=ind, services=list(CORE), context=context,
                local=LOCAL_REMOTO.format(ciudad=name))

CITIES_MX_MORE = [
c("puebla", "Puebla", "Puebla", "MX-PUE", "19.0414", "-98.2063", ["automotriz", "logistica", "salud"],
  "Puebla vive de la industria automotriz y sus proveedores (la planta de Volkswagen en Cuautlancingo, la de Audi en San José Chiapa y los parques FINSA, Chachapa y Ciudad Textil), de la textil y del comercio de la zona metropolitana con Cholula y Tlaxcala. Las pymes que surten a las armadoras firman anexos de seguridad de la información que casi nadie revisa después de firmarlos; la vigilancia continua es la forma barata de cumplirlos de verdad."),
c("tijuana", "Tijuana", "Baja California", "MX-BCN", "32.5149", "-117.0382", ["automotriz", "salud", "logistica"],
  "Tijuana es la capital de la maquila de dispositivos médicos, electrónica y aeroespacial, con parques como Otay, El Florido, Pacífico y Valle Bonito pegados a la frontera con San Diego. Muchas plantas son filiales de empresas de Estados Unidos que exigen a sus proveedores locales controles tipo NIST o CMMC; un proveedor mexicano sin vigilancia de su correo y sus servidores es el eslabón que los auditores ven primero."),
c("leon", "León", "Guanajuato", "MX-GUA", "21.1221", "-101.6827", ["comercio", "automotriz", "logistica"],
  "León es la capital del calzado y la piel, con cientos de talleres, marcas y tiendas en línea, y el corredor automotriz del Bajío a un paso: Puerto Interior en Silao, las plantas de GM, Toyota y Mazda y sus proveedores. Las tiendas en línea de calzado concentran pagos con tarjeta y datos de clientes; los proveedores automotrices, portales de pedidos y acceso remoto a su ERP."),
c("merida", "Mérida", "Yucatán", "MX-YUC", "20.9674", "-89.5926", ["salud", "turismo", "tecnologia"],
  "Mérida creció como polo de salud privada, inmobiliario, turismo y servicios de tecnología (parques científicos y centros de desarrollo que atienden a clientes de Estados Unidos). Clínicas con expediente electrónico, desarrolladoras con portales de clientes y agencias de software con repositorios llenos de llaves de sus clientes son el perfil típico de riesgo en la ciudad."),
c("san-luis-potosi", "San Luis Potosí", "San Luis Potosí", "MX-SLP", "22.1565", "-100.9855", ["automotriz", "logistica", "metalurgia"],
  "San Luis Potosí es nodo logístico e industrial del centro del país: las plantas de General Motors y BMW, los parques Logistik, WTC Industrial, Millennium y Tres Naciones, y una base metalmecánica y de autopartes que surte al Bajío y al norte. Los proveedores de las armadoras manejan planos, pedidos y facturación por portales y correo; eso es lo que más se ataca."),
c("aguascalientes", "Aguascalientes", "Aguascalientes", "MX-AGU", "21.8853", "-102.2916", ["automotriz", "tecnologia", "comercio"],
  "Aguascalientes gira alrededor de Nissan y de los parques industriales PIVA, San Francisco de los Romo y Chichimeco, con un sector de tecnología y centros de datos en crecimiento y comercio regional fuerte. Las pymes proveedoras de la industria automotriz y las empresas de software locales suelen tener acceso remoto abierto y repositorios sin revisión."),
c("ciudad-juarez", "Ciudad Juárez", "Chihuahua", "MX-CHH", "31.6904", "-106.4245", ["automotriz", "logistica", "salud"],
  "Ciudad Juárez es una de las zonas de maquila más grandes de México: electrónica, arneses y autopartes, dispositivos médicos y parques como Intermex, Bermúdez, Omega y Los Fuentes, con operación ligada a El Paso. Los proveedores y transportistas que cruzan la frontera manejan documentos aduanales, pedidos y pagos por correo, y la suplantación de correos para cambiar cuentas de pago es el fraude más repetido."),
c("hermosillo", "Hermosillo", "Sonora", "MX-SON", "29.0729", "-110.9559", ["automotriz", "metalurgia", "agro"],
  "Hermosillo combina la planta de Ford y su cadena de proveedores en el Parque Industrial Dynatech y la Zona Industrial, con minería, agroindustria y servicios para el estado. Las empresas medianas tienen ERP con acceso remoto para el proveedor de sistemas, correo sin SPF, DKIM ni DMARC y respaldos que nadie ha probado."),
c("culiacan", "Culiacán", "Sinaloa", "MX-SIN", "24.8091", "-107.3940", ["agro", "comercio", "salud"],
  "Culiacán es el centro de la agroindustria y la exportación de hortalizas de Sinaloa, con empaques, distribuidoras, transportistas y un sector de salud privada y comercio grande para la región. Las empacadoras y distribuidoras operan con sistemas de facturación y logística expuestos a internet y con proveedores que entran por escritorio remoto."),
c("mazatlan", "Mazatlán", "Sinaloa", "MX-SIN", "23.2494", "-106.4111", ["turismo", "logistica", "comercio"],
  "Mazatlán vive del turismo, el puerto y la pesca: hoteles, tour operadores, desarrollos inmobiliarios, agencias navieras y comercio. Los hoteles manejan tarjetas de huéspedes y motores de reserva; los operadores del puerto, documentos y pagos con clientes extranjeros. Ambos son objetivos de phishing y de clonación de sitios."),
c("zacatecas", "Zacatecas", "Zacatecas", "MX-ZAC", "22.7709", "-102.5833", ["metalurgia", "gobierno", "turismo"],
  "Zacatecas es minería (Fresnillo, Peñasquito y sus contratistas), proveedores de gobierno estatal, turismo y servicios. Los contratistas mineros manejan contratos y pagos con empresas grandes que exigen controles de seguridad; un correo tomado o un servidor expuesto puede costar el contrato."),
c("morelia", "Morelia", "Michoacán", "MX-MIC", "19.7060", "-101.1950", ["gobierno", "agro", "comercio"],
  "Morelia concentra gobierno estatal y sus proveedores, universidades, servicios profesionales y la agroindustria del aguacate y los berries que exporta desde Uruapan y la región. Empacadoras y exportadoras con certificaciones de inocuidad y clientes en Estados Unidos reciben cada vez más cuestionarios de ciberseguridad."),
c("toluca", "Toluca", "Estado de México", "MX-MEX", "19.2826", "-99.6557", ["automotriz", "logistica", "despachos"],
  "Toluca y su corredor industrial (Lerma, Toluca 2000, Santiago Tianguistenco, Ocoyoacac) reúnen plantas automotrices, farmacéuticas, de alimentos y logística para el centro del país, además de despachos y servicios que atienden a la Ciudad de México. Las pymes proveedoras de esos corredores son el caso típico de servidor con acceso remoto y correo sin autenticar."),
c("cancun", "Cancún", "Quintana Roo", "MX-ROO", "21.1619", "-86.8515", ["turismo", "comercio", "salud"],
  "Cancún y la Riviera Maya son hotelería, tour operadores, agencias, desarrollos inmobiliarios y turismo médico, con una temporada alta que no perdona caídas. Motores de reserva, pasarelas de pago, sitios clonados para vender tours falsos y correos de 'cambio de cuenta' a proveedores son los incidentes que más se repiten."),
c("veracruz", "Veracruz", "Veracruz", "MX-VER", "19.1738", "-96.1342", ["logistica", "comercio", "gobierno"],
  "Veracruz es el puerto más importante del Golfo: agencias aduanales, navieras, transportistas, almacenes fiscales y comercio exterior, más proveedores de gobierno y servicios. Las agencias aduanales manejan pedimentos, pagos de impuestos y datos de clientes por correo y portales; un buzón tomado ahí sale caro el mismo día."),
c("villahermosa", "Villahermosa", "Tabasco", "MX-TAB", "17.9892", "-92.9475", ["logistica", "gobierno", "comercio"],
  "Villahermosa es la capital de los servicios a la industria petrolera y energética del sureste: contratistas, transportistas, talleres y proveedores de Pemex y de las empresas del sector, más gobierno y comercio. Los contratistas firman anexos de seguridad de la información en licitaciones y casi ninguno tiene quien vigile su correo y sus servidores."),
c("tampico", "Tampico", "Tamaulipas", "MX-TAM", "22.2331", "-97.8614", ["logistica", "salud", "comercio"],
  "Tampico, Madero y Altamira forman un corredor de puerto, petroquímica, logística y salud privada que atiende a la Huasteca. Agencias aduanales, transportistas, clínicas y distribuidoras operan con sistemas expuestos a internet y proveedores externos de TI."),
c("oaxaca", "Oaxaca", "Oaxaca", "MX-OAX", "17.0732", "-96.7266", ["turismo", "gobierno", "comercio"],
  "Oaxaca es turismo, gastronomía, mezcal y artesanía con ventas en línea, además de gobierno estatal, universidades y comercio. Hoteles boutique, tour operadores y marcas de mezcal con tienda en línea manejan pagos con tarjeta y clientes extranjeros; los sitios clonados y el fraude por correo son el riesgo más común."),
c("tuxtla-gutierrez", "Tuxtla Gutiérrez", "Chiapas", "MX-CHP", "16.7516", "-93.1029", ["gobierno", "comercio", "salud"],
  "Tuxtla Gutiérrez concentra gobierno estatal y federal, salud, universidades, comercio y distribuidoras que surten al estado. Los proveedores de gobierno y las distribuidoras regionales son pymes con ERP, facturación electrónica y correo corporativo sin nadie que los vigile."),
c("mexicali", "Mexicali", "Baja California", "MX-BCN", "32.6245", "-115.4523", ["automotriz", "agro", "gobierno"],
  "Mexicali es capital del estado, maquila aeroespacial, electrónica y automotriz (parques PIMSA, Calafia, El Vigía) y agroindustria del Valle de Mexicali, con operación cruzada con Calexico e Imperial Valley. Los proveedores de las plantas y los exportadores agrícolas reciben requisitos de seguridad de clientes de Estados Unidos."),
c("la-paz", "La Paz", "Baja California Sur", "MX-BCS", "24.1426", "-110.3128", ["turismo", "gobierno", "comercio"],
  "La Paz es gobierno estatal, turismo náutico, pesca deportiva, inmobiliario y comercio que abastece a Los Cabos. Hoteles, marinas y desarrolladoras manejan reservas y pagos de clientes extranjeros, y su proveedor de sistemas suele estar a cientos de kilómetros."),
c("pachuca", "Pachuca", "Hidalgo", "MX-HID", "20.1011", "-98.7591", ["gobierno", "logistica", "salud"],
  "Pachuca es gobierno estatal, universidades, salud y la Plataforma Logística de Hidalgo y los parques industriales de Tizayuca y Ciudad Sahagún al sur, a una hora de la Ciudad de México. Los proveedores de gobierno y las empresas de los parques son pymes con correo, ERP y portales expuestos sin vigilancia."),
c("cuernavaca", "Cuernavaca", "Morelos", "MX-MOR", "18.9242", "-99.2216", ["automotriz", "salud", "despachos"],
  "Cuernavaca tiene el corredor industrial CIVAC (automotriz, farmacéutica, alimentos), clínicas y hospitales privados, despachos y servicios para quienes trabajan en la Ciudad de México. Las plantas de CIVAC exigen controles a sus proveedores locales; las clínicas manejan expedientes y resultados en línea."),
c("acapulco", "Acapulco", "Guerrero", "MX-GRO", "16.8531", "-99.8237", ["turismo", "comercio", "gobierno"],
  "Acapulco es hotelería, restaurantes, inmobiliario y comercio, con una recuperación en marcha que trajo nuevos sistemas de reservas, pagos y marketing en línea montados rápido y sin revisión. Motores de reserva, sitios de hoteles y correos de ventas son el objetivo más frecuente."),
]
