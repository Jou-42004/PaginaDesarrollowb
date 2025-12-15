from backend.database import SessionLocal, engine
from backend import models
import bcrypt

def init_db():
    # Reiniciar esquema de base de datos
    print("♻️  Reiniciando esquema de base de datos...")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. CATALOGO DE PRODUCTOS
        # ---------------------------------------------------------
        print("➡️  Cargando catálogo de productos...")

        # Nota: 'disponible' se incluye en cada diccionario para evitar duplicidad de argumentos
        PRODUCTOS_DATA = [
            # BOWLS
            {"id": 1, "nombre": "Bowl Quinoa Power", "precio_base": 7990, "tipo": "bowl", "kcal": 420, "proteina": 24, "grasas": 12, "carbs": 54, "descripcion": "Quinoa, garbanzos, aguacate y vegetales asados.", "imagen_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=500&q=80", "disponible": True},
            {"id": 2, "nombre": "Bowl Proteico Plus", "precio_base": 8990, "tipo": "bowl", "kcal": 520, "proteina": 40, "grasas": 18, "carbs": 50, "descripcion": "Pollo glaseado con salsa teriyaki y arroz.", "imagen_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80", "disponible": True},
            {"id": 3, "nombre": "Bowl Energía Verde", "precio_base": 7490, "tipo": "bowl", "kcal": 380, "proteina": 22, "grasas": 10, "carbs": 48, "descripcion": "Espinacas, kale, aguacate y semillas.", "imagen_url": "https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?auto=format&fit=crop&w=500&q=80", "disponible": True},
            {"id": 4, "nombre": "Bowl Vegano Supreme", "precio_base": 8490, "tipo": "bowl", "kcal": 430, "proteina": 20, "grasas": 14, "carbs": 60, "descripcion": "Falafel de lentejas con granada y quinoa.", "imagen_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=500&q=80", "disponible": True},
            {"id": 5, "nombre": "Bowl Mediterráneo", "precio_base": 8990, "tipo": "bowl", "kcal": 480, "proteina": 28, "grasas": 16, "carbs": 52, "descripcion": "Atún fresco, aceitunas y queso feta.", "imagen_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=500&q=80", "disponible": True},
            {"id": 6, "nombre": "Bowl Carne Coreana", "precio_base": 9490, "tipo": "bowl", "kcal": 550, "proteina": 35, "grasas": 20, "carbs": 45, "descripcion": "Carne marinada, kimchi y huevo.", "imagen_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=500&q=80", "disponible": True},
            
            # SNACKS
            {"id": 7, "nombre": "Barra Proteína Almendras", "precio_base": 1990, "tipo": "snack", "kcal": 180, "proteina": 15, "grasas": 8, "carbs": 12, "descripcion": "Barra energética natural.", "imagen_url": "https://images.unsplash.com/photo-1619601875086-009b81185dcc?auto=format&fit=crop&w=500&q=80", "disponible": True},
            {"id": 8, "nombre": "Barra Proteína Chocolate", "precio_base": 2190, "tipo": "snack", "kcal": 210, "proteina": 18, "grasas": 9, "carbs": 15, "descripcion": "Barra 70% cacao sin azúcar.", "imagen_url": "https://images.unsplash.com/photo-1628149332315-482992f5f4c5?auto=format&fit=crop&w=500&q=80", "disponible": True},
            
            # COMBOS
            {"id": 9, "nombre": "Combo Energía Total", "precio_base": 18990, "tipo": "combo", "descripcion": "2 Bowls proteicos de tu elección, 2 Barras de proteína, 1 Bebida energética natural, 1 Mix de frutos secos", "imagen_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", "disponible": True},
            {"id": 10, "nombre": "Combo Proteína Max", "precio_base": 27990, "tipo": "combo", "descripcion": "3 Bowls altos en proteína, 3 Barras proteicas, 1 Batido de proteína listo, 1 Pack de snacks proteicos", "imagen_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", "disponible": True},
            {"id": 11, "nombre": "Combo Vegano Power", "precio_base": 16990, "tipo": "combo", "descripcion": "2 Bowls veganos gourmet, 2 Snacks vegetales crujientes, 1 Dip de hummus artesanal, 1 Bebida vegetal", "imagen_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", "disponible": True},
            {"id": 12, "nombre": "Combo Semanal Fit", "precio_base": 39990, "tipo": "combo", "descripcion": "5 Bowls variados (1 por día), 5 Snacks saludables, 2 Bebidas funcionales, 1 Guía de nutrición digital", "imagen_url": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", "disponible": True},
            {"id": 13, "nombre": "Combo Desayuno Express", "precio_base": 14990, "tipo": "combo", "descripcion": "3 Bowls de avena y granola, 3 Smoothies listos para beber, 2 Muffins saludables, 1 Café o té de especialidad", "imagen_url": "https://images.unsplash.com/photo-1551218808-94e220e084d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", "disponible": True},
            {"id": 14, "nombre": "Combo Pareja Saludable", "precio_base": 22990, "tipo": "combo", "descripcion": "4 Bowls (2 para cada uno), 4 Barras de proteína, 2 Bebidas energéticas, 2 Postres saludables", "imagen_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", "disponible": True},
            
            # ITEM ESPECIAL (Para personalización)
            {"id": 99, "nombre": "Bowl Personalizado", "precio_base": 6990, "tipo": "bowl", "descripcion": "Bowl a medida con ingredientes seleccionados.", "disponible": True, "imagen_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80"}
        ]

        for data in PRODUCTOS_DATA:
            # Aquí eliminamos el argumento duplicado. 'disponible' ya viene en el diccionario o asumimos True en el modelo.
            producto = models.Producto(**data)
            db.merge(producto)
        
        db.commit()
        print(f" {len(PRODUCTOS_DATA)} productos insertados.")

        # ---------------------------------------------------------
        # 2. USUARIOS INICIALES
        # ---------------------------------------------------------
        print("➡️  Creando usuarios de prueba...")

        # Admin
        admin_pass = bcrypt.hashpw("042025".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin = models.Usuario(
            nombre="Jesus Admin",
            email="jesuszavaleta55@gmail.com",
            hashed_password=admin_pass,
            rut="99.999.999-9",
            direccion="Oficina Central FitExpress",
            comuna="Santiago",
            rol="admin"
        )
        db.add(admin)
        db.commit()
        db.add(models.Carrito(usuario_id=admin.id)) # Carrito para admin
        
        # Cliente
        cliente_pass = bcrypt.hashpw("12345".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cliente = models.Usuario(
            nombre="Juan Cliente",
            email="cliente@prueba.com",
            hashed_password=cliente_pass,
            rut="11.111.111-1",
            direccion="Av. Providencia 123",
            comuna="Providencia",
            rol="cliente"
        )
        db.add(cliente)
        db.commit()
        db.add(models.Carrito(usuario_id=cliente.id)) # Carrito para cliente
        
        db.commit()
        print("✅ Usuarios Admin y Cliente creados.")

    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()
        print("🚀 Inicialización completada.")

if __name__ == "__main__":
    init_db()