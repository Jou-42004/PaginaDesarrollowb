# Diagrama de Clases UML - Fit Express

## Diagrama Global del Sistema

```mermaid
classDiagram
    %% ===== INTERFACES GLOBALES =====
    class ICRUD {
        <<interface>>
        +add(Object) Response
        +update(key: Object, input: Object) Response
        +delete(key: Object) Response
        +query(params: Object) Response
    }

    class Response {
        +status: HttpCode
        +data: Object
        +message: String
        +timestamp: Date
        +errors: List~ValidationError~
    }

    class ValidationError {
        +campo: String
        +mensaje: String
        +codigo: String
    }

    %% ===== ENTIDADES PRINCIPALES =====
    class Usuario {
        <<Entity>>
        +id: int
        +email: String
        +contraseña: String
        +nombre: String
        +rut: String
        +direccion: String
        +comuna: String
        +region: String
        +telefono: String
        +notificaPromo: boolean
        +fechaRegistro: Date
        +activo: boolean
    }

    class Pedido {
        <<Entity>>
        +id: String
        +usuarioId: int
        +fecha: Date
        +total: float
        +metodoPago: String
        +numeroConfirmacion: String
        +estado: String
        +direccionEntrega: String
        +comunaEntrega: String
        +tiempoEstimado: int
    }

    class Carrito {
        <<Entity>>
        +id: int
        +usuarioId: int
        +total: float
        +fechaCreacion: Date
        +items: List~CarritoItem~
    }

    class CarritoItem {
        <<Entity>>
        +id: int
        +carritoId: int
        +productoId: int
        +cantidad: int
        +precioUnitario: float
        +personalizacion: String
    }

    class Producto {
        <<Entity>>
        +id: int
        +nombre: String
        +descripcion: String
        +precio: float
        +calorias: int
        +macros: String
        +tipo: String
        +imagen: String
        +disponible: boolean
        +categoria: String
    }

    class Promocion {
        <<Entity>>
        +id: int
        +productoId: int
        +precioOriginal: float
        +precioPromocion: float
        +fechaInicio: Date
        +fechaExpiracion: Date
        +activa: boolean
        +tipo: String
    }

    class Documento {
        <<Entity>>
        +id: String
        +pedidoId: String
        +tipo: String
        +usuarioId: String
        +fecha: Date
        +montoTotal: float
        +rut: String
        +cantItems: String
        +numeroDocumento: String
    }

    class Notificacion {
        <<Entity>>
        +id: int
        +pedidoId: int
        +tipo: String
        +mensaje: String
        +fechaEstimada: Date
        +leida: boolean
        +fechaCreacion: Date
    }

    class Seguimiento {
        <<Entity>>
        +id: String
        +pedidoId: String
        +estado: String
        +entregaHora: Date
        +ubicacion: Object
        +repartidor: String
        +comentarios: String
        +fechaActualizacion: Date
    }

    class DireccionEntrega {
        <<Entity>>
        +id: int
        +usuarioId: int
        +calle: String
        +numero: String
        +depto: String
        +comuna: String
        +region: String
        +referencia: String
        +favorita: boolean
    }

    %% ===== SERVICIOS Y DTOs =====
    class UsuarioService {
        <<Service>>
        +add(input: UsuarioInput) Response
        +update(key: int, input: DatosPersonalesInput) Response
        +update(key: String, input: SuscripcionInput) Response
        +login(input: LoginInput) Response
        +cambiarContraseña(input: CambioContraseñaInput) Response
    }

    class ProductoService {
        <<Service>>
        +query(params: ProductoQueryInput) Response
        +query(key: int) Response
        +update(key: int, input: ProductoInput) Response
        +filtrarPorMacros(input: FiltroMacrosInput) Response
    }

    class PromocionService {
        <<Service>>
        +query(params: Object) Response
        +add(input: PromocionInput) Response
        +aplicarPromocion(input: AplicarPromocionInput) Response
    }

    class PedidoService {
        <<Service>>
        +add(input: PedidoInput) Response
        +update(key: String, input: ConfirmarPagoInput) Response
        +update(key: String, input: CancelarPedidoInput) Response
        +calcularTotal(input: CalcularTotalInput) Response
    }

    class CarritoService {
        <<Service>>
        +add(input: CarritoItemInput) Response
        +update(key: int, input: ActualizarCantidadInput) Response
        +delete(key: int) Response
        +delete() Response
        +calcularTotal() Response
    }

    class DocumentoService {
        <<Service>>
        +add(input: FacturaInput) Response
        +add(input: BoletaInput) Response
        +generarDocumento(input: GenerarDocumentoInput) Response
    }

    class NotificacionService {
        <<Service>>
        +add(input: CrearNotificacionInput) Response
        +update(key: String, input: ActualizarNotificacionInput) Response
        +enviarNotificacion(input: EnviarNotificacionInput) Response
    }

    class SeguimientoService {
        <<Service>>
        +query(key: String) Response
        +update(key: String, input: ConfirmarEntregaInput) Response
        +actualizarUbicacion(input: UbicacionInput) Response
    }

    class DireccionService {
        <<Service>>
        +add(input: DireccionInput) Response
        +update(key: int, input: DireccionInput) Response
        +delete(key: int) Response
        +marcarFavorita(key: int) Response
        +calcularCostoEnvio(input: CalcularEnvioInput) Response
    }

    %% ===== DTOs DE ENTRADA =====
    class UsuarioInput {
        <<DTO>>
        +email: String
        +contraseña: String
        +nombre: String
        +rut: String
        +direccion: String
        +comuna: String
        +region: String
        +telefono: String
        +notificaPromo: boolean
    }

    class LoginInput {
        <<DTO>>
        +email: String
        +contraseña: String
        +recordarSesion: boolean
    }

    class DatosPersonalesInput {
        <<DTO>>
        +nombre: String
        +telefono: String
        +direccion: String
        +comuna: String
        +region: String
    }

    class SuscripcionInput {
        <<DTO>>
        +email: String
        +notificaPromo: boolean
    }

    class CambioContraseñaInput {
        <<DTO>>
        +email: String
        +codigoVerificacion: String
        +nuevaContraseña: String
        +confirmarContraseña: String
    }

    class ProductoQueryInput {
        <<DTO>>
        +categoria: String
        +precioMin: float
        +precioMax: float
        +caloriasMin: int
        +caloriasMax: int
        +tipo: String
    }

    class ProductoInput {
        <<DTO>>
        +nombre: String
        +descripcion: String
        +precio: float
        +calorias: int
        +macros: String
        +tipo: String
        +imagen: String
        +categoria: String
    }

    class FiltroMacrosInput {
        <<DTO>>
        +proteinaMin: int
        +proteinaMax: int
        +carbohidratosMin: int
        +carbohidratosMax: int
        +grasasMin: int
        +grasasMax: int
    }

    class PedidoInput {
        <<DTO>>
        +usuarioId: int
        +items: List~CantidadItemInput~
        +direccionEntrega: String
        +comunaEntrega: String
        +metodoPago: String
        +observaciones: String
    }

    class CantidadItemInput {
        <<DTO>>
        +productoId: int
        +cantidad: int
        +personalizacion: String
        +precioUnitario: float
    }

    class CarritoItemInput {
        <<DTO>>
        +productoId: int
        +cantidad: int
        +personalizacion: String
    }

    class ActualizarCantidadInput {
        <<DTO>>
        +cantidad: int
    }

    class ConfirmarPagoInput {
        <<DTO>>
        +metodoPago: String
        +numeroConfirmacion: String
        +tokenPago: String
    }

    class CancelarPedidoInput {
        <<DTO>>
        +motivo: String
        +comentarios: String
    }

    class CalcularTotalInput {
        <<DTO>>
        +items: List~CantidadItemInput~
        +descuentos: List~DescuentoInput~
        +costoEnvio: float
    }

    class DescuentoInput {
        <<DTO>>
        +codigo: String
        +porcentaje: float
        +monto: float
    }

    class FacturaInput {
        <<DTO>>
        +pedidoId: String
        +usuarioId: String
        +rut: String
        +razonSocial: String
        +direccion: String
    }

    class BoletaInput {
        <<DTO>>
        +pedidoId: String
        +usuarioId: String
        +rut: String
        +nombre: String
        +direccion: String
    }

    class GenerarDocumentoInput {
        <<DTO>>
        +tipo: String
        +pedidoId: String
        +datosCliente: Object
    }

    class CrearNotificacionInput {
        <<DTO>>
        +pedidoId: int
        +tipo: String
        +mensaje: String
        +fechaEstimada: Date
    }

    class ActualizarNotificacionInput {
        <<DTO>>
        +leida: boolean
        +fechaLectura: Date
    }

    class EnviarNotificacionInput {
        <<DTO>>
        +pedidoId: int
        +tipo: String
        +canal: String
    }

    class ConfirmarEntregaInput {
        <<DTO>>
        +estado: String
        +comentarios: String
        +fotoEntrega: String
    }

    class UbicacionInput {
        <<DTO>>
        +pedidoId: String
        +latitud: double
        +longitud: double
        +direccion: String
        +timestamp: Date
    }

    class DireccionInput {
        <<DTO>>
        +calle: String
        +numero: String
        +depto: String
        +comuna: String
        +region: String
        +referencia: String
    }

    class CalcularEnvioInput {
        <<DTO>>
        +comuna: String
        +region: String
        +pesoTotal: float
    }

    class PromocionInput {
        <<DTO>>
        +productoId: int
        +precioOriginal: float
        +precioPromocion: float
        +fechaInicio: Date
        +fechaExpiracion: Date
        +tipo: String
    }

    class AplicarPromocionInput {
        <<DTO>>
        +codigoPromocion: String
        +pedidoId: String
    }

    %% ===== RELACIONES ENTRE ENTIDADES =====
    Usuario ||--o{ Pedido : "Realiza"
    Usuario ||--o| Carrito : "Tiene"
    Usuario ||--o{ DireccionEntrega : "Tiene"
    
    Pedido ||--o{ CarritoItem : "Contiene Items de"
    Pedido ||--o{ Documento : "Genera"
    Pedido ||--o{ Notificacion : "Genera"
    Pedido ||--o{ Seguimiento : "Genera"
    
    Carrito ||--o{ CarritoItem : "Contiene"
    
    CarritoItem }o--|| Producto : "Referencia"
    
    Producto ||--o{ Promocion : "Puede tener"

    %% ===== IMPLEMENTACIÓN DE INTERFACES =====
    UsuarioService ..|> ICRUD
    ProductoService ..|> ICRUD
    PromocionService ..|> ICRUD
    PedidoService ..|> ICRUD
    CarritoService ..|> ICRUD
    DocumentoService ..|> ICRUD
    NotificacionService ..|> ICRUD
    SeguimientoService ..|> ICRUD
    DireccionService ..|> ICRUD

    %% ===== USO DE DTOs POR SERVICIOS =====
    UsuarioService ..> UsuarioInput : "usa"
    UsuarioService ..> LoginInput : "usa"
    UsuarioService ..> DatosPersonalesInput : "usa"
    UsuarioService ..> SuscripcionInput : "usa"
    UsuarioService ..> CambioContraseñaInput : "usa"
    
    ProductoService ..> ProductoQueryInput : "usa"
    ProductoService ..> ProductoInput : "usa"
    ProductoService ..> FiltroMacrosInput : "usa"
    
    PromocionService ..> PromocionInput : "usa"
    PromocionService ..> AplicarPromocionInput : "usa"
    
    PedidoService ..> PedidoInput : "usa"
    PedidoService ..> ConfirmarPagoInput : "usa"
    PedidoService ..> CancelarPedidoInput : "usa"
    PedidoService ..> CalcularTotalInput : "usa"
    
    CarritoService ..> CarritoItemInput : "usa"
    CarritoService ..> ActualizarCantidadInput : "usa"
    
    DocumentoService ..> FacturaInput : "usa"
    DocumentoService ..> BoletaInput : "usa"
    DocumentoService ..> GenerarDocumentoInput : "usa"
    
    NotificacionService ..> CrearNotificacionInput : "usa"
    NotificacionService ..> ActualizarNotificacionInput : "usa"
    NotificacionService ..> EnviarNotificacionInput : "usa"
    
    SeguimientoService ..> ConfirmarEntregaInput : "usa"
    SeguimientoService ..> UbicacionInput : "usa"
    
    DireccionService ..> DireccionInput : "usa"
    DireccionService ..> CalcularEnvioInput : "usa"

    %% ===== RELACIONES ENTRE DTOs =====
    PedidoInput *-- CantidadItemInput : "contiene"
    CarritoItemInput --|> CantidadItemInput : "extiende"
    CalcularTotalInput *-- CantidadItemInput : "contiene"
    CalcularTotalInput *-- DescuentoInput : "contiene"

    %% ===== RETORNO DE SERVICIOS =====
    UsuarioService --> Response : "retorna"
    ProductoService --> Response : "retorna"
    PromocionService --> Response : "retorna"
    PedidoService --> Response : "retorna"
    CarritoService --> Response : "retorna"
    DocumentoService --> Response : "retorna"
    NotificacionService --> Response : "retorna"
    SeguimientoService --> Response : "retorna"
    DireccionService --> Response : "retorna"

    Response *-- ValidationError : "contiene"
```

