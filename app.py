from shiny import App, render, ui
import numpy as np
import plotly.graph_objects as go

# Configuration dictionaries
TISSUE_DESCRIPTIONS = {
    "cardiac": (
        "Cardiac action potentials have a characteristic long plateau phase (Phase 2) "
        "that lasts 200-300ms. This extended depolarization is due to slow Ca²⁺ channels "
        "and prevents tetanic contractions, ensuring proper heart pumping function. "
        "The five phases are: 0 (rapid depolarization), 1 (early repolarization), "
        "2 (plateau), 3 (repolarization), and 4 (resting potential)."
    ),
    "neuron": (
        "Neuronal action potentials are rapid, lasting only 1-2ms. They feature a sharp "
        "depolarization phase followed by quick repolarization and a brief hyperpolarization "
        "period. This rapid signaling allows neurons to transmit information quickly along "
        "axons. The brief refractory period enables high-frequency firing."
    ),
    "skeletal": (
        "Skeletal muscle action potentials have an intermediate duration of 2-5ms. "
        "They are similar to neuronal action potentials but slightly longer. The action "
        "potential propagates along the muscle fiber membrane (sarcolemma) and into "
        "T-tubules, triggering calcium release and muscle contraction."
    )
}

HR_RANGES = {
    "resting": (60, 80),
    "exercise": (120, 150),
    "stress": (90, 110),
    "sleep": (40, 60)
}

