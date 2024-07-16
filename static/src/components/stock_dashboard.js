/** @odoo-module **/

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks"
const { Component, onWillStart, useRef, onMounted, useState } = owl


export class StockDashboard extends Component {
    setup() {
        this.state = useState({
            gambiaSDH: {
                value: 0,
                percentage: 0,
            },
            gambiaBK: {
                value: 0,
                percentage: 0,
            },
            gambiaFT: {
                value: 0,
                percentage: 0,
            },
            average: {
                value: 0,
                percentage: 0,
            },
            token: '',
        });

        this.orm = useService("orm");
        this.actionService = useService("action");

        onWillStart(async () => {
            try {
                const token = await this.getAuthToken();
                this.state.token = token;
                console.log('Authentication Token:', token); // Log the token
                await this.fetchTemperatureData('66519', 'gambiaSDH'); // Fetch for Gambia SDH
                await this.fetchTemperatureData('66518', 'gambiaBK'); // Fetch for Gambia BK
                await this.fetchTemperatureData('66515', 'gambiaFT'); // Fetch for Gambia FT
                this.calculateAverageTemperature();
            } catch (error) {
                console.error('Error during setup:', error);
            }
        });
    }

   async getAuthToken() {
        try {
            const response = await fetch('https://api.secteurnetworks.com/proxy/identity');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log('Auth Token Response:', data); // Log the response data
            if (data.status !== 1) {
                throw new Error(`API error! message: ${data.msg}`);
            }
            return data.body.token; // Adjust according to the actual response structure
        } catch (error) {
            console.error('Error fetching authentication token:', error);
            throw error;
        }
    }

     async fetchTemperatureData(serialNumber, stateKey) {
        try {
            const response = await fetch(`https://api.secteurnetworks.com/proxy/data/${serialNumber}?token=${this.state.token}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log(`${stateKey} Temperature Data:`, data); // Log the response data
            if (data.status !== 1) {
                throw new Error(`API error! message: ${data.msg}`);
            }
            // Assuming the temperature value is in data.body.temperature
            this.state[stateKey].value = data.body.temperature;
            // Example percentage calculation (customize as needed)
            this.state[stateKey].percentage = (data.body.temperature / 100) * 100;
        } catch (error) {
            console.error(`Error fetching temperature data for ${serialNumber}:`, error);
        }
    }
    calculateAverageTemperature() {
        const total = this.state.gambiaSDH.value + this.state.gambiaBK.value + this.state.gambiaFT.value;
        const average = total / 3;
        this.state.average.value = parseFloat(average.toFixed(2));
        this.state.average.percentage = parseFloat(((average / 100) * 100).toFixed(2));
    }
}

StockDashboard.template = "rider_warehouse_cus.stock_dashboard";
StockDashboard.components = { KpiCard };

registry.category("actions").add("rider_warehouse_cus.stock_dashboard", StockDashboard);