import { EstadoPago, EstadoPedido, TipoDocumento } from "./enums";

export interface Usuario {
  id: string;
  nombre: string;
  email: string;
  password: string;
  activo: boolean;
}

export interface Producto {
  id: string;
  nombre: string;
  descripcion: string;
  precio: number;
  activo: boolean;
}

export interface Carrito {
  id: string;
  usuarioId: string;
  productos: ItemCarrito[];
}

export interface ItemCarrito {
  id: string;
  productoId: string;
  cantidad: number;
  precioUnitario: number;
}

export interface Pedido {
  id: string;
  usuarioId: string;
  estado: EstadoPedido;
  total: number;
  creadoEn: Date;
}

export interface Pago {
  id: string;
  pedidoId: string;
  monto: number;
  estado: EstadoPago;
  fecha: Date;
}

export interface DatosFacturacion {
  id: string;
  usuarioId: string;
  tipoDocumento: TipoDocumento;
  rut: string;
  razonSocial: string;
}