app_ui = ui.page_navbar(
# --- HOMEPAGE: LEONARDO A SINISTRA, ANIMAZIONI A DESTRA ---
    ui.nav_panel(
        "Home",
        ui.div(
            # Assicuriamoci che il player Lottie sia caricato nell'header della pagina
            ui.head_content(
                ui.HTML('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')
            ),
            
            ui.h1(
                "Human physiology can be cool", 
                style="margin-bottom: 40px; font-weight: 700; color: #2C3E50;"
            ),
            
            # Container Orizzontale (Sinistra: Immagine | Destra: Animazioni)
            ui.div(
                # PARTE SINISTRA: Immagine Leonardo
                ui.div(
                    ui.img(
                        src="https://raw.githubusercontent.com/DaniloBondi/Fisiologia/main/Leonardo.png", 
                        style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.15);"
                    ),
                    style="flex: 2; display: flex; align-items: center; justify-content: center; max-width: 600px;"
                ),
                
                # PARTE DESTRA: Colonna di Animazioni
                ui.div(
                    # Animazione 1: Health Care
                    ui.HTML('''
                        <lottie-player src="https://lottie.host/43f47864-77e8-4660-8481-905183495804/m0eP8nK9zO.json" 
                        background="transparent" speed="1" style="width: 150px; height: 150px;" loop autoplay></lottie-player>
                    '''),
                    # Animazione 2: Brain
                    ui.HTML('''
                        <lottie-player src="https://lottie.host/46112d8a-986b-4e4b-8012-005164d14210/pYfC8GfXp3.json" 
                        background="transparent" speed="1" style="width: 150px; height: 150px;" loop autoplay></lottie-player>
                    '''),
                    # Animazione 3: Lung
                    ui.HTML('''
                        <lottie-player src="https://lottie.host/5b487e0b-2224-42f0-9118-2e0f06560942/r3Z9uGf8rP.json" 
                        background="transparent" speed="1" style="width: 150px; height: 150px;" loop autoplay></lottie-player>
                    '''),
                    style="""
                        flex: 1; 
                        display: flex; 
                        flex-direction: column; 
                        align-items: center; 
                        justify-content: center; 
                        gap: 15px;
                        border-left: 2px solid #f0f0f0;
                        padding-left: 20px;
                    """
                ),
                
                style="""
                    display: flex; 
                    flex-direction: row; 
                    align-items: center; 
                    justify-content: center; 
                    gap: 40px; 
                    width: 100%; 
                    max-width: 1100px;
                    flex-wrap: nowrap;
                """
            ),
            
            ui.p(
                "Teaching materials and oddities curated by Danilo Bondi", 
                style="margin-top: 40px; font-size: 1.4rem; font-style: italic; color: #5D6D7E;"
            ),
            
            style="""
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                justify-content: center; 
                text-align: center; 
                min-height: 90vh; 
                padding: 30px;
                background-color: #ffffff;
            """
        )
    ),
    # -----------------------------
    ui.nav_panel(
        "Action Potential",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select(
                    "tissue_type",
                    "Select Tissue Type:",
                    choices={
                        "cardiac": "Cardiac Muscle",
                        "neuron": "Neuron",
                        "skeletal": "Skeletal Muscle"
                    },
                    selected="cardiac"
                ),
                ui.input_slider(
                    "duration",
                    "Time Window (ms):",
                    min=50,
                    max=500,
                    value=300,
                    step=10
                )
            ),
            ui.card(
                ui.card_header("Action Potential"),
                ui.output_ui("action_potential_plot")
            ),
            ui.card(
                ui.card_header("Description"),
                ui.output_text("description")
            )
        )
    ),
    ui.nav_panel(
        "Heart Rate",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select(
                    "condition",
                    "Select Condition:",
                    choices={
                        "resting": "Resting (60-80 bpm)",
                        "exercise": "Exercise (120-150 bpm)",
                        "stress": "Stress/Anxiety (90-110 bpm)",
                        "sleep": "Sleep (40-60 bpm)"
                    },
                    selected="resting"
                ),
                ui.input_slider(
                    "time_window",
                    "Time Window (seconds):",
                    min=5,
                    max=30,
                    value=10,
                    step=5
                ),
                ui.input_checkbox(
                    "show_variability",
                    "Show Heart Rate Variability",
                    value=True
                )
            ),
            ui.card(
                ui.card_header("ECG Signal Simulation"),
                ui.output_ui("ecg_plot")
            ),
            ui.card(
                ui.card_header("Heart Rate Statistics"),
                ui.output_text("hr_stats")
            )
        )
    ),
    ui.nav_panel(
        "About",
        ui.card(
            ui.card_header("About This Application"),
            ui.markdown(
                """
                This application simulates action potentials and heart rate patterns in different conditions.
                
                ### Features:
                - **Interactive Graphs**: Hover, zoom, and pan to explore the waveforms
                - **Multiple Tissue Types**: Compare cardiac muscle, neurons, and skeletal muscle
                - **Heart Rate Simulation**: View ECG patterns under different physiological conditions
                - **Heart Rate Variability**: Toggle HRV to see natural variation in heart rhythm
                
                ### Pages:
                
                **Action Potential**: Simulates action potentials across different tissue types
                with characteristic waveform shapes and durations.
                
                **Heart Rate**: Displays simulated ECG signals showing heart rate patterns
                during rest, exercise, stress, and sleep conditions.
                
                ---
                
                Developed to make human physiology concepts more accessible and engaging.
                """
            )
        )
    ),
    title=ui.tags.span(
        "Physiology Lab",
        style="font-family: 'Aptos', 'Segoe UI', 'Calibri', sans-serif; font-weight: 600;"
    ),
    id="page"
)

# --- Funzioni di supporto (rimaste invariate) ---

def generate_cardiac_ap(t):
    v = np.full_like(t, -90.0)
    v[(t >= 10) & (t < 12)] = -90 + (t[(t >= 10) & (t < 12)] - 10) * 65
    v[(t >= 12) & (t < 15)] = 40 - (t[(t >= 12) & (t < 15)] - 12) * 10
    v[(t >= 15) & (t < 210)] = 10
    v[(t >= 210) & (t < 260)] = 10 - (t[(t >= 210) & (t < 260)] - 210) * 2
    v[t >= 260] = -90
    return v

def generate_neuron_ap(t):
    v = np.full_like(t, -70.0)
    v[(t >= 10) & (t < 11)] = -70 + (t[(t >= 10) & (t < 11)] - 10) * 110
    v[(t >= 11) & (t < 13)] = 40 - (t[(t >= 11) & (t < 13)] - 11) * 55
    v[(t >= 13) & (t < 15)] = -70 - (t[(t >= 13) & (t < 15)] - 13) * 10
    v[t >= 15] = -70
    return v

def generate_skeletal_ap(t):
    v = np.full_like(t, -90.0)
    v[(t >= 10) & (t < 12)] = -90 + (t[(t >= 10) & (t < 12)] - 10) * 65
    v[(t >= 12) & (t < 15)] = 40 - (t[(t >= 12) & (t < 15)] - 12) * 36.67
    v[t >= 15] = -90
    return v

