/** @odoo-module */

import { registry} from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
const { Component } = owl

export class StockDashboard extends Component {}

StockDashboard.template = "riders_warehouse_custom.stock_dashboard"
StockDashboard.components = { KpiCard }

registry.category("actions").add("riders_warehouse_custom.stock_dashboard", StockDashboard)