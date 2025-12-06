from sqlmodel import Session, select
from database import engine, create_db_and_tables
from modelos import models, schemas
from passlib.context import CryptContext

# Configuración para hashear la contraseña (igual que en tu gestor)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def poblar_base_datos():
    # 1. Crear las tablas si no existen
    create_db_and_tables()

    with Session(engine) as session:
        print("🌱 Iniciando poblado de base de datos...")

        # --- A. CREAR USUARIO DE PRUEBA (Juan Álvarez) ---
        # Verificamos si ya existe para no duplicarlo
        usuario_existente = session.exec(select(models.Usuario).where(models.Usuario.email == "juan@fitexpress.cl")).first()
        
        if not usuario_existente:
            juan = models.Usuario(
                nombre="Juan Álvarez",
                rut="11.222.333-4",
                email="juan@fitexpress.cl",
                telefono="+56912345678",
                password=get_password_hash("123"), # La clave es '123'
                direccion="Av. Siempre Viva 742",
                comuna="Providencia",
                region="Metropolitana",
                estado=schemas.EstadoUsuario.ACTIVO
            )
            session.add(juan)
            print("✅ Usuario 'Juan Álvarez' creado (User: juan@fitexpress.cl / Pass: 123)")
            
            # Crear carrito para Juan
            session.commit() # Guardar para tener el ID
            session.refresh(juan)
            carrito_juan = models.Carrito(usuario_id=juan.id, total=0)
            session.add(carrito_juan)
        else:
            print("ℹ️ Usuario 'Juan Álvarez' ya existe.")

        # --- B. CREAR PRODUCTOS ---
        # Producto 1: Bowl Quinoa
        prod1_existente = session.exec(select(models.Producto).where(models.Producto.nombre == "Bowl Quinoa Power")).first()
        if not prod1_existente:
            macros1 = models.Macros(kcal=420, p=24, f=12, c=54)
            prod1 = models.Producto(
                nombre="Bowl Quinoa Power",
                precio=7990,
                disponible=True,
                imagen_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                macros=macros1
            )
            session.add(prod1)
            print("✅ Producto 'Bowl Quinoa' creado.")

        # Producto 2: Bowl Proteico
        prod2_existente = session.exec(select(models.Producto).where(models.Producto.nombre == "Bowl Proteico Plus")).first()
        if not prod2_existente:
            macros2 = models.Macros(kcal=520, p=40, f=18, c=50)
            prod2 = models.Producto(
                nombre="Bowl Proteico Plus",
                precio=8990,
                disponible=True,
                imagen_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                macros=macros2
            )
            session.add(prod2)
            print("✅ Producto 'Bowl Proteico' creado.")

        # Producto 3: Snack Almendras
        prod3_existente = session.exec(select(models.Producto).where(models.Producto.nombre == "Snack Almendras")).first()
        if not prod3_existente:
            macros3 = models.Macros(kcal=180, p=15, f=8, c=12)
            prod3 = models.Producto(
                nombre="Snack Almendras",
                precio=1990,
                disponible=True,
                imagen_url="https://images.unsplash.com/photo-1619601875086-009b81185dcc?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                macros=macros3
            )
            session.add(prod3)
            print("✅ Producto 'Snack Almendras' creado.")

        session.commit()
        print("🚀 ¡Base de datos poblada con éxito!")

if __name__ == "__main__":
    poblar_base_datos()