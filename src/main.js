import { createApp } from "vue";
import App from "./App.vue";
import PrimeVue from "primevue/config";

// Import the styles
import "primevue/resources/themes/saga-blue/theme.css"; //theme
import "primevue/resources/primevue.min.css"; //core css
import "primeicons/primeicons.css"; //icons
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Dialog from "primevue/dialog";
import TabView from "primevue/tabview";
import TabPanel from "primevue/tabpanel";
import FloatLabel from "primevue/floatlabel";
import TextArea from "primevue/textarea";
const app = createApp(App);

// Use PrimeVue
app.use(PrimeVue);
app.component("PrimeButton", Button);
app.component("InputText", InputText);
app.component("DataTable", DataTable);
app.component("PrimeColumn", Column);
app.component("PrimeDialog", Dialog);
app.component("TabView",TabView);
app.component("TabPanel",TabPanel);
app.component("FloatLabel", FloatLabel);
app.component("TextArea", TextArea);
app.mount("#app");