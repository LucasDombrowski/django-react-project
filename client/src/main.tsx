import React from "react";
import ReactDOM from "react-dom/client";
import * as DjangoBridge from "@django-bridge/react";
import "./index.css";

import HomeView from "./views/Home";
import { CSRFTokenContext } from "./contexts";
import FormDef from "./adapters/Form";
import FieldDef from "./adapters/Field";
import ServerRenderedFieldDef from "./adapters/ServerRenderedField";
import TextInputDef from "./adapters/widgets/TextInput";
import SelectDef from "./adapters/widgets/Select";
import LoginView from "./views/Login";
import RegisterView from "./views/Register";
import MatchDetailView from "./views/MatchDetail";
import CompetitionDetailView from "./views/CompetitionDetail";
import TeamDetailView from "./views/TeamDetail";
const config = new DjangoBridge.Config();

// Add your views here
config.addView("HomeView", HomeView);
config.addView("LoginView", LoginView);
config.addView("RegisterView", RegisterView);
config.addView("MatchDetailView", MatchDetailView);
config.addView("CompetitionDetailView", CompetitionDetailView);
config.addView("TeamDetailView", TeamDetailView);

// Add your context providers here
config.addContextProvider("csrf_token", CSRFTokenContext);

// Add your adapters here
config.addAdapter("forms.Form", FormDef);
config.addAdapter("forms.Field", FieldDef);
config.addAdapter("forms.ServerRenderedField", ServerRenderedFieldDef);
config.addAdapter("forms.TextInput", TextInputDef);
config.addAdapter("forms.Select", SelectDef);

const rootElement = document.getElementById("root")!;
const initialResponse = JSON.parse(
  document.getElementById("initial-response")!.textContent!
);

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <DjangoBridge.App config={config} initialResponse={initialResponse} />
  </React.StrictMode>
);