def create_plotly_figure(x, y, title, xlabel, ylabel, color='#2E86AB'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines',
        line=dict(color=color, width=2),
        hovertemplate=f'{xlabel}: %{{x:.2f}}<br>{ylabel}: %{{y:.2f}}<extra></extra>'
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#333')),
        xaxis=dict(title=xlabel, gridcolor='lightgray'),
        yaxis=dict(title=ylabel, gridcolor='lightgray'),
        hovermode='x unified',
        plot_bgcolor='white',
        height=500
    )
    return fig

def generate_ecg_beat(t_beat):
    signal = np.zeros_like(t_beat)
    signal += 0.15 * np.exp(-((t_beat - 0.13) ** 2) / (2 * 0.067 ** 2))
    signal -= 0.05 * np.exp(-((t_beat - 0.27) ** 2) / (2 * 0.017 ** 2))
    signal += 1.0 * np.exp(-((t_beat - 0.30) ** 2) / (2 * 0.017 ** 2))
    signal -= 0.15 * np.exp(-((t_beat - 0.33) ** 2) / (2 * 0.017 ** 2))
    signal += 0.25 * np.exp(-((t_beat - 0.58) ** 2) / (2 * 0.13 ** 2))
    return signal

def server(input, output, session):
    @render.ui
    def action_potential_plot():
        tissue = input.tissue_type()
        duration = input.duration()
        t = np.linspace(0, duration, 1000)
        ap_generators = {
            "cardiac": generate_cardiac_ap,
            "neuron": generate_neuron_ap,
            "skeletal": generate_skeletal_ap
        }
        v = ap_generators[tissue](t)
        fig = create_plotly_figure(
            x=t, y=v,
            title=f'Action Potential: {tissue.title()}',
            xlabel='Time (ms)', ylabel='Membrane Potential (mV)'
        )
        fig.update_xaxes(range=[0, duration])
        return ui.HTML(fig.to_html(include_plotlyjs="cdn", full_html=False))

    @render.text
    def description():
        return TISSUE_DESCRIPTIONS[input.tissue_type()]

    @render.ui
    def ecg_plot():
        condition = input.condition()
        time_window = input.time_window()
        show_hrv = input.show_variability()
        hr_min, hr_max = HR_RANGES[condition]
        base_hr = (hr_min + hr_max) / 2
        beat_interval = 60.0 / base_hr
        t = np.linspace(0, time_window, int(time_window * 1000))
        ecg_signal = np.zeros_like(t)
        current_time = 0.5
        while current_time < time_window - 0.5:
            beat_duration = 0.6
            beat_mask = (t >= current_time) & (t < current_time + beat_duration)
            if np.any(beat_mask):
                t_beat = (t[beat_mask] - current_time) / beat_duration
                ecg_signal[beat_mask] += generate_ecg_beat(t_beat)
            if show_hrv:
                variation = np.random.normal(0, 0.05 * beat_interval)
                next_interval = max(beat_interval + variation, beat_interval * 0.8)
            else:
                next_interval = beat_interval
            current_time += next_interval
        fig = create_plotly_figure(
            x=t, y=ecg_signal,
            title=f'ECG Signal: {condition.title()}',
            xlabel='Time (s)', ylabel='Voltage (mV)', color='#E63946'
        )
        return ui.HTML(fig.to_html(include_plotlyjs="cdn", full_html=False))

    @render.text
    def hr_stats():
        condition = input.condition()
        show_hrv = input.show_variability()
        hr_min, hr_max = HR_RANGES[condition]
        base_hr = (hr_min + hr_max) / 2
        if show_hrv:
            return f"Condition: {condition.title()}\nBase Heart Rate: {base_hr:.0f} bpm\nRange: {hr_min}-{hr_max} bpm\nVariability: Enabled (±5% variation)"
        else:
            return f"Condition: {condition.title()}\nBase Heart Rate: {base_hr:.0f} bpm\nRange: {hr_min}-{hr_max} bpm\nVariability: Disabled (constant)"

app = App(app_ui, server)