## Descripción del Diagrama

### **Interfaces Globales**
- **`ICRUD`**: Interface estándar para operaciones CRUD que implementan todos los servicios
- **`Response`**: Clase genérica para respuestas estandarizadas del sistema
- **`ValidationError`**: Para manejo de errores de validación

### **Entidades Principales**
- **`Usuario`**: Gestión de usuarios del sistema
- **`Pedido`**: Órdenes de compra
- **`Carrito`** y **`CarritoItem`**: Gestión del carrito de compras
- **`Producto`**: Catálogo de productos
- **`Promocion`**: Descuentos y ofertas
- **`Documento`**: Boletas y facturas
- **`Notificacion`**: Sistema de notificaciones
- **`Seguimiento`**: Tracking de pedidos
- **`DireccionEntrega`**: Gestión de direcciones

### **Servicios**
Cada servicio implementa `ICRUD` y maneja la lógica de negocio específica:
- **`UsuarioService`**: Autenticación, registro, gestión de perfil
- **`ProductoService`**: Catálogo, filtros, búsquedas
- **`PromocionService`**: Gestión de ofertas
- **`PedidoService`**: Procesamiento de órdenes
- **`CarritoService`**: Gestión del carrito
- **`DocumentoService`**: Generación de documentos
- **`NotificacionService`**: Sistema de notificaciones
- **`SeguimientoService`**: Tracking de entregas
- **`DireccionService`**: Gestión de direcciones

### **DTOs (Data Transfer Objects)**
Cada servicio utiliza DTOs específicos para entrada y salida de datos, manteniendo la separación de responsabilidades y facilitando la validación.

### **Características del Diseño**
1. **Separación clara** entre entidades, servicios y DTOs
2. **Interface común** (`ICRUD`) para consistencia
3. **Respuestas estandarizadas** con `Response`
4. **DTOs específicos** para cada operación
5. **Relaciones bien definidas** entre entidades
6. **Escalabilidad** y mantenibilidad del código

