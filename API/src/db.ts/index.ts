import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { notFound } from "./middleware/notFound";
import { errorHandler } from "./middleware/error";

// Rutas
import authRoutes from "./routes/auth";
import usersRoutes from "./routes/users";
import catalogRoutes from "./routes/catalog";
import cartRoutes from "./routes/cart";
import ordersRoutes from "./routes/orders";
import paymentsRoutes from "./routes/payments";
import invoicesRoutes from "./routes/invoices";
import dispatchRoutes from "./routes/dispatch";
import trackingRoutes from "./routes/tracking";
import refundsRoutes from "./routes/refunds";
import reportsRoutes from "./routes/reports";

dotenv.config();
const app = express();

app.use(cors());
app.use(express.json());

// Rutas
app.use("/auth", authRoutes);
app.use("/users", usersRoutes);
app.use("/catalog", catalogRoutes);
app.use("/cart", cartRoutes);
app.use("/orders", ordersRoutes);
app.use("/payments", paymentsRoutes);
app.use("/invoices", invoicesRoutes);
app.use("/dispatch", dispatchRoutes);
app.use("/tracking", trackingRoutes);
app.use("/refunds", refundsRoutes);
app.use("/reports", reportsRoutes);

app.use(notFound);
app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor corriendo en http://localhost:${PORT}`));
