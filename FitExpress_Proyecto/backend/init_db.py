from backend.database import SessionLocal, engine
from backend import models
import bcrypt

# --- REINICIO LIMPIO DE LA BASE DE DATOS ---
print(" Reiniciando base de datos para aplicar cambios...")
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

print("--- CARGANDO CATÁLOGO COMPLETO (RÚBRICA INTEGRACIÓN) ---")

# Lista Maestra de Productos (Coincide con tu HTML)
productos = [
    # --- BOWLS (IDs 1-6) ---
    models.Producto(
        id=1, nombre="Bowl Quinoa Power", precio_base=7990, tipo="bowl", 
        descripcion="Quinoa, garbanzos, aguacate y vegetales asados.",
        kcal=420, proteina=24, grasas=12, carbs=54, disponible=True,
        imagen_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=500&q=80"
    ),
    models.Producto(
        id=2, nombre="Bowl Proteico Plus", precio_base=8990, tipo="bowl", 
        descripcion="Pollo glaseado con salsa teriyaki y arroz.",
        kcal=520, proteina=40, grasas=18, carbs=50, disponible=True,
        imagen_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80"
    ),
    models.Producto(
        id=3, nombre="Bowl Energía Verde", precio_base=7490, tipo="bowl", 
        descripcion="Espinacas, kale, aguacate y semillas.",
        kcal=380, proteina=22, grasas=10, carbs=48, disponible=True,
        imagen_url="https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?auto=format&fit=crop&w=500&q=80"
    ),
    models.Producto(
        id=4, nombre="Bowl Vegano Supreme", precio_base=8490, tipo="bowl", 
        descripcion="Falafel de lentejas con granada y quinoa.",
        kcal=430, proteina=20, grasas=14, carbs=60, disponible=True,
        imagen_url="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=500&q=80"
    ),
    models.Producto(
        id=5, nombre="Bowl Mediterráneo", precio_base=8990, tipo="bowl", 
        descripcion="Atún fresco, aceitunas y queso feta.",
        kcal=480, proteina=28, grasas=16, carbs=52, disponible=True,
        imagen_url="https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=500&q=80"
    ),
    models.Producto(
        id=6, nombre="Bowl Carne Coreana", precio_base=9490, tipo="bowl", 
        descripcion="Carne marinada, kimchi y huevo.",
        kcal=550, proteina=35, grasas=20, carbs=45, disponible=True,
        imagen_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=500&q=80"
    ),

    # --- SNACKS (IDs 7-8) ---
    models.Producto(
        id=7, nombre="Barra Proteína Almendras", precio_base=1990, tipo="snack", 
        descripcion="Barra energética natural.",
        kcal=180, proteina=15, grasas=8, carbs=12, disponible=True,
        imagen_url="https://images.unsplash.com/photo-1619601875086-009b81185dcc?auto=format&fit=crop&w=500&q=80"
    ),
    models.Producto(
        id=8, nombre="Barra Proteína Chocolate", precio_base=2190, tipo="snack", 
        descripcion="Barra 70% cacao sin azúcar.",
        kcal=210, proteina=18, grasas=9, carbs=15, disponible=True,
        imagen_url="https://images.unsplash.com/photo-1628149332315-482992f5f4c5?auto=format&fit=crop&w=500&q=80"
    ),

    # --- COMBOS (IDs 9-14) ---
    models.Producto(
        id=9, nombre="Combo Energía Total", precio_base=18990, tipo="combo",
        descripcion="2 Bowls proteicos de tu elección, 2 Barras de proteína, 1 Bebida energética natural, 1 Mix de frutos secos", disponible=True,
        imagen_url="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    ),
    models.Producto(
        id=10, nombre="Combo Proteína Max", precio_base=27990, tipo="combo",
        descripcion="3 Bowls altos en proteína, 3 Barras proteicas, 1 Batido de proteína listo, 1 Pack de snacks proteicos", disponible=True,
        imagen_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    ),
    models.Producto(
        id=11, nombre="Combo Vegano Power", precio_base=16990, tipo="combo",
        descripcion="2 Bowls veganos gourmet, 2 Snacks vegetales crujientes, 1 Dip de hummus artesanal, 1 Bebida vegetal", disponible=True,
        imagen_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    ),
    models.Producto(
        id=12, nombre="Combo Semanal Fit", precio_base=39990, tipo="combo",
        descripcion="5 Bowls variados (1 por día), 5 Snacks saludables, 2 Bebidas funcionales, 1 Guía de nutrición digital", disponible=True,
        imagen_url="https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    ),
    models.Producto(
        id=13, nombre="Combo Desayuno Express", precio_base=14990, tipo="combo",
        descripcion="3 Bowls de avena y granola, 3 Smoothies listos para beber, 2 Muffins saludables, 1 Café o té de especialidad", disponible=True,
        imagen_url="https://images.unsplash.com/photo-1551218808-94e220e084d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    ),
    models.Producto(
        id=14, nombre="Combo Pareja Saludable", precio_base=22990, tipo="combo",
        descripcion="4 Bowls (2 para cada uno), 4 Barras de proteína, 2 Bebidas energéticas, 2 Postres saludables", disponible=True,
        imagen_url="https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    ),
    models.Producto(
        id=99, 
        nombre="Bowl Personalizado", 
        precio_base=6990, 
        tipo="bowl", 
        descripcion="Bowl a medida con ingredientes seleccionados.",
        kcal=0, proteina=0, grasas=0, carbs=0, # Valores variables
        disponible=True,
        imagen_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80"
    )
]

# Guardar productos forzando IDs
for p in productos:
    db.merge(p)
db.commit()
print(f" {len(productos)} Productos cargados correctamente.")

# --- 3. USUARIOS (ADMIN Y CLIENTE) ---
print("--- CREANDO USUARIOS ---")

# Admin (Tu cuenta real)
email_admin = "jesuszavaleta55@gmail.com"
pass_admin = "042025"
hashed_pw_admin = bcrypt.hashpw(pass_admin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

admin = models.Usuario(
    nombre="Jesus Admin",
    email=email_admin,
    hashed_password=hashed_pw_admin,
    rut="99.999.999-9",
    direccion="Oficina Central FitExpress",
    comuna="Santiago",
    rol="admin" # ROL CLAVE PARA LA RÚBRICA (Gestión de Acceso)
)
db.add(admin)
db.commit()
db.add(models.Carrito(usuario_id=admin.id)) # Carrito para admin
db.commit()
print(f" Admin creado: {email_admin}")

# Cliente de Prueba
email_cliente = "cliente@prueba.com"
hashed_pw_cliente = bcrypt.hashpw("12345".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cliente = models.Usuario(
    nombre="Juan Cliente",
    email=email_cliente,
    hashed_password=hashed_pw_cliente,
    rut="11.111.111-1",
    direccion="Av. Providencia 123",
    comuna="Providencia",
    rol="cliente"
)
db.add(cliente)
db.commit()
db.add(models.Carrito(usuario_id=cliente.id))
db.commit()
print(f" Cliente creado: {email_cliente}")

db.close()
print("🚀 BASE DE DATOS LISTA PARA LA DEMO")